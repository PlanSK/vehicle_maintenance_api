from sqlalchemy import Result, desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.vehicles.utils import update_vehicle_mileage_from_event
from core.models import MileageEvent
from core.schemas.mileage_events import MileageEvent as MileageEventSchema
from core.schemas.mileage_events import MileageEventCreate, MileageEventUpdate


async def get_mileage_event_by_id(
    event_id: int, session: AsyncSession
) -> MileageEvent | None:
    return await session.get(MileageEvent, event_id)


async def create_mileage_event(
    session: AsyncSession, mileage_event_data: MileageEventCreate
) -> MileageEvent:
    mileage_event = MileageEvent(**mileage_event_data.model_dump())
    session.add(mileage_event)
    await session.commit()
    await session.refresh(mileage_event)

    await update_vehicle_mileage_from_event(
        session=session,
        vehicle_id=mileage_event.vehicle_id,
        event_mileage=mileage_event.mileage,
    )
    return mileage_event


async def get_vehicle_mileage_events(
    vehicle_id: int, session: AsyncSession
) -> list[MileageEvent]:
    statement = (
        select(MileageEvent)
        .where(MileageEvent.vehicle_id == vehicle_id)
        .order_by(desc(getattr(MileageEvent, "mileage_date")))
    )
    result: Result = await session.execute(statement)
    mileage_events_list: list = list(result.scalars().all())

    return mileage_events_list


async def update_mileage_event(
    session: AsyncSession,
    mileage_event: MileageEventSchema,
    mileage_event_update: MileageEventUpdate,
) -> MileageEventSchema:
    for name, value in mileage_event_update.model_dump(
        exclude_unset=True
    ).items():
        setattr(mileage_event, name, value)
    await session.commit()
    return mileage_event


async def delete_mileage_event(
    session: AsyncSession, mileage_event: MileageEventSchema
) -> None:
    await session.delete(mileage_event)
    await session.commit()
