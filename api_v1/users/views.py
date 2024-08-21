from fastapi import APIRouter, HTTPException, status, Depends

from core.database import db_interface
from . import crud
from .schemas import UserCreate, User

router = APIRouter(tags=["Users"])


@router.get("/", response_model=list[User])
async def get_users(session=Depends(db_interface.scoped_session_dependency)):
    return await crud.get_users(session=session)


@router.post("/", response_model=User)
async def user_create(
    user_data: UserCreate,
    session=Depends(db_interface.scoped_session_dependency),
):
    return await crud.user_create(session=session, user_data=user_data)


@router.get("/{user_id}/", response_model=User)
async def get_user(
    user_id: int, session=Depends(db_interface.scoped_session_dependency)
):
    user = await crud.get_user(user_id=user_id, session=session)
    if user is not None:
        return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with id {user_id} not found.",
    )
