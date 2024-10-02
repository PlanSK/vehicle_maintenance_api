from fastapi import Depends, Form
from loguru import logger

from auth.password_operators import password_validation
from core.schemas.users import UserSchema

from .exceptions import http_forbidden_exception, http_unauth_exception
from .getters import get_active_user_from_payload, get_user_from_db_by_username


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


async def get_current_active_user(
    user: UserSchema = Depends(get_active_user_from_payload),
):
    if user.is_active:
        return user
    logger.error(f"Inactive user {user.username!r} try to login.")
    raise http_forbidden_exception
