import pytest
from pydantic import ValidationError

from app.core.config import Settings


def test_production_requires_https_secure_cookie_and_mysql():
    with pytest.raises(ValidationError):
        Settings(
            app_env="production",
            jwt_secret="s" * 48,
            database_url="sqlite:///test.db",
            cookie_secure=False,
        )


def test_production_config_is_accepted():
    settings = Settings(
        app_env="production",
        jwt_secret="s" * 48,
        database_url="mysql+pymysql://user:password@localhost/trace",
        public_origin="https://trace.example",
        cookie_secure=True,
    )
    assert settings.access_token_minutes == 120


def test_placeholder_secret_is_rejected():
    with pytest.raises(ValidationError):
        Settings(jwt_secret="REPLACE_WITH_RANDOM_SECRET_AT_LEAST_32_CHARACTERS")


def test_configuration_errors_do_not_print_secrets():
    secret = "private-jwt-secret-that-must-not-be-logged"
    with pytest.raises(ValidationError) as exc:
        Settings(
            app_env="production",
            jwt_secret=secret,
            database_url="mysql+pymysql://user:private-db-password@localhost/trace",
            cookie_secure=False,
        )
    assert secret not in str(exc.value)
    assert "private-db-password" not in str(exc.value)
