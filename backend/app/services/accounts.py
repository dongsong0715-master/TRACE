from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.errors import AppError
from app.core.security import hash_password, verify_password
from app.models import StudentProfile, User
from app.schemas.auth import Credentials, ProfilePatch, RegisterInput


def create_student(db: Session, payload: RegisterInput, *, is_demo: bool) -> User:
    user = User(
        username=payload.username,
        password_hash=hash_password(payload.password),
        role="student",
        is_demo=is_demo,
    )
    try:
        db.add(user)
        db.flush()
        db.add(StudentProfile(user_id=user.id, nickname=payload.nickname))
        db.commit()
    except IntegrityError:
        db.rollback()
        raise AppError(409, "USERNAME_EXISTS", "用户名已存在，请换一个") from None
    return user


def authenticate(db: Session, payload: Credentials) -> User:
    user = db.scalar(select(User).where(User.username == payload.username))
    if not verify_password(payload.password, user.password_hash if user else None):
        raise AppError(401, "INVALID_CREDENTIALS", "用户名或密码不正确")
    if not user.is_active:
        raise AppError(401, "INVALID_CREDENTIALS", "用户名或密码不正确")
    return user


def serialize_profile(profile: StudentProfile):
    return {
        "id": str(profile.id),
        "nickname": profile.nickname,
        "education": profile.education,
        "target_category": profile.target_category,
        "preferred_cities": profile.preferred_cities_json,
        "version": profile.version,
    }


def account_data(db: Session, user: User):
    profile = db.scalar(select(StudentProfile).where(StudentProfile.user_id == user.id))
    return {
        "id": str(user.id),
        "username": user.username,
        "role": user.role,
        "is_demo": user.is_demo,
        "profile": serialize_profile(profile) if profile else None,
    }


def save_profile(db: Session, user: User, payload: ProfilePatch):
    values = payload.model_dump(exclude_unset=True, exclude={"version"})
    if "preferred_cities" in values:
        values["preferred_cities_json"] = values.pop("preferred_cities")
    if not values:
        raise AppError(422, "EMPTY_UPDATE", "至少更新一个资料字段")
    result = db.execute(
        update(StudentProfile)
        .where(
            StudentProfile.user_id == user.id,
            StudentProfile.version == payload.version,
        )
        .values(**values, version=StudentProfile.version + 1)
    )
    if result.rowcount != 1:
        db.rollback()
        raise AppError(409, "PROFILE_VERSION_CONFLICT", "资料已更新，请刷新后再保存")
    db.commit()
    profile = db.scalar(select(StudentProfile).where(StudentProfile.user_id == user.id))
    db.refresh(profile)
    return serialize_profile(profile)
