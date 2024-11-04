from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import ExpiredSignatureError, InvalidTokenError
from loguru import logger

from api_v1.users.crud import get_user_by_username
from auth.utils import decode_jwt
from core.config import settings
from core.database import db_handler
from core.schemas.users import UserSchema

from .exceptions import http_unauth_exception
from .token import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE, token_type_validation

LOGIN_ROUTER_PREFIX = "/login/"
REFRESH_ROUTER_PREFIX = "/refresh/"
ROUTER_PREFIX = "/auth"


oauth_token = OAuth2PasswordBearer(
    tokenUrl=settings.api_v1_prefix + ROUTER_PREFIX + LOGIN_ROUTER_PREFIX
)


async def get_user_from_db_by_username(username: str) -> UserSchema | None:
    async for db_session in db_handler.get_db():
        async with db_session as session:
            user = await get_user_by_username(
                session=session, username=username
            )
    if not user:
        return None
    return UserSchema.model_validate(user)


async def get_payload_from_token(
    token: str = Depends(oauth_token),
) -> dict:
    try:
        payload = await decode_jwt(token=token)
    except ExpiredSignatureError:
        logger.error("Token signature has expired. Needs refreshing.")
        raise http_unauth_exception
    except InvalidTokenError:
        logger.error("Decode token error: Invalid token error.")
        raise http_unauth_exception
    return payload


async def get_active_user_from_payload(
    payload: dict = Depends(get_payload_from_token),
) -> UserSchema:
    if await token_type_validation(
        payload=payload, needed_token_type=ACCESS_TOKEN_TYPE
    ):
        if username := payload.get("username"):
            if user := await get_user_from_db_by_username(username):
                return user
    logger.error(f"User {username!r} not found in db or token type incorrect.")
    raise http_unauth_exception


async def get_active_user_from_payload_for_refresh(
    payload: dict = Depends(get_payload_from_token),
) -> UserSchema:
    if await token_type_validation(
        payload=payload, needed_token_type=REFRESH_TOKEN_TYPE
    ):
        if username := payload.get("username"):
            if user := await get_user_from_db_by_username(username):
                return user
    logger.error(f"User {username!r} not found in db or token type incorrect.")
    raise http_unauth_exception
