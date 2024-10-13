from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.works.utils import create_works_on_create_vehicle
from core.models import Vehicle
from core.schemas.vehicles import VehicleCreate, VehicleSchema, VehicleUpdate
from core.vin import VIN_Type


async def create_vehicle(
    session: AsyncSession, vehicle_data: VehicleCreate, owner_id: int
) -> Vehicle:
    vehicle_data_dump: dict = vehicle_data.model_dump()
    vin_code: str = vehicle_data_dump.get("vin_code", "")
    vehicle_data_dump.update(owner_id=owner_id, vin_code=vin_code.upper())
    vehicle_instance = Vehicle(**vehicle_data_dump)

    session.add(vehicle_instance)
    await session.commit()
    await session.refresh(vehicle_instance)
    await create_works_on_create_vehicle(
        vehicle_id=vehicle_instance.id, session=session
    )
    return vehicle_instance


async def get_all_vehicles(session: AsyncSession) -> list[Vehicle]:
    statement = select(Vehicle).order_by(Vehicle.id)
    result: Result = await session.execute(statement)
    vehicles_list: list = list(result.scalars().all())
    return vehicles_list


async def get_user_vehicles(
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


async def update_vehicle(
    session: AsyncSession,
    vehicle: VehicleSchema,
    vehicle_update: VehicleUpdate,
) -> VehicleSchema:
    for name, value in vehicle_update.model_dump(exclude_unset=True).items():
        setattr(vehicle, name, value)
    await session.commit()
    return vehicle


async def delete_vehicle(
    session: AsyncSession, vehicle: VehicleSchema
) -> None:
    await session.delete(vehicle)
    await session.commit()


async def get_vehicle_by_vin(session: AsyncSession, vin: VIN_Type):
    statement = select(Vehicle).where(Vehicle.vin_code == vin)
    return await session.scalar(statement)
