import datetime
import secrets
import uuid
from typing import Annotated

from fastapi import (
    APIRouter,
    Cookie,
    Depends,
    Header,
    HTTPException,
    Response,
    status,
)
from fastapi.security import HTTPBasic, HTTPBasicCredentials

router = APIRouter(prefix="/auth", tags=["Auth"])

security = HTTPBasic()


users_dict = {"admin": "admin"}


@router.get("/basic-auth/")
def basic_auth_credentials(
    credencials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    return {
        "message": "Hi!",
        "username": credencials.username,
        "password": credencials.password,
    }


def get_auth_user_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
) -> str:
    unauth_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password.",
        headers={"WWW-Authenticate": "Basic"},
    )
    correct_password = users_dict.get(credentials.username)
    if correct_password is None:
        raise unauth_exception

    if not secrets.compare_digest(credentials.password, correct_password):
        raise unauth_exception
    return credentials.username


@router.get("/basic-auth-username/")
def basic_auth_username(auth_username: str = Depends(get_auth_user_username)):
    return {
        "message": f"Hi, {auth_username}",
        "username": auth_username,
    }


static_auth_tokens = {
    "ffcb46aac55299e193cdef5bab3d7c0f": "admin",
    "43454e2365d55563905749648a76eb9d": "john",
}


def get_username_by_static_auth_token(
    static_token: str = Header(alias="x-static-auth-token"),
) -> str:
    if token := static_auth_tokens.get(static_token):
        return token
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token."
    )


@router.get("/some-http-header-auth/")
def some_http_header_auth(
    header_username: str = Depends(get_username_by_static_auth_token),
):
    return {
        "message": f"Hi, {header_username}",
        "username": header_username,
    }


COOKIES: dict = {}
COOKIE_SESSION_ID_KEY = "web-app-session-id"


def generate_session_id() -> str:
    return uuid.uuid4().hex


@router.get("/login-cookie/")
def auth_login_set_cookie(
    response: Response, auth_username: str = Depends(get_auth_user_username)
):
    session_id = generate_session_id()
    COOKIES[session_id] = {
        "username": auth_username,
        "login_at": int(datetime.datetime.now().timestamp()),
    }
    response.set_cookie(COOKIE_SESSION_ID_KEY, session_id)
    return {"result": "ok"}


def get_session_data(session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY)):
    if session_id not in COOKIES:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated.",
        )
    return COOKIES[session_id]


@router.get("/check-cookie/")
def auth_login_check_cookie(
    user_session_data: dict = Depends(get_session_data),
):
    username = user_session_data.get("username")
    return {"message": f"Hello, {username}!", **user_session_data}


@router.get("/logout-cookie/")
def auth_logout_cookie(
    response: Response,
    session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY),
    user_session_data: dict = Depends(get_session_data),
):
    COOKIES.pop(session_id)
    response.delete_cookie(COOKIE_SESSION_ID_KEY)
    username = user_session_data.get("username")
    return {"message": f"Bye bye, {username}!", **user_session_data}
