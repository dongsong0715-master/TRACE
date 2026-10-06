import os
from pathlib import Path

import pytest
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import delete
from sqlalchemy.engine import make_url

from alembic import command
from app.core.config import Settings
from app.main import create_app
from app.models import StudentProfile, User

BACKEND = Path(__file__).resolve().parents[1]
ORIGIN = "http://localhost:5173"
TEST_SECRET = "only-for-tests-not-a-production-secret-" * 2


@pytest.fixture
def application(tmp_path, monkeypatch):
    # CI may use a dedicated MySQL 8 database. Refuse arbitrary non-test databases.
    url = os.getenv("TRACE_TEST_DATABASE_URL") or f"sqlite:///{tmp_path / 'test.db'}"
    if not url.startswith("sqlite") and make_url(url).database != "trace_test":
        pytest.fail("TRACE_TEST_DATABASE_URL must name the dedicated trace_test database")
    monkeypatch.setenv("DATABASE_URL", url)
    monkeypatch.setenv("JWT_SECRET", TEST_SECRET)
    monkeypatch.setenv("APP_ENV", "test")
    command.upgrade(Config(str(BACKEND / "alembic.ini")), "head")
    app = create_app(
        Settings(
            database_url=url,
            jwt_secret=TEST_SECRET,
            app_env="test",
            public_origin=ORIGIN,
            cookie_secure=False,
        )
    )
    with app.state.session_factory() as db:
        db.execute(delete(StudentProfile))
        db.execute(delete(User))
        db.commit()
    yield app
    app.state.engine.dispose()


@pytest.fixture
def client(application):
    with TestClient(application, headers={"Origin": ORIGIN}) as current:
        yield current


@pytest.fixture
def student(client):
    payload = {"username": "alice_01", "password": "Long-Password-123", "nickname": "苏同学"}
    assert client.post("/api/v1/auth/register", json=payload).status_code == 201
    login = client.post(
        "/api/v1/auth/login", json={k: payload[k] for k in ["username", "password"]}
    )
    assert login.status_code == 200
    return login.json()["data"]
