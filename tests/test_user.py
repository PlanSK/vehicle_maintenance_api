from urllib import response

from httpx import AsyncClient
from pytest import FixtureDef

from core.models.user import User
from core.schemas.users import UserCreate, UserSchema

from .conftest import async_session_maker


USERS_API_URL = "/api/v1/users/"

async def test_create_user(async_conn: AsyncClient):
    user_create_json = UserCreate(
        username="test",
        first_name="Test",
        last_name="",
        email="test@example.com",
        password="qwerty",
    )
    response = await async_conn.post(
        USERS_API_URL,
        json=user_create_json.model_dump(),
    )
    assert response.status_code == 201
    reference_response: dict = response.json()
    user_instance = UserSchema(**reference_response)

    async with async_session_maker() as session:
        user_instance_from_db = await session.get(User, user_instance.id)
    for name, value in user_instance.model_dump().items():
        assert value == getattr(user_instance_from_db, name)


async def test_get_users(
    async_conn: AsyncClient, create_test_users_list: FixtureDef
):
    response = await async_conn.get(USERS_API_URL)
    assert response.status_code == 200
    result: list[dict] = response.json()
    assert len(result) == 2
    for user_dict in result:
        if user_dict.get("id") == 1:
            assert user_dict.get("username") == "test1"
        if user_dict.get("id") == 2:
            assert user_dict.get("username") == "test2"


async def test_get_user_by_username(
    async_conn: AsyncClient, create_test_users_list: FixtureDef
):
    test_available_name = "test1"
    test_unavailable_name = "unknown_name"
    response = await async_conn.get(
        USERS_API_URL + test_available_name + "/"
    )
    assert response.status_code == 200
    response = await async_conn.get(
        USERS_API_URL + test_unavailable_name + "/"
    )
    print(response.json())
    assert response.status_code == 404
