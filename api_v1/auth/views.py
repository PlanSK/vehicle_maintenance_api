from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from loguru import logger
from pydantic import BaseModel

from api_v1.users.crud import get_user_by_username
from api_v1.users.schemas import User as UserSchema
from auth.password_operators import password_validation
from auth.utils import decode_jwt, encode_jwt
from core.config import settings
from core.database import db_interface

LOGIN_ROUTER_PREFIX = "/login/"


class TokenInfo(BaseModel):
    access_token: str
    token_type: str = "Bearer"


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


async def get_user_from_db_by_username(username: str):
    async with db_interface.session_factory() as session:
        user = await get_user_by_username(session=session, username=username)
    if not user:
        return None
    return UserSchema.model_validate(user)


async def auth_user_validate(username: str = Form(), password: str = Form()):
    if not (user := await get_user_from_db_by_username(username)):
        logger.error(f"User {username!r} not found in db.")
        raise http_unauth_exception

    if not password_validation(password=password, hash=user.password):
        logger.error(f"User {username!r} password incorrect.")
        raise http_unauth_exception
    elif not user.is_active:
        logger.error(f"Inactive user {username!r} try to login.")
        raise http_forbidden_exception

    return user


async def get_payload_from_token(
    token: str = Depends(oauth_token),
) -> dict:
    try:
        payload = decode_jwt(token=token)
    except InvalidTokenError:
        logger.error("Decode token error: Invalid token error.")
        raise http_unauth_exception
    return payload


async def get_active_user_from_payload(
    payload: dict = Depends(get_payload_from_token),
) -> UserSchema:
    if username := payload.get("username"):
        if user := await get_user_from_db_by_username(username):
            return user
    logger.error(f"User {username!r} not found in db.")
    raise http_unauth_exception


async def get_current_active_user(
    user: UserSchema = Depends(get_active_user_from_payload),
):
    if user.is_active:
        return user
    logger.error(f"Inactive user {user.username!r} try to login.")
    raise http_forbidden_exception


@router.post(LOGIN_ROUTER_PREFIX)
async def auth_user_jwt(user: UserSchema = Depends(auth_user_validate)):
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
        "email": user.email,
    }
    token = encode_jwt(jwt_payload)
    return TokenInfo(access_token=token)


@router.get("/users/me/")
async def auth_user_get_self_info(
    payload: dict = Depends(get_payload_from_token),
    user: UserSchema = Depends(get_current_active_user),
):
    return {
        "username": user.username,
        "email": user.email,
        "logged in": payload.get("iat"),
    }
