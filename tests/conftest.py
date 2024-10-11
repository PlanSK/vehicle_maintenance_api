import datetime
import random
from typing import AsyncGenerator

import pytest
from asgi_lifespan import LifespanManager
from faker import Faker
from httpx import ASGITransport, AsyncClient
from pydantic import field_serializer

from api_v1.auth.validate import get_current_active_user
from core.database import db_handler
from core.models import BaseDbModel
from core.models.user import User
from core.schemas.users import UserSchema
from core.schemas.vehicles import VehicleCreate
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


class TestVehicleCreate(VehicleCreate):
    @field_serializer("vehicle_last_update_date")
    def serialize_date(self, vehicle_last_update_date: datetime.date):
        return str(vehicle_last_update_date)


@pytest.fixture(scope="function")
async def vehicle_create_model() -> TestVehicleCreate:
    return TestVehicleCreate(
        vin_code=fake.vin(),
        vehicle_manufacturer=fake.name(),
        vehicle_model=fake.random_letter(),
        vehicle_body="",
        vehicle_year=random.randint(2000, 2023),
        vehicle_mileage=random.randint(1000, 100000),
        vehicle_last_update_date=fake.date_object(),
    )


async def override_get_current_active_user() -> UserSchema:
    return UserSchema(
        id=random.randint(1, 100),
        username=fake.user_name(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.email(),
        password=fake.password(),
        is_active=True,
    )


app.dependency_overrides[get_current_active_user] = (
    override_get_current_active_user
)
