from pathlib import Path
from typing import Literal

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BACKEND_DIR / ".env", extra="ignore", hide_input_in_errors=True
    )

    app_env: Literal["development", "test", "production"] = "development"
    database_url: str = "sqlite:///./trace.db"
    jwt_secret: str = Field(min_length=32)
    public_origin: str = "http://localhost:5173"
    access_token_minutes: int = Field(default=120, ge=1, le=1440)
    cookie_secure: bool = False
    data_mode: Literal["demo", "real"] = "demo"

    @field_validator("jwt_secret")
    @classmethod
    def reject_placeholder_secret(cls, value: str) -> str:
        if value.upper().startswith(("REPLACE_", "GENERATE_")):
            raise ValueError("请使用 setup_local.py 生成本机随机密钥")
        return value

    @model_validator(mode="after")
    def production_requires_secure_config(self):
        if self.public_origin.endswith("/"):
            raise ValueError("PUBLIC_ORIGIN 不应以 / 结尾")
        if self.app_env == "production" and (
            not self.cookie_secure
            or not self.public_origin.startswith("https://")
            or not self.database_url.startswith("mysql+pymysql://")
        ):
            raise ValueError("生产环境必须配置 HTTPS、Secure Cookie 和 MySQL")
        return self
