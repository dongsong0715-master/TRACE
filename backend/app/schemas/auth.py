from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class StrictInput(BaseModel):
    model_config = ConfigDict(extra="forbid", hide_input_in_errors=True)


class Credentials(StrictInput):
    username: str = Field(min_length=3, max_length=64, pattern=r"^[a-zA-Z0-9_]+$")
    password: str = Field(min_length=8, max_length=128)

    @field_validator("username")
    @classmethod
    def canonical_username(cls, value: str) -> str:
        return value.lower()


class RegisterInput(Credentials):
    nickname: str = Field(min_length=1, max_length=64)

    @field_validator("nickname")
    @classmethod
    def meaningful_nickname(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("昵称不能为空")
        return value


class ProfilePatch(StrictInput):
    version: int = Field(ge=1)
    nickname: str | None = Field(default=None, min_length=1, max_length=64)
    education: Literal["college", "bachelor", "master"] | None = None
    target_category: Literal["python", "frontend", "data"] | None = None
    preferred_cities: list[str] | None = Field(default=None, max_length=5)

    @field_validator("nickname")
    @classmethod
    def validate_nickname(cls, value: str | None):
        if value is None or not value.strip():
            raise ValueError("昵称不能为空")
        return value.strip()

    @field_validator("preferred_cities")
    @classmethod
    def validate_cities(cls, value: list[str] | None):
        if value is None:
            raise ValueError("城市应为列表")
        cities = [city.strip() for city in value]
        if any(not city or len(city) > 64 for city in cities) or len(set(cities)) != len(cities):
            raise ValueError("城市不能为空、重复或过长")
        return cities
