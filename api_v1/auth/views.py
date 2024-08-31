from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from loguru import logger
from pydantic import BaseModel

from auth.password_operators import password_validation
from auth.utils import decode_jwt, encode_jwt
from core.config import settings

from .schemas import UserSchema, users_db

LOGIN_ROUTER_PREFIX = "/login/"


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


router = APIRouter(prefix="/jwt", tags=["JWT Auth"])
oauth_token = OAuth2PasswordBearer(
    tokenUrl=settings.api_v1_prefix + router.prefix + LOGIN_ROUTER_PREFIX
)


http_forbidden_exception: HTTPException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden."
)
http_unauth_exception: HTTPException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect auth data.",
)


def auth_user_validate(username: str = Form(), password: str = Form()):
    if not (user := users_db.get(username)):
        logger.error(f"User {username!r} not found in db.")
        raise http_unauth_exception

    if not password_validation(password=password, hash=user.password):
        logger.error(f"User {username!r} password incorrect.")
        raise http_unauth_exception
    elif not user.is_active:
        logger.error(f"Inactive user {username!r} try to login.")
        raise http_forbidden_exception

    return user


def get_current_payload_from_token(
    token: str = Depends(oauth_token),
) -> UserSchema:
    try:
        payload = decode_jwt(token=token)
    except InvalidTokenError:
        logger.error("Decode token error: Invalid token error.")
        raise http_unauth_exception
    return payload


def get_active_user_from_payload(
    payload: dict = Depends(get_current_payload_from_token),
) -> UserSchema:
    username: str | None = payload.get("username")
    if username and (user := users_db.get(username)):
        return user
    logger.error(f"User {username!r} not found in db.")
    raise http_unauth_exception


def get_current_active_user(
    user: UserSchema = Depends(get_active_user_from_payload),
):
    if user.is_active:
        return user
    logger.error(f"Inactive user {user.username!r} try to login.")
    raise http_forbidden_exception


@router.post(LOGIN_ROUTER_PREFIX)
def auth_user_jwt(user: UserSchema = Depends(auth_user_validate)):
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
        "email": user.email,
    }
    token = encode_jwt(jwt_payload)
    return TokenInfo(access_token=token, token_type="Bearer")


@router.get("/users/me/")
def auth_user_get_self_info(
    payload: dict = Depends(get_current_payload_from_token),
    user: UserSchema = Depends(get_current_active_user),
):
    return {
        "username": user.username,
        "email": user.email,
        "logged in": payload.get("iat"),
    }
