import datetime
import json
import random

import pytest
from httpx import AsyncClient
from pydantic import field_serializer

from core.database import db_handler
from core.models.user import User
from core.models.vehicle import Vehicle
from core.schemas.vehicles import VehicleCreate, VehicleSchema, VehicleUpdate

from .conftest import fake

VEHICLES_API_URL: str = "/api/v1/vehicle"


@pytest.fixture(scope="function")
async def vehicle_create_dict() -> dict:
    return json.loads(VehicleCreate(
        vin_code=fake.vin(),
        vehicle_manufacturer=fake.name(),
        vehicle_model=fake.random_letter(),
        vehicle_body="",
        vehicle_year=random.randint(2000, 2023),
        vehicle_mileage=random.randint(1000, 100000),
        vehicle_last_update_date=fake.date_object(),
    ).model_dump_json())


@pytest.fixture(scope="function")
async def vehicle_data_for_changing() -> dict:
    return VehicleUpdate(
        vin_code=random.choice([None, fake.vin()]),
        vehicle_manufacturer=random.choice([None, fake.name()]),
        vehicle_model=random.choice([None, fake.last_name()]),
        vehicle_body=random.choice([None, str(fake.random_letters(2))]),
        vehicle_year=random.choice([None, int(fake.year())]),
        vehicle_mileage=random.choice([None, random.randint(1, 999999)]),
    ).model_dump()


async def test_create_vehicle(vehicle_create_dict, async_conn: AsyncClient):
    response = await async_conn.post(
        f"{VEHICLES_API_URL}/", json=vehicle_create_dict
    )
    assert response.status_code == 201
    vehicle_from_response = VehicleSchema(**response.json())
    async for db_session in db_handler.get_db():
        async with db_session as session:
            vehicle_from_db = await session.get(
                Vehicle, vehicle_from_response.id
            )
    assert (
        VehicleSchema.model_validate(vehicle_from_db) == vehicle_from_response
    )


async def test_create_duplicated_vehicle(
    random_vehicle_from_list: Vehicle,
    vehicles_add_to_db,
    async_conn: AsyncClient,
):
    create_schema = VehicleCreate.model_validate(
        random_vehicle_from_list, from_attributes=True
    )
    response = await async_conn.post(
        f"{VEHICLES_API_URL}/",
        json=json.loads(create_schema.model_dump_json()),
    )
    assert response.status_code == 400


async def test_create_blank_vehicle(async_conn: AsyncClient):
    response = await async_conn.post(
        f"{VEHICLES_API_URL}/",
        json={},
    )
    assert response.status_code == 422


async def test_get_all_vehicles(
    vehicle_test_models_list, vehicles_add_to_db, async_conn: AsyncClient
):
    response = await async_conn.get(f"{VEHICLES_API_URL}/")
    assert response.status_code == 200
    response_reference_list = sorted(
        [
            VehicleSchema.model_validate(vehicle_schema)
            for vehicle_schema in vehicle_test_models_list
        ],
        key=lambda x: x.id,
    )
    response_schemas_list = sorted(
        [
            VehicleSchema(**vehicle_schema)
            for vehicle_schema in response.json()
        ],
        key=lambda x: x.id,
    )
    assert response_schemas_list == response_reference_list


async def test_get_all_non_existent_vehicles(async_conn: AsyncClient):
    response = await async_conn.get(f"{VEHICLES_API_URL}/")
    assert response.status_code == 200
    assert response.json() == []


async def test_get_vehicle_by_id(
    random_vehicle_from_list: Vehicle,
    vehicles_add_to_db,
    async_conn: AsyncClient,
):
    response = await async_conn.get(
        f"{VEHICLES_API_URL}/{random_vehicle_from_list.id}/"
    )
    assert response.status_code == 200
    assert VehicleSchema.model_validate(
        random_vehicle_from_list
    ) == VehicleSchema(**response.json())


async def test_get_non_existent_vehicle_by_id(
    async_conn: AsyncClient,
):
    response = await async_conn.get(
        f"{VEHICLES_API_URL}/{random.randint(1, 100)}/"
    )
    assert response.status_code == 404


async def test_get_user_vehicles(
    random_user_from_list: User,
    vehicles_add_to_db,
    async_conn: AsyncClient,
):
    response = await async_conn.get(
        f"{VEHICLES_API_URL}/by_user_id/{random_user_from_list.id}/"
    )
    assert response.status_code == 200


async def test_get_non_existent_user_vehicles(
    random_user_from_list: User, async_conn: AsyncClient
):
    response = await async_conn.get(
        f"{VEHICLES_API_URL}/by_user_id/{random_user_from_list.id}/"
    )
    assert response.status_code == 200
    assert response.json() == []


async def test_update_vehicle_partial(
    random_vehicle_from_list: Vehicle,
    vehicles_add_to_db,
    vehicle_data_for_changing,
    async_conn: AsyncClient,
):
    response = await async_conn.patch(
        f"{VEHICLES_API_URL}/{random_vehicle_from_list.id}/",
        json=vehicle_data_for_changing,
    )
    assert response.status_code == 200
    async for db_session in db_handler.get_db():
        async with db_session as session:
            vehicle_instance_from_db = await session.get(
                Vehicle, random_vehicle_from_list.id
            )
    if vehicle_instance_from_db:
        for field, value in vehicle_data_for_changing.items():
            if value is None:
                continue
            assert getattr(vehicle_instance_from_db, field) == value


async def test_update_non_existent_vehicle(
    vehicle_data_for_changing,
    async_conn: AsyncClient,
):
    response = await async_conn.patch(
        f"{VEHICLES_API_URL}/{random.randint(1, 100)}/",
        json=vehicle_data_for_changing,
    )
    assert response.status_code == 404


async def test_blank_updates_vehicle(
    random_vehicle_from_list: Vehicle,
    vehicles_add_to_db,
    async_conn: AsyncClient,
):
    response = await async_conn.patch(
        f"{VEHICLES_API_URL}/{random_vehicle_from_list.id}/",
        json={},
    )
    assert response.status_code == 200


async def test_delete_vehicle(
    random_vehicle_from_list: Vehicle,
    vehicles_add_to_db,
    async_conn: AsyncClient,
):
    response = await async_conn.delete(
        f"{VEHICLES_API_URL}/{random_vehicle_from_list.id}/"
    )
    response.status_code == 204
    async for db_session in db_handler.get_db():
        async with db_session as session:
            vehicle_from_db = await session.get(
                Vehicle, random_vehicle_from_list.id
            )
    assert vehicle_from_db is None


async def test_delete_non_existent_vehicle(
    async_conn: AsyncClient,
):
    response = await async_conn.delete(
        f"{VEHICLES_API_URL}/{random.randint(1, 100)}/"
    )
    response.status_code == 404


async def test_get_vehicle_by_vin(
    random_vehicle_from_list, vehicles_add_to_db, async_conn
):
    response = await async_conn.get(
        f"{VEHICLES_API_URL}/by_vin/{random_vehicle_from_list.vin_code}/"
    )
    assert response.status_code == 200
    assert VehicleSchema.model_validate(
        random_vehicle_from_list
    ) == VehicleSchema(**response.json())


async def test_get_unexistent_vin_vehicle(async_conn: AsyncClient):
    response = await async_conn.get(f"{VEHICLES_API_URL}/by_vin/{fake.vin()}/")
    assert response.status_code == 404
