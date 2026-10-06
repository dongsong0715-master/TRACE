from sqlalchemy import JSON, Boolean, CheckConstraint, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import ID_TYPE, Base, TimestampMixin


class User(TimestampMixin, Base):
    __tablename__ = "users"
    __table_args__ = (CheckConstraint("role IN ('student','admin')", name="role"),)

    id: Mapped[int] = mapped_column(ID_TYPE, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(64), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(16), default="student", server_default="student")
    token_version: Mapped[int] = mapped_column(Integer, default=1, server_default="1")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")
    is_demo: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")


class StudentProfile(TimestampMixin, Base):
    __tablename__ = "student_profiles"
    __table_args__ = (
        CheckConstraint(
            "education IS NULL OR education IN ('college','bachelor','master')", name="education"
        ),
        CheckConstraint(
            "target_category IS NULL OR target_category IN ('python','frontend','data')",
            name="target_category",
        ),
    )

    id: Mapped[int] = mapped_column(ID_TYPE, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    nickname: Mapped[str] = mapped_column(String(64))
    education: Mapped[str | None] = mapped_column(String(16))
    target_category: Mapped[str | None] = mapped_column(String(16))
    preferred_cities_json: Mapped[list[str]] = mapped_column(JSON, default=list)
    version: Mapped[int] = mapped_column(Integer, default=1, server_default="1")
