import random
from typing import AsyncGenerator

import pytest
from asgi_lifespan import LifespanManager
from faker import Faker
from httpx import ASGITransport, AsyncClient

from api_v1.auth.validate import get_current_active_user
from core.database import db_handler
from core.models import BaseDbModel
from core.models.user import User
from core.models.vehicle import Vehicle
from core.models.workpattern import WorkPattern
from core.models.works import Work, WorkType
from core.schemas.users import UserSchema
from main import app

fake = Faker()


@pytest.fixture(autouse=True, scope="function")
async def prepare_db():
    async with db_handler.engine.begin() as conn:
        await conn.run_sync(BaseDbModel.metadata.create_all)
    async with LifespanManager(app):
        yield
    async with db_handler.engine.begin() as conn:
        await conn.run_sync(BaseDbModel.metadata.drop_all)


@pytest.fixture(scope="session")
async def async_conn() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost"
    ) as async_conn:
        yield async_conn


async def get_random_user_model(id: int = random.randint(1, 100)) -> User:
    return User(
        id=id,
        username=fake.user_name(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.email(),
        password=fake.password(),
        is_active=True,
    )


@pytest.fixture(scope="function")
async def users_list() -> list[User]:
    number_of_users = random.randint(1, 5)
    test_users_list = [
        await get_random_user_model(id) for id in range(1, number_of_users + 1)
    ]
    return test_users_list


@pytest.fixture(scope="function")
async def random_user_from_list(users_list: list[User]) -> User:
    return random.choice(users_list)


@pytest.fixture(scope="function")
async def vehicle_test_models_list(users_list: list[User]) -> list[Vehicle]:
    users_id_list = [user.id for user in users_list]
    test_users_list = [
        Vehicle(
            id=vehicle_id,
            vin_code=fake.vin(),
            vehicle_manufacturer=fake.name(),
            vehicle_model=fake.random_letter(),
            vehicle_body="",
            vehicle_year=random.randint(2000, 2023),
            vehicle_mileage=random.randint(1000, 100000),
            vehicle_last_update_date=fake.date_object(),
            owner_id=id,
        )
        for vehicle_id, id in enumerate(users_id_list, start=1)
    ]

    return test_users_list


@pytest.fixture(scope="function")
async def random_vehicle_from_list(
    vehicle_test_models_list: list[Vehicle],
) -> Vehicle:
    return random.choice(vehicle_test_models_list)


@pytest.fixture(scope="function")
async def add_users_to_db(users_list: list[User]) -> None:
    async for db_session in db_handler.get_db():
        async with db_session as session:
            session.add_all(users_list)
            await session.commit()


@pytest.fixture(scope="function")
async def vehicles_add_to_db(
    vehicle_test_models_list, add_users_to_db
) -> None:
    async for db_session in db_handler.get_db():
        async with db_session as session:
            session.add_all(vehicle_test_models_list)
            await session.commit()


@pytest.fixture(scope="function")
async def works_test_list(
    vehicle_test_models_list: list[Vehicle],
) -> list[Work]:
    works_list = []
    id = 1
    for vehicle in vehicle_test_models_list:
        for _ in range(1, random.randint(2, 10)):
            works_list.append(
                Work(
                    id=id,
                    title=fake.text(max_nb_chars=80),
                    interval_month=random.randint(1, 12),
                    interval_km=random.randint(1000, 100000),
                    work_type=WorkType.MAINTENANCE,
                    note=random.choice([fake.text(max_nb_chars=20), ""]),
                    vehicle_id=vehicle.id,
                )
            )
            id += 1
    return works_list


@pytest.fixture(scope="function")
async def works_add_to_db(
    vehicles_add_to_db, works_test_list: list[Work]
) -> None:
    async for db_session in db_handler.get_db():
        async with db_session as session:
            session.add_all(works_test_list)
            await session.commit()


@pytest.fixture(scope="function")
async def random_work_model(works_test_list) -> Work:
    return random.choice(works_test_list)


@pytest.fixture(scope="function")
async def workpattern_model_list() -> list[WorkPattern]:
    number_of_models = random.randint(1, 10)
    models_list = [
        WorkPattern(
            id=id,
            title=fake.text(max_nb_chars=80),
            interval_month=random.randint(1, 12),
            interval_km=random.randint(1000, 100000),
        )
        for id in range(1, number_of_models + 1)
    ]
    return models_list


@pytest.fixture(scope="function")
async def add_workpattern_to_db(workpattern_model_list: list[WorkPattern]):
    async for db_session in db_handler.get_db():
        async with db_session as session:
            session.add_all(workpattern_model_list)
            await session.commit()


async def override_get_current_active_user() -> UserSchema:
    user_model = await get_random_user_model()
    return UserSchema.model_validate(user_model)


app.dependency_overrides[get_current_active_user] = (
    override_get_current_active_user
)
