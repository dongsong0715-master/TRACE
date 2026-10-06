from datetime import datetime, timedelta, timezone

import jwt
import pytest
from conftest import ORIGIN, TEST_SECRET
from fastapi.testclient import TestClient
from sqlalchemy import select, update

from app.core.security import COOKIE_NAME
from app.models import StudentProfile, User


def test_registration_is_atomic_and_hashes_password(client, application):
    payload = {"username": "New_User", "password": "Good-Password-123", "nickname": "  同学  "}
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()["data"]
    assert data["username"] == "new_user"
    assert isinstance(data["id"], str)
    assert data["profile"]["nickname"] == "同学"
    assert data["profile"]["version"] == 1
    assert "password_hash" not in data
    with application.state.session_factory() as db:
        user = db.scalar(select(User).where(User.username == "new_user"))
        assert user.password_hash.startswith("$argon2id$")
        assert payload["password"] not in user.password_hash
        assert db.scalar(select(StudentProfile).where(StudentProfile.user_id == user.id))
    duplicate = client.post("/api/v1/auth/register", json={**payload, "username": "NEW_USER"})
    assert duplicate.status_code == 409
    assert duplicate.json()["error"]["code"] == "USERNAME_EXISTS"


@pytest.mark.parametrize("extra", [{"role": "admin"}, {"user_id": "42"}])
def test_cannot_register_privileged_or_other_user(client, extra):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "intruder",
            "password": "Valid-Password-1",
            "nickname": "测试",
            **extra,
        },
    )
    assert response.status_code == 422
    assert "Valid-Password" not in response.text


def test_login_cookie_and_refresh_restore(client, student):
    assert client.get("/api/v1/me").json()["data"]["id"] == student["id"]
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "ALICE_01",
            "password": "Long-Password-123",
        },
    )
    cookie = response.headers["set-cookie"]
    assert "HttpOnly" in cookie and "SameSite=lax" in cookie
    assert "Path=/api" in cookie and "Max-Age=7200" in cookie
    assert "trace_session" not in response.json()["data"]
    assert response.headers["cache-control"] == "no-store"
    assert response.json()["request_id"] == response.headers["x-request-id"]


def test_logout_revokes_old_cookie_in_another_browser(client, application, student):
    old_cookie = client.cookies.get(COOKIE_NAME)
    assert client.post("/api/v1/auth/logout").status_code == 200
    assert client.get("/api/v1/me").status_code == 401
    with TestClient(application) as other:
        other.cookies.set(COOKIE_NAME, old_cookie, path="/api")
        assert other.get("/api/v1/me").status_code == 401


@pytest.mark.parametrize(
    "username,password",
    [
        ("alice_01", "incorrect-password"),
        ("unknown_user", "incorrect-password"),
    ],
)
def test_credentials_errors_are_generic(client, student, username, password):
    response = client.post("/api/v1/auth/login", json={"username": username, "password": password})
    assert response.status_code == 401
    assert response.json()["error"] == {
        "code": "INVALID_CREDENTIALS",
        "message": "用户名或密码不正确",
    }


@pytest.mark.parametrize("origin", [None, "http://evil.example", "null"])
def test_write_requires_exact_origin(application, origin):
    with TestClient(application) as client:
        headers = {"Origin": origin} if origin else {}
        response = client.post(
            "/api/v1/auth/register",
            headers=headers,
            json={
                "username": "attempt",
                "password": "Good-Password-123",
                "nickname": "测试",
            },
        )
        assert response.status_code == 403
        assert response.json()["error"]["code"] == "ORIGIN_REJECTED"


def test_profile_update_uses_current_user_and_rejects_stale_version(client, student, application):
    response = client.patch(
        "/api/v1/me/profile",
        json={
            "version": 1,
            "nickname": "小苏",
            "education": "bachelor",
            "target_category": "python",
            "preferred_cities": ["北京", "天津"],
        },
    )
    assert response.status_code == 200
    assert response.json()["data"]["version"] == 2
    conflict = client.patch("/api/v1/me/profile", json={"version": 1, "nickname": "旧昵称"})
    assert conflict.status_code == 409
    assert client.get("/api/v1/me").json()["data"]["profile"]["nickname"] == "小苏"
    with TestClient(application, headers={"Origin": ORIGIN}) as bob:
        bob.post(
            "/api/v1/auth/register",
            json={
                "username": "bob_01",
                "password": "Different-Password",
                "nickname": "小李",
            },
        )
        bob.post(
            "/api/v1/auth/login", json={"username": "bob_01", "password": "Different-Password"}
        )
        assert bob.get("/api/v1/me").json()["data"]["profile"]["nickname"] == "小李"
        malicious = bob.patch(
            "/api/v1/me/profile",
            json={
                "version": 2,
                "nickname": "越权",
                "user_id": student["id"],
            },
        )
        assert malicious.status_code == 422
    assert client.get("/api/v1/me").json()["data"]["profile"]["nickname"] == "小苏"


@pytest.mark.parametrize(
    "payload",
    [
        {"version": 1, "preferred_cities": ["北京", "北京"]},
        {"version": 1, "nickname": "   "},
        {"version": 1, "nickname": None},
        {"version": 1, "preferred_cities": None},
        {"version": 1, "education": "unknown"},
        {"version": 1, "target_category": "unknown"},
        {"version": 1},
        {"version": 1, "preferred_cities": ["A", "B", "C", "D", "E", "F"]},
    ],
)
def test_invalid_profiles_are_rejected(client, student, payload):
    assert client.patch("/api/v1/me/profile", json=payload).status_code == 422


def test_disabled_account_cannot_authenticate_or_reuse_token(client, application, student):
    with application.state.session_factory() as db:
        db.execute(
            update(User)
            .where(User.id == int(student["id"]))
            .values(
                is_active=False,
                token_version=User.token_version + 1,
            )
        )
        db.commit()
    assert client.get("/api/v1/me").status_code == 401
    assert (
        client.post(
            "/api/v1/auth/login",
            json={
                "username": "alice_01",
                "password": "Long-Password-123",
            },
        ).status_code
        == 401
    )


@pytest.mark.parametrize("tampered", [False, True])
def test_expired_and_tampered_token(client, student, tampered):
    if tampered:
        cookie = client.cookies.get(COOKIE_NAME)
        head, body, signature = cookie.split(".")
        cookie = ".".join([head, body, ("a" if signature[0] != "a" else "b") + signature[1:]])
    else:
        now = datetime.now(timezone.utc)
        cookie = jwt.encode(
            {
                "sub": student["id"],
                "ver": 1,
                "iat": now - timedelta(hours=3),
                "exp": now - timedelta(hours=1),
                "iss": "trace",
                "aud": "trace-web",
            },
            TEST_SECRET,
            algorithm="HS256",
        )
    client.cookies.clear()
    client.cookies.set(COOKIE_NAME, cookie, path="/api")
    assert client.get("/api/v1/me").status_code == 401


def test_admin_cannot_edit_student_profile(client, student, application):
    with application.state.session_factory() as db:
        db.execute(update(User).where(User.id == int(student["id"])).values(role="admin"))
        db.commit()
    assert client.get("/api/v1/me").json()["data"]["role"] == "admin"
    assert (
        client.patch("/api/v1/me/profile", json={"version": 1, "nickname": "管理员"}).status_code
        == 403
    )


def test_no_session_and_allowed_preflight(client):
    assert client.get("/api/v1/me").status_code == 401
    health = client.get("/api/v1/health")
    assert health.status_code == 200
    response = client.options(
        "/api/v1/auth/login",
        headers={
            "Origin": ORIGIN,
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type",
        },
    )
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == ORIGIN


def test_validation_response_does_not_echo_password(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "bad name",
            "password": "private-value",
            "nickname": "测试",
        },
    )
    assert response.status_code == 422
    assert "private-value" not in response.text
