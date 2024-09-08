from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.vehicle import Vehicle
from core.schemas.vehicles import Vehicle as VehicleSchema
from core.schemas.vehicles import VehicleCreate, VehicleUpdate
from core.vin import VIN_Type


async def create_vehicle(
    session: AsyncSession, vehicle_data: VehicleCreate, owner_id: int
) -> Vehicle:
    vehicle_data_dump = vehicle_data.model_dump()
    vehicle_data_dump.update(owner_id=owner_id)
    vehicle = Vehicle(**vehicle_data_dump)
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


async def update_vehicle_mileage_from_event(
    session: AsyncSession, vehicle_id: int, event_mileage: int
) -> None:
    vehicle_instance = await get_vehicle_by_id(
        vehicle_id=vehicle_id, session=session
    )
    if vehicle_instance and vehicle_instance.vehicle_mileage < event_mileage:
        vehicle_instance.vehicle_mileage = event_mileage
        await session.commit()
