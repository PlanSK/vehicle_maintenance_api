from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.password_operators import password_hasher
from core.models import User
from core.schemas.users import (
    UserCreate,
    UserSchema,
    UserUpdate,
    UserUpdatePart,
)


async def get_users(session: AsyncSession) -> list[User]:
    statement = select(User).order_by(User.id)
    result: Result = await session.execute(statement)
    users_list: list = list(result.scalars().all())
    return users_list


async def get_user(session: AsyncSession, user_id: int) -> User | None:
    return await session.get(User, user_id)


async def create_user(session: AsyncSession, user_data: UserCreate) -> User:
    user_data_dict = user_data.model_dump()
    unhased_password = user_data_dict.pop("password")
    user_data_dict.update(password=password_hasher.hash(unhased_password))
    user = User(**user_data_dict)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def update_user(
    session: AsyncSession,
    user: UserSchema,
    user_update: UserUpdate | UserUpdatePart,
    partial: bool = False,
) -> UserSchema:
    for name, value in user_update.model_dump(exclude_unset=partial).items():
        setattr(user, name, value)
    await session.commit()
    return user


async def delete_user(session: AsyncSession, user: UserSchema) -> None:
    await session.delete(user)
    await session.commit()


async def get_user_by_username(
    session: AsyncSession, username: str
) -> User | None:
    statement = select(User).where(User.username == username)
    result: Result = await session.execute(statement)
    return result.scalar_one_or_none()
