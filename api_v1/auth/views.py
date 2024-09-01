from urllib import response

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from core.schemas.users import User

from .getters import (
    LOGIN_ROUTER_PREFIX,
    ROUTER_PREFIX,
    get_payload_from_token,
    get_user_auth_for_user_refresh,
)
from .token import TokenInfo, create_access_token, create_refresh_token
from .validate import auth_user_validate, get_current_active_user

router = APIRouter(prefix=ROUTER_PREFIX, tags=["JWT Auth"])


@router.post(LOGIN_ROUTER_PREFIX)
async def auth_user_jwt(user: User = Depends(auth_user_validate)):
    access_token = await create_access_token(user)
    refresh_token = await create_refresh_token(user)
    response = JSONResponse(
        content=TokenInfo(
            access_token=access_token, refresh_token=refresh_token
        ).model_dump()
    )
    response.set_cookie(key="refresh-token", value=refresh_token)
    return response


@router.post(
    "/refresh/", response_model=TokenInfo, response_model_exclude_none=True
)
async def auth_user_refresh_access_token(
    user: User = Depends(get_user_auth_for_user_refresh),
):
    access_token = await create_access_token(user)
    return TokenInfo(access_token=access_token)


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
