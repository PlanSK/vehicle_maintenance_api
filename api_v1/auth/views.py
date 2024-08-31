from fastapi import APIRouter, Depends

from auth.utils import encode_jwt
from core.schemas.users import User

from .getters import LOGIN_ROUTER_PREFIX, ROUTER_PREFIX, get_payload_from_token
from .token import TokenInfo
from .validate import auth_user_validate, get_current_active_user

router = APIRouter(prefix=ROUTER_PREFIX, tags=["JWT Auth"])


@router.post(LOGIN_ROUTER_PREFIX)
async def auth_user_jwt(user: User = Depends(auth_user_validate)):
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
    user: User = Depends(get_current_active_user),
):
    return {
        "username": user.username,
        "email": user.email,
        "logged in": payload.get("iat"),
    }
