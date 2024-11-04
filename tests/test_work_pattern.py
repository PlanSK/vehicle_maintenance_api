import random

import pytest
from httpx import AsyncClient

from core.database import db_handler
from core.models.workpattern import WorkPattern
from core.schemas.workpattern import WorkPatternBase, WorkPatternSchema

from .conftest import fake


@pytest.fixture(scope="function")
async def workpattern_create_dict() -> dict:
    return WorkPatternBase(
        title=fake.text(max_nb_chars=80),
        interval_month=random.randint(1, 12),
        interval_km=random.randint(1000, 100000),
    ).model_dump()


VEHICLES_API_URL: str = "/api/v1/workpatterns"


async def test_create_workpattern(
    workpattern_create_dict, async_conn: AsyncClient
):
    response = await async_conn.post(
        f"{VEHICLES_API_URL}/", json=workpattern_create_dict
    )
    assert response.status_code == 201
    workpattern_from_response = WorkPatternSchema(**response.json())
    async for db_session in db_handler.get_db():
        async with db_session as session:
            vehicle_from_db = await session.get(
                WorkPattern, workpattern_from_response.id
            )
    assert (
        WorkPatternSchema.model_validate(vehicle_from_db)
        == workpattern_from_response
    )


async def test_create_blank_workpattern(async_conn: AsyncClient):
    response = await async_conn.post(f"{VEHICLES_API_URL}/", json={})
    assert response.status_code == 422


async def test_get_all_workpatterns(
    workpattern_model_list: list[WorkPattern],
    add_workpattern_to_db,
    async_conn: AsyncClient,
):
    response = await async_conn.get(f"{VEHICLES_API_URL}/")
    assert response.status_code == 200
    response_reference_list = sorted(
        [
            WorkPatternSchema.model_validate(workpattern_schema)
            for workpattern_schema in workpattern_model_list
        ],
        key=lambda x: x.id,
    )
    response_schemas_list = sorted(
        [
            WorkPatternSchema(**workpattern_dict)
            for workpattern_dict in response.json()
        ],
        key=lambda x: x.id,
    )
    assert response_schemas_list == response_reference_list


# async def test_get_workpattern_by_id(async_conn: AsyncClient):
#     response = await async_conn.get(f"{VEHICLES_API_URL}/")
#     assert response.status_code == 200


# async def test_get_non_existent_workpattern_by_id(async_conn: AsyncClient):
#     response = await async_conn.get(f"{VEHICLES_API_URL}/")
#     assert response.status_code == 404


async def test_update_workpattern():
    pass


async def test_delete_workpattern():
    pass
