import random
from typing import AsyncGenerator

import pytest
from faker import Faker
from httpx import ASGITransport, AsyncClient

from core.database import db_handler
from core.models import BaseDbModel
from core.models.user import User
from core.schemas.users import UserCreate, UserUpdatePart
from main import app

fake = Faker()


@pytest.fixture(autouse=True, scope="function")
async def prepare_db():
    async with db_handler.engine.begin() as conn:
        await conn.run_sync(BaseDbModel.metadata.create_all)
    yield
    async with db_handler.engine.begin() as conn:
        await conn.run_sync(BaseDbModel.metadata.drop_all)


@pytest.fixture(scope="session")
async def async_conn() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost"
    ) as async_conn:
        yield async_conn


@pytest.fixture(scope="function")
async def test_users_list_fixture() -> list[User]:
    number_of_users = 3
    test_users_list = [
        User(
            id=id,
            username=fake.user_name(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            password=fake.password(),
            is_active=True,
        )
        for id in range(1, number_of_users + 1)
    ]
    async for db_session in db_handler.get_db():
        async with db_session as session:
            session.add_all(test_users_list)
            await session.commit()
    return test_users_list


@pytest.fixture(scope="function")
async def user_create_model() -> UserCreate:
    return UserCreate(
        username=fake.user_name(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.email(),
        password=fake.password(),
    )


@pytest.fixture(scope="function")
async def unknown_user_test_name() -> str:
    return fake.user_name()


@pytest.fixture(scope="function")
async def test_data_for_changing() -> dict:
    return UserUpdatePart(
        username=random.choice([None, fake.user_name()]),
        first_name=random.choice([None, fake.first_name()]),
        last_name=random.choice([None, fake.last_name()]),
        email=random.choice([None, fake.email()]),
    ).model_dump()
