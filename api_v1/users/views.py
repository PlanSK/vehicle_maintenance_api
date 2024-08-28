from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import db_interface

from . import crud
from .dependencies import user_by_id
from .schemas import User, UserCreate, UserUpdate, UserUpdatePart

router = APIRouter(tags=["Users"])


@router.get("/", response_model=list[User])
async def get_users(
    session: AsyncSession = Depends(db_interface.scoped_session_dependency),
):
    return await crud.get_users(session=session)


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    session: AsyncSession = Depends(db_interface.scoped_session_dependency),
):
    return await crud.create_user(session=session, user_data=user_data)


@router.get("/{user_id}/", response_model=User)
async def get_user(user: User = Depends(user_by_id)):
    return user


@router.put("/{user_id}/")
async def update_user(
    user_update: UserUpdate,
    user: User = Depends(user_by_id),
    session: AsyncSession = Depends(db_interface.scoped_session_dependency),
):
    return await crud.update_user(
        session=session, user=user, user_update=user_update
    )


@router.patch("/{user_id}/")
async def update_user_partial(
    user_update: UserUpdatePart,
    user: User = Depends(user_by_id),
    session: AsyncSession = Depends(db_interface.scoped_session_dependency),
):
    return await crud.update_user(
        session=session, user=user, user_update=user_update, partial=True
    )


@router.delete("/{user_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user: User = Depends(user_by_id),
    session: AsyncSession = Depends(db_interface.scoped_session_dependency),
) -> None:
    return await crud.delete_user(session=session, user=user)
