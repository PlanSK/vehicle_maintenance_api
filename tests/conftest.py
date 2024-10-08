from typing import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from core.database import db_interface
from core.models import BaseDbModel
from core.models.user import User
from main import app

TEST_DB_URL = "sqlite+aiosqlite:///testdb.sqlite3"

engine_test = create_async_engine(url=TEST_DB_URL, echo=False)
async_session_maker = async_sessionmaker(
    bind=engine_test, autoflush=False, autocommit=False, expire_on_commit=False
)


async def override_session_dependency() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[db_interface.scoped_session_dependency] = (
    override_session_dependency
)


@pytest.fixture(autouse=True, scope="function")
async def prepare_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(BaseDbModel.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(BaseDbModel.metadata.drop_all)


@pytest.fixture(scope="session")
async def async_conn() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost"  # type: ignore
    ) as async_conn:
        yield async_conn


@pytest.fixture(scope="function")
async def create_test_users_list():
    async with async_session_maker() as session:
        session.add_all(
            [
                User(
                    id=1,
                    username="test1",
                    first_name="Test1",
                    last_name="",
                    email="test1@example.com",
                    password="qwerty",
                    is_active=True,
                ),
                User(
                    id=2,
                    username="test2",
                    first_name="Test2",
                    last_name="",
                    email="test2@example.com",
                    password="qwerty",
                    is_active=True,
                ),
            ]
        )
        await session.commit()
