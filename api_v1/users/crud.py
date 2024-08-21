"""
Create
Read
Update
Delete
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Result, select
from typing import Coroutine, Any

from core.models import User

from .schemas import UserCreate


async def get_users(session: AsyncSession) -> list[User]:
    statement = select(User).order_by(User.id)
    result: Result = await session.execute(statement)
    users_list: list = list(result.scalars().all())
    return users_list


async def get_user(
    session: AsyncSession, user_id: int
) -> User | None:
    return await session.get(User, user_id)


async def user_create(session: AsyncSession, user_data: UserCreate) -> User:
    user = User(**user_data.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
