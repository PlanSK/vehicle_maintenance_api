import random

import pytest
from httpx import AsyncClient

from core.database import db_handler
from core.models.user import User
from core.schemas.users import UserCreate, UserSchema, UserUpdatePart

from .conftest import fake

USERS_API_URL: str = "/api/v1/users"


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
async def user_data_for_changing() -> dict:
    return UserUpdatePart(
        username=random.choice([None, fake.user_name()]),
        first_name=random.choice([None, fake.first_name()]),
        last_name=random.choice([None, fake.last_name()]),
        email=random.choice([None, fake.email()]),
    ).model_dump()


async def test_create_user(
    user_create_model: UserCreate, async_conn: AsyncClient
):
    response = await async_conn.post(
        f"{USERS_API_URL}/",
        json=user_create_model.model_dump(),
    )
    assert response.status_code == 201
    user_from_responce = UserSchema(**response.json())

    async for db_session in db_handler.get_db():
        async with db_session as session:
            user_from_db = await session.get(User, user_from_responce.id)
    assert UserSchema.model_validate(user_from_db) == user_from_responce


async def test_create_duplicated_user(
    random_user_from_list, add_users_to_db, async_conn: AsyncClient
):
    create_schema = UserCreate.model_validate(
        random_user_from_list, from_attributes=True
    )
    response = await async_conn.post(
        f"{USERS_API_URL}/",
        json=create_schema.model_dump(),
    )
    assert response.status_code == 400


async def test_create_blank_user(async_conn: AsyncClient):
    response = await async_conn.post(
        f"{USERS_API_URL}/",
        json={},
    )
    assert response.status_code == 422


async def test_get_users(
    users_list: list[User], add_users_to_db, async_conn: AsyncClient
):
    response = await async_conn.get(f"{USERS_API_URL}/")
    assert response.status_code == 200
    response_reference_list = sorted(
        [UserSchema.model_validate(user_schema) for user_schema in users_list],
        key=lambda x: x.id,
    )
    response_schemas_list = sorted(
        [UserSchema(**user_schema) for user_schema in response.json()],
        key=lambda x: x.id,
    )
    assert response_schemas_list == response_reference_list


async def test_get_blank_users_list(async_conn: AsyncClient):
    response = await async_conn.get(f"{USERS_API_URL}/")
    assert response.status_code == 200
    assert response.json() == []


async def test_get_user_by_username(
    random_user_from_list, add_users_to_db, async_conn: AsyncClient
):
    response = await async_conn.get(
        f"{USERS_API_URL}/username/{random_user_from_list.username}/"
    )
    assert response.status_code == 200


async def test_get_nonexistent_user_by_name(async_conn: AsyncClient):
    response = await async_conn.get(
        f"{USERS_API_URL}/username/{fake.user_name()}/"
    )
    assert response.status_code == 404


async def test_get_user(
    random_user_from_list, add_users_to_db, async_conn: AsyncClient
):
    response = await async_conn.get(
        f"{USERS_API_URL}/id/{random_user_from_list.id}/"
    )
    assert response.status_code == 200
    assert UserSchema(**response.json()) == UserSchema.model_validate(
        random_user_from_list
    )


async def test_get_nonexistent_user(async_conn: AsyncClient):
    response = await async_conn.get(
        f"{USERS_API_URL}/id/{random.randint(1, 100)}/"
    )
    assert response.status_code == 404


async def test_update_user(
    random_user_from_list,
    add_users_to_db,
    user_data_for_changing: dict,
    async_conn: AsyncClient,
):
    response = await async_conn.patch(
        f"{USERS_API_URL}/{random_user_from_list.id}/",
        json=user_data_for_changing,
    )
    assert response.status_code == 200
    async for db_session in db_handler.get_db():
        async with db_session as session:
            user_instance_from_db = await session.get(
                User, random_user_from_list.id
            )
    if user_instance_from_db:
        for field, value in user_data_for_changing.items():
            if value is None:
                continue
            assert getattr(user_instance_from_db, field) == value
    else:
        raise AssertionError("User instance is not in db.")


async def test_update_non_existent_user(
    user_data_for_changing: dict, async_conn: AsyncClient
):
    response = await async_conn.patch(
        f"{USERS_API_URL}/{random.randint(1,100)}/",
        json=user_data_for_changing,
    )
    assert response.status_code == 404


async def test_blank_update_user(
    random_user_from_list,
    add_users_to_db,
    async_conn: AsyncClient,
):
    response = await async_conn.patch(
        f"{USERS_API_URL}/{random_user_from_list.id}/",
        json={},
    )
    assert response.status_code == 200


async def test_delete_user(
    random_user_from_list, add_users_to_db, async_conn: AsyncClient
):
    response = await async_conn.delete(
        f"{USERS_API_URL}/{random_user_from_list.id}/"
    )
    assert response.status_code == 204
    async for db_session in db_handler.get_db():
        async with db_session as session:
            user_model = await session.get(User, random_user_from_list.id)
    assert user_model is None


async def test_delete_nonexistent_user(async_conn: AsyncClient):
    response = await async_conn.delete(f"{USERS_API_URL}/0/")
    assert response.status_code == 404
