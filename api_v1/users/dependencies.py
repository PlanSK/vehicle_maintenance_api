import hashlib
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Path, Depends, HTTPException, status
from loguru import logger

from core.database import db_interface
from core.models import User
from core.config import settings

from . import crud


async def user_by_id(
    user_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_interface.scoped_session_dependency),
) -> User:
    user = await crud.get_user(user_id=user_id, session=session)
    if user is not None:
        return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with id {user_id} not found.",
    )


def get_password_hash(unhashed_password: str) -> str:
    if settings.secret_key == "test":
        logger.warning(
            "SECRET_KEY variable is not defined! Using test secret key."
        )
    hash = hashlib.pbkdf2_hmac(
        "sha512",
        unhashed_password.encode("utf-8"),
        settings.secret_key.encode("utf-8"),
        1024,
        32,
    )
    return hash.hex()
