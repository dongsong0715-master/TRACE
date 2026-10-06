from datetime import datetime, timedelta, timezone

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError

from app.core.config import Settings
from app.core.errors import AppError

COOKIE_NAME = "trace_session"
hasher = PasswordHasher()
_DUMMY_HASH = hasher.hash("dummy-password-for-timing-only")


def hash_password(password: str) -> str:
    return hasher.hash(password)


def verify_password(password: str, stored_hash: str | None) -> bool:
    try:
        valid = hasher.verify(stored_hash or _DUMMY_HASH, password)
        return valid and stored_hash is not None
    except (VerificationError, InvalidHashError):
        return False


def encode_token(user_id: int, token_version: int, settings: Settings) -> str:
    now = datetime.now(timezone.utc)
    return jwt.encode(
        {
            "sub": str(user_id),
            "ver": token_version,
            "iat": now,
            "exp": now + timedelta(minutes=settings.access_token_minutes),
            "iss": "trace",
            "aud": "trace-web",
        },
        settings.jwt_secret,
        algorithm="HS256",
    )


def decode_token(token: str, settings: Settings) -> tuple[int, int]:
    try:
        claims = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=["HS256"],
            issuer="trace",
            audience="trace-web",
            options={"require": ["sub", "ver", "iat", "exp", "iss", "aud"]},
        )
        if not isinstance(claims["sub"], str) or not claims["sub"].isdigit():
            raise ValueError("Invalid subject")
        if type(claims["ver"]) is not int:
            raise ValueError("Invalid version")
        return int(claims["sub"]), claims["ver"]
    except (jwt.InvalidTokenError, ValueError, TypeError):
        raise AppError(401, "UNAUTHENTICATED", "登录已失效，请重新登录") from None
