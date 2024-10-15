import json
import random

import pytest
from httpx import AsyncClient

from core.database import db_handler
from core.models.vehicle import Vehicle
from core.models.works import Work, WorkType
from core.schemas.works import WorkBase, WorkSchema, WorkUpdate

from .conftest import fake

WORKS_API_URL = "/api/v1/works"


@pytest.fixture(scope="function")
async def work_create_dict() -> dict:
    return json.loads(
        WorkBase(
            title=fake.text(max_nb_chars=80),
            interval_month=random.randint(1, 12),
            interval_km=random.randint(1000, 100000),
            work_type=WorkType.MAINTENANCE,
            note=random.choice([fake.text(max_nb_chars=20), ""]),
            vehicle_id=random.randint(1, 100),
        ).model_dump_json()
    )


@pytest.fixture(scope="function")
async def work_data_for_changing() -> dict:
    return json.loads(
        WorkUpdate(
            title=random.choice([fake.text(max_nb_chars=80), None]),
            interval_month=random.choice([random.randint(1, 12), None]),
            interval_km=random.choice([random.randint(1000, 100000), None]),
            work_type=random.choice(
                [WorkType.MAINTENANCE, WorkType.TUNING, WorkType.REPAIR, None]
            ),
            note=random.choice([fake.text(max_nb_chars=20), None]),
        ).model_dump_json()
    )


async def test_create_work(work_create_dict, async_conn: AsyncClient):
    response = await async_conn.post(
        f"{WORKS_API_URL}/",
        json=work_create_dict,
    )
    assert response.status_code == 201
    work_from_responce = WorkSchema(**response.json())

    async for db_session in db_handler.get_db():
        async with db_session as session:
            work_from_db = await session.get(Work, work_from_responce.id)
    assert WorkSchema.model_validate(work_from_db) == work_from_responce


async def test_create_blank_work(async_conn: AsyncClient):
    response = await async_conn.post(
        f"{WORKS_API_URL}/",
        json={},
    )
    assert response.status_code == 422


async def test_get_work_by_id(
    random_work_model: Work, works_add_to_db, async_conn: AsyncClient
):
    response = await async_conn.get(
        f"{WORKS_API_URL}/{random_work_model.id}/",
    )
    assert response.status_code == 200
    async for db_session in db_handler.get_db():
        async with db_session as session:
            work_from_db = await session.get(Work, random_work_model.id)
    assert WorkSchema.model_validate(
        work_from_db
    ) == WorkSchema.model_validate(random_work_model)


async def test_get_non_existent_work_by_id(async_conn: AsyncClient):
    response = await async_conn.get(
        f"{WORKS_API_URL}/{random.randint(1,100)}/",
    )
    assert response.status_code == 404


async def test_get_works_by_vehicle_id(
    random_vehicle_from_list: Vehicle,
    works_test_list,
    works_add_to_db,
    async_conn: AsyncClient,
):
    response = await async_conn.get(
        f"{WORKS_API_URL}/vehicle_id/{random_vehicle_from_list.id}/",
    )
    assert response.status_code == 200
    works_model_by_vehicle_id_list = sorted(
        [
            work
            for work in works_test_list
            if work.vehicle_id == random_vehicle_from_list.id
        ],
        key=lambda x: x.id,
    )
    sorted_works_list = [
        json.loads(WorkSchema.model_validate(work).model_dump_json())
        for work in works_model_by_vehicle_id_list
    ]
    assert response.json() == sorted_works_list


async def test_get_non_existent_works_by_vehicle_id(async_conn: AsyncClient):
    response = await async_conn.get(
        f"{WORKS_API_URL}/vehicle_id/{random.randint(1,100)}/",
    )
    assert response.status_code == 200
    assert response.json() == []


async def test_update_work(
    random_work_model: Work,
    work_data_for_changing: dict,
    works_add_to_db,
    async_conn: AsyncClient,
):
    response = await async_conn.patch(
        f"{WORKS_API_URL}/{random_work_model.id}/", json=work_data_for_changing
    )
    assert response.status_code == 200
    async for db_session in db_handler.get_db():
        async with db_session as session:
            work_instance_from_db = await session.get(
                Work, random_work_model.id
            )
    work_schema_dict = json.loads(
        WorkSchema.model_validate(work_instance_from_db).model_dump_json()
    )
    if work_instance_from_db:
        for field, value in work_data_for_changing.items():
            if value is None:
                continue
            assert work_schema_dict.get(field) == value


async def test_blank_update_work(
    random_work_model: Work, works_add_to_db, async_conn: AsyncClient
):
    response = await async_conn.patch(
        f"{WORKS_API_URL}/{random_work_model.id}/", json={}
    )
    assert response.status_code == 200


async def test_delete_work(
    random_work_model: Work,
    works_add_to_db,
    async_conn: AsyncClient,
):
    response = await async_conn.delete(
        f"{WORKS_API_URL}/{random_work_model.id}/"
    )
    response.status_code == 204
    async for db_session in db_handler.get_db():
        async with db_session as session:
            vehicle_from_db = await session.get(Work, random_work_model.id)
    assert vehicle_from_db is None


async def test_delete_non_existent_work(async_conn: AsyncClient):
    response = await async_conn.delete(
        f"{WORKS_API_URL}/{random.randint(1, 100)}/"
    )
    response.status_code == 404
