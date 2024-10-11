import random

import pytest
from httpx import AsyncClient

from core.database import db_handler
from core.models.user import User
from core.schemas.users import UserCreate, UserSchema, UserUpdatePart

from .conftest import fake

USERS_API_URL: str = "/api/v1/users"


@pytest.fixture(scope="function")
async def users_list() -> list[User]:
    number_of_users = random.randint(1, 5)
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
    return test_users_list


@pytest.fixture(scope="function")
async def add_users_to_db(users_list: list[User]) -> None:
    async for db_session in db_handler.get_db():
        async with db_session as session:
            session.add_all(users_list)
            await session.commit()


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
    users_list: list[User], add_users_to_db, async_conn: AsyncClient
):
    existed_user = random.choice(users_list)
    create_schema = UserCreate.model_validate(
        existed_user, from_attributes=True
    )
    response = await async_conn.post(
        f"{USERS_API_URL}/",
        json=create_schema.model_dump(),
    )
    assert response.status_code == 400


async def test_get_users(
    users_list: list[User], add_users_to_db, async_conn: AsyncClient
):
    response = await async_conn.get(f"{USERS_API_URL}/")
    assert response.status_code == 200
    result: list[dict] = response.json()
    assert len(result) == len(users_list)
    for user in users_list:
        for user_dict in result:
            if user_dict.get("id") == user.id:
                assert UserSchema(**user_dict) == UserSchema.model_validate(
                    user
                )


async def test_get_user_by_username(
    users_list: list[User], add_users_to_db, async_conn: AsyncClient
):
    reference_user_name = random.choice(users_list).username
    response = await async_conn.get(
        f"{USERS_API_URL}/username/{reference_user_name}/"
    )
    assert response.status_code == 200


async def test_get_nonexistent_user_by_name(
    unknown_user_test_name: str, async_conn: AsyncClient
):
    response = await async_conn.get(
        f"{USERS_API_URL}/username/{unknown_user_test_name}/"
    )
    assert response.status_code == 404


async def test_get_user(
    users_list: list[User], add_users_to_db, async_conn: AsyncClient
):
    user_model = random.choice(users_list)
    response = await async_conn.get(f"{USERS_API_URL}/id/{user_model.id}/")
    assert response.status_code == 200
    assert UserSchema(**response.json()) == UserSchema.model_validate(
        user_model
    )


async def test_get_nonexistent_user(async_conn: AsyncClient):
    response = await async_conn.get(f"{USERS_API_URL}/id/0/")
    assert response.status_code == 404


async def test_update_user(
    users_list: list[User],
    add_users_to_db,
    user_data_for_changing: dict,
    async_conn: AsyncClient,
):
    reference_user_model = random.choice(users_list)
    response = await async_conn.patch(
        f"{USERS_API_URL}/{reference_user_model.id}/",
        json=user_data_for_changing,
    )
    assert response.status_code == 200
    async for db_session in db_handler.get_db():
        async with db_session as session:
            user_instance_from_db = await session.get(
                User, reference_user_model.id
            )
    if user_instance_from_db:
        for field, value in user_data_for_changing.items():
            if value is None:
                continue
            assert getattr(user_instance_from_db, field) == value
    else:
        raise AssertionError("User instance is not in db.")


async def test_update_nonexistent_user(
    user_data_for_changing: dict, async_conn: AsyncClient
):
    response = await async_conn.patch(
        f"{USERS_API_URL}/{random.randint(1,100)}/",
        json=user_data_for_changing,
    )
    assert response.status_code == 404


async def test_delete_user(
    users_list: list[User], add_users_to_db, async_conn: AsyncClient
):
    reference_user_model = random.choice(users_list)
    response = await async_conn.delete(
        f"{USERS_API_URL}/{reference_user_model.id}/"
    )
    assert response.status_code == 204
    async for db_session in db_handler.get_db():
        async with db_session as session:
            user_model = await session.get(User, reference_user_model.id)
    assert user_model is None


async def test_delete_nonexistent_user(async_conn: AsyncClient):
    response = await async_conn.delete(f"{USERS_API_URL}/0/")
    assert response.status_code == 404
