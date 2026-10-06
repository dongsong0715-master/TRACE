from typing import Generic, Literal, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class Envelope(BaseModel, Generic[T]):
    data: T
    request_id: str


class ProfileOut(BaseModel):
    id: str
    nickname: str
    education: Literal["college", "bachelor", "master"] | None
    target_category: Literal["python", "frontend", "data"] | None
    preferred_cities: list[str]
    version: int


class AccountOut(BaseModel):
    id: str
    username: str
    role: Literal["student", "admin"]
    is_demo: bool
    profile: ProfileOut | None


class LogoutOut(BaseModel):
    logged_out: bool


class HealthOut(BaseModel):
    status: Literal["ok"]
    version: str
    database: Literal["connected"]
