from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from pydantic import BaseModel

from .schemas import UserSchema
from .utils import decode_jwt, encode_jwt, password_hasher, password_validation


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


oauth_token = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/jwt/login/")
router = APIRouter(prefix="/jwt", tags=["JWT"])

http_forbidden_exception: HTTPException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden."
)
http_unauth_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect auth data.",
)

# Test login data
plan = UserSchema(
    username="plan",
    password=password_hasher.hash("qwerty"),
    email="plan@example.com",
)
sam = UserSchema(username="sam", password=password_hasher.hash("password"))
users_db: dict[str, UserSchema] = {plan.username: plan, sam.username: sam}


def auth_user_validate(username: str = Form(), password: str = Form()):
    if not (user := users_db.get(username)):
        raise http_unauth_exception

    if not password_validation(password=password, hash=user.password):
        raise http_unauth_exception
    elif not user.is_active:
        raise http_forbidden_exception

    return user


def get_current_payload_from_token(
    token: str = Depends(oauth_token),
) -> UserSchema:
    try:
        payload = decode_jwt(token=token)
    except InvalidTokenError:
        raise http_unauth_exception
    return payload


def get_active_user_from_payload(
    payload: dict = Depends(get_current_payload_from_token),
) -> UserSchema:
    username: str | None = payload.get("username")
    if not (user := users_db.get(username)):
        raise http_unauth_exception
    return user


def get_current_active_user(
    user: UserSchema = Depends(get_active_user_from_payload),
):
    if user.is_active:
        return user
    raise http_forbidden_exception


@router.post("/login/")
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
