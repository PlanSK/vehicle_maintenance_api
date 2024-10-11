import random

from httpx import AsyncClient

from core.database import db_handler
from core.models.user import User
from core.schemas.users import UserCreate, UserSchema

USERS_API_URL: str = "/api/v1/users"


async def test_create_user(
    async_conn: AsyncClient, user_create_model: UserCreate
):
    response = await async_conn.post(
        f"{USERS_API_URL}/",
        json=user_create_model.model_dump(),
    )
    assert response.status_code == 201
    reference_response: dict = response.json()
    user_instance = UserSchema(**reference_response)

    async for db_session in db_handler.get_db():
        async with db_session as session:
            user_instance_from_db = await session.get(User, user_instance.id)
    for name, value in user_instance.model_dump().items():
        assert value == getattr(user_instance_from_db, name)
    response = await async_conn.post(
        f"{USERS_API_URL}/",
        json=user_create_model.model_dump(),
    )
    assert response.status_code == 400


async def test_get_users(
    async_conn: AsyncClient, test_users_list_fixture: list[User]
):
    response = await async_conn.get(f"{USERS_API_URL}/")
    assert response.status_code == 200
    result: list[dict] = response.json()
    assert len(result) == len(test_users_list_fixture)
    for user in test_users_list_fixture:
        for result_user_dict in result:
            if result_user_dict.get("id") == user.id:
                assert result_user_dict.get("username") == user.username


async def test_get_user_by_username(
    async_conn: AsyncClient,
    test_users_list_fixture: list[User],
    unknown_user_test_name: str,
):
    reference_user_name = random.choice(test_users_list_fixture).username
    test_unavailable_name = unknown_user_test_name
    response = await async_conn.get(
        f"{USERS_API_URL}/username/{reference_user_name}/"
    )
    assert response.status_code == 200
    response = await async_conn.get(
        f"{USERS_API_URL}/username/{test_unavailable_name}/"
    )
    assert response.status_code == 404


async def test_get_user(
    async_conn: AsyncClient, test_users_list_fixture: list[User]
):
    reference_user_model = random.choice(test_users_list_fixture)
    response = await async_conn.get(
        f"{USERS_API_URL}/id/{reference_user_model.id}/"
    )
    assert response.status_code == 200
    for field in response.json().keys():
        assert response.json().get(field) == getattr(
            reference_user_model, field
        )
    response = await async_conn.get(f"{USERS_API_URL}/id/0/")
    assert response.status_code == 404


async def test_update_user(
    async_conn: AsyncClient,
    test_users_list_fixture: list[User],
    test_data_for_changing: dict,
):
    reference_user_model = random.choice(test_users_list_fixture)
    response = await async_conn.patch(
        f"{USERS_API_URL}/{reference_user_model.id}/",
        json=test_data_for_changing,
    )
    assert response.status_code == 200
    async for db_session in db_handler.get_db():
        async with db_session as session:
            user_instance_from_db = await session.get(
                User, reference_user_model.id
            )
    if user_instance_from_db:
        for field, value in test_data_for_changing.items():
            if value is None:
                continue
            assert getattr(user_instance_from_db, field) == value
    else:
        raise AssertionError("User instance is not in db.")


async def test_delete_user(
    async_conn: AsyncClient, test_users_list_fixture: list[User]
):
    reference_user_model = random.choice(test_users_list_fixture)
    response = await async_conn.delete(
        f"{USERS_API_URL}/{reference_user_model.id}/"
    )
    assert response.status_code == 204
    async for db_session in db_handler.get_db():
        async with db_session as session:
            user_model = await session.get(User, reference_user_model.id)
    assert user_model is None
    response = await async_conn.delete(f"{USERS_API_URL}/0/")
    assert response.status_code == 404
