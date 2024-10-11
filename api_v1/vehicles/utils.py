from sqlalchemy.ext.asyncio import AsyncSession

from . import crud


async def update_vehicle_mileage_from_event(
    session: AsyncSession, vehicle_id: int, event_mileage: int
) -> None:
    vehicle_instance = await crud.get_vehicle_by_id(
        vehicle_id=vehicle_id, session=session
    )
    if vehicle_instance and vehicle_instance.vehicle_mileage < event_mileage:
        vehicle_instance.vehicle_mileage = event_mileage
        await session.commit()
