from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from loguru import logger

from api_v1.users.crud import get_user_by_username
from core.schemas.users import User
from auth.utils import decode_jwt
from core.config import settings
from core.database import db_interface

from .exceptions import http_unauth_exception

LOGIN_ROUTER_PREFIX = "/login/"
ROUTER_PREFIX = "/auth"


oauth_token = OAuth2PasswordBearer(
    tokenUrl=settings.api_v1_prefix + ROUTER_PREFIX + LOGIN_ROUTER_PREFIX
)


async def get_user_from_db_by_username(username: str):
    async with db_interface.session_factory() as session:
        user = await get_user_by_username(session=session, username=username)
    if not user:
        return None
    return User.model_validate(user)


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
) -> User:
    if username := payload.get("username"):
        if user := await get_user_from_db_by_username(username):
            return user
    logger.error(f"User {username!r} not found in db.")
    raise http_unauth_exception
