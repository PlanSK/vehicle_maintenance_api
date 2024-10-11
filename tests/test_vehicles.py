from httpx import AsyncClient

from core.database import db_handler
from core.models.vehicle import Vehicle
from core.schemas.vehicles import VehicleSchema

VEHICLES_API_URL: str = "/api/v1/vehicle"


async def test_create_vehicle(vehicle_create_model, async_conn: AsyncClient):
    response = await async_conn.post(
        f"{VEHICLES_API_URL}/", json=vehicle_create_model.model_dump()
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
