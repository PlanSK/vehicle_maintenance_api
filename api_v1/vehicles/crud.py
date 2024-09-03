from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.vehicle import Vehicle
from core.schemas.vehicles import Vehicle as VehicleSchema
from core.schemas.vehicles import VehicleCreate


async def create_vehicle(
    session: AsyncSession, vehicle_data: VehicleCreate
) -> Vehicle:
    vehicle = Vehicle(**vehicle_data.model_dump())
    session.add(vehicle)
    await session.commit()
    await session.refresh(vehicle)
    return vehicle


async def get_all_vehicles(session: AsyncSession) -> list[Vehicle]:
    statement = select(Vehicle).order_by(Vehicle.id)
    result: Result = await session.execute(statement)
    vehicles_list: list = list(result.scalars().all())
    return vehicles_list


async def get_users_vehicles(
    user_id: int, session: AsyncSession
) -> list[Vehicle]:
    statement = (
        select(Vehicle).where(Vehicle.owner_id == user_id).order_by(Vehicle.id)
    )
    result: Result = await session.execute(statement)
    vehicles_list: list = list(result.scalars().all())
    return vehicles_list


async def get_vehicle_by_id(
    vehicle_id: int, session: AsyncSession
) -> Vehicle | None:
    return await session.get(Vehicle, vehicle_id)


async def delete_vehicle(
    session: AsyncSession, vehicle: VehicleSchema
) -> None:
    await session.delete(vehicle)
    await session.commit()
