from loguru import logger
from pydantic import BaseModel

from auth.utils import encode_jwt
from core.config import settings
from core.schemas.users import User
from .exceptions import http_unauth_exception

class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


async def create_jwt(
    token_type: str,
    payload: dict,
    expire_minutes: int = settings.auth.access_token_expire_minutes,
    expire_days: int | None = None,
) -> str:
    payload_data = {TOKEN_TYPE_FIELD: token_type}
    payload_data.update(payload)
    if token_type == REFRESH_TOKEN_TYPE:
        return await encode_jwt(payload_data, expire_days=expire_days)
    return await encode_jwt(
        payload=payload_data,
        expire_minutes=expire_minutes,
    )


async def create_access_token(user: User) -> str:
    access_token_payload = {
        "sub": user.username,
        "user_id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "email": user.email,
    }
    return await create_jwt(
        token_type=ACCESS_TOKEN_TYPE, payload=access_token_payload
    )


async def create_refresh_token(user: User):
    refresh_token_payload = {
        "sub": user.username,
        "user_id": user.id,
        "username": user.username,
    }

    return await create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        payload=refresh_token_payload,
        expire_days=settings.auth.refresh_token_expire_days,
    )


async def token_type_validation(payload: dict, needed_token_type: str) -> bool:
    if payload.get(TOKEN_TYPE_FIELD) != needed_token_type:
        logger.error(
            f"Error of checing token type. "
            f"Token type is not {needed_token_type!r}."
        )
        raise http_unauth_exception
    return True
