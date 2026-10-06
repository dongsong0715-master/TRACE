from fastapi import APIRouter, Request, Response
from sqlalchemy import update

from app.api.dependencies import DB, CurrentUser, StudentUser
from app.core.errors import success
from app.core.security import COOKIE_NAME, encode_token
from app.models import User
from app.schemas.auth import Credentials, ProfilePatch, RegisterInput
from app.schemas.responses import AccountOut, Envelope, LogoutOut, ProfileOut
from app.services.accounts import account_data, authenticate, create_student, save_profile

router = APIRouter()


@router.post("/auth/register", status_code=201, tags=["auth"], response_model=Envelope[AccountOut])
def register(payload: RegisterInput, request: Request, db: DB):
    user = create_student(db, payload, is_demo=request.app.state.settings.data_mode == "demo")
    return success(request, account_data(db, user))


@router.post("/auth/login", tags=["auth"], response_model=Envelope[AccountOut])
def login(payload: Credentials, request: Request, response: Response, db: DB):
    user = authenticate(db, payload)
    settings = request.app.state.settings
    response.set_cookie(
        COOKIE_NAME,
        encode_token(user.id, user.token_version, settings),
        max_age=settings.access_token_minutes * 60,
        httponly=True,
        secure=settings.cookie_secure,
        samesite="lax",
        path="/api",
    )
    return success(request, account_data(db, user))


@router.post("/auth/logout", tags=["auth"], response_model=Envelope[LogoutOut])
def logout(request: Request, response: Response, db: DB, user: CurrentUser):
    # Atomic increment revokes every session, including simultaneous logouts.
    db.execute(
        update(User)
        .where(User.id == user.id)
        .values(
            token_version=User.token_version + 1,
        )
    )
    db.commit()
    response.delete_cookie(
        COOKIE_NAME,
        path="/api",
        httponly=True,
        secure=request.app.state.settings.cookie_secure,
        samesite="lax",
    )
    return success(request, {"logged_out": True})


@router.get("/me", tags=["me"], response_model=Envelope[AccountOut])
def me(request: Request, db: DB, user: CurrentUser):
    return success(request, account_data(db, user))


@router.patch("/me/profile", tags=["me"], response_model=Envelope[ProfileOut])
def profile(payload: ProfilePatch, request: Request, db: DB, user: StudentUser):
    return success(request, save_profile(db, user, payload))
