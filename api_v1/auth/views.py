from fastapi import APIRouter, Cookie, Depends
from fastapi.responses import JSONResponse
from loguru import logger

from core.schemas.users import User

from .exceptions import http_unauth_exception
from .getters import (
    LOGIN_ROUTER_PREFIX,
    ROUTER_PREFIX,
    get_active_user_from_payload_for_refresh,
    get_payload_from_token,
)
from .token import TokenInfo, create_access_token, create_refresh_token
from .validate import auth_user_validate, get_current_active_user


router = APIRouter(
    prefix=ROUTER_PREFIX,
    tags=["JWT Auth"],
)


@router.post(LOGIN_ROUTER_PREFIX)
async def auth_user_jwt(user: User = Depends(auth_user_validate)):
    access_token = await create_access_token(user)
    refresh_token = await create_refresh_token(user)
    response = JSONResponse(
        content=TokenInfo(
            access_token=access_token, refresh_token=refresh_token
        ).model_dump()
    )
    response.set_cookie(key="refresh_token", value=refresh_token)
    return response


@router.get(
    "/refresh/", response_model=TokenInfo, response_model_exclude_none=True
)
async def auth_user_refresh_access_token(
    refresh_token: str | None = Cookie(default=None),
):
    if refresh_token:
        payload: dict = await get_payload_from_token(token=refresh_token)
        user: User = await get_active_user_from_payload_for_refresh(payload)
        if user.is_active:
            access_token = await create_access_token(user)
            return TokenInfo(access_token=access_token)
    raise http_unauth_exception


@router.get("/users/me/")
async def auth_user_get_self_info(
    payload: dict = Depends(get_payload_from_token),
    user: User = Depends(get_current_active_user),
):
    return {
        "username": user.username,
        "email": user.email,
        "logged in": payload.get("iat"),
    }
