from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import db_interface
from core.schemas.users import (
    UserCreate,
    UserSchema,
    UserUpdate,
    UserUpdatePart,
)

from . import crud
from .utils import user_by_id

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserSchema])
async def get_users(
    session: AsyncSession = Depends(db_interface.scoped_session_dependency),
):
    return await crud.get_users(session=session)


@router.post(
    "/", response_model=UserSchema, status_code=status.HTTP_201_CREATED
)
async def create_user(
    user_data: UserCreate,
    session: AsyncSession = Depends(db_interface.scoped_session_dependency),
):
    return await crud.create_user(session=session, user_data=user_data)


@router.get("/{username}/")
async def get_user_by_username(
    username: str,
    session: AsyncSession = Depends(db_interface.scoped_session_dependency),
):
    return await crud.get_user_by_username(session=session, username=username)


@router.get("/{user_id}/", response_model=UserSchema)
async def get_user(user: UserSchema = Depends(user_by_id)):
    return user


@router.put("/{user_id}/")
async def update_user(
    user_update: UserUpdate,
    user: UserSchema = Depends(user_by_id),
    session: AsyncSession = Depends(db_interface.scoped_session_dependency),
):
    return await crud.update_user(
        session=session, user=user, user_update=user_update
    )


@router.patch("/{user_id}/")
async def update_user_partial(
    user_update: UserUpdatePart,
    user: UserSchema = Depends(user_by_id),
    session: AsyncSession = Depends(db_interface.scoped_session_dependency),
):
    return await crud.update_user(
        session=session, user=user, user_update=user_update, partial=True
    )


@router.delete("/{user_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user: UserSchema = Depends(user_by_id),
    session: AsyncSession = Depends(db_interface.scoped_session_dependency),
) -> None:
    return await crud.delete_user(session=session, user=user)
