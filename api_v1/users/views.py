from fastapi import APIRouter, Depends

from core.database import db_interface
from . import crud
from .schemas import UserCreate, User
from .dependencies import user_by_id


router = APIRouter(tags=["Users"])


@router.get("/", response_model=list[User])
async def get_users(session=Depends(db_interface.scoped_session_dependency)):
    return await crud.get_users(session=session)


@router.post("/", response_model=User)
async def create_user(
    user_data: UserCreate,
    session=Depends(db_interface.scoped_session_dependency),
):
    return await crud.create_user(session=session, user_data=user_data)


@router.get("/{user_id}/", response_model=User)
async def get_user(user: User = Depends(user_by_id)):
    return user
