from typing import Annotated

from fastapi import Depends, Request, Security
from fastapi.security import APIKeyCookie
from sqlalchemy.orm import Session

from app.core.errors import AppError
from app.core.security import COOKIE_NAME, decode_token
from app.models import User


def get_db(request: Request):
    with request.app.state.session_factory() as session:
        yield session


DB = Annotated[Session, Depends(get_db)]
session_cookie = APIKeyCookie(name=COOKIE_NAME, auto_error=False)


def get_current_user(
    request: Request, db: DB, token: Annotated[str | None, Security(session_cookie)]
) -> User:
    if not token:
        raise AppError(401, "UNAUTHENTICATED", "请先登录")
    user_id, version = decode_token(token, request.app.state.settings)
    user = db.get(User, user_id)
    if user is None or not user.is_active or user.token_version != version:
        raise AppError(401, "UNAUTHENTICATED", "登录已失效，请重新登录")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def require_student(user: CurrentUser) -> User:
    if user.role != "student":
        raise AppError(403, "FORBIDDEN", "此功能仅面向学生")
    return user


def require_admin(user: CurrentUser) -> User:
    if user.role != "admin":
        raise AppError(403, "FORBIDDEN", "需要管理员权限")
    return user


StudentUser = Annotated[User, Depends(require_student)]
