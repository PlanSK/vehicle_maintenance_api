from sqlalchemy import Result, desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.vehicles.crud import update_vehicle_mileage_from_event
from core.models import Event
from core.schemas.events import Event as EventSchema
from core.schemas.events import EventCreate, EventUpdate


async def get_event_by_id(
    event_id: int, session: AsyncSession
) -> Event | None:
    return await session.get(Event, event_id)


async def create_event(
    session: AsyncSession, event_data: EventCreate
) -> Event:
    event = Event(**event_data.model_dump())
    session.add(event)
    await session.commit()
    await session.refresh(event)

    # await update_vehicle_mileage_from_event(
    #     session=session,
    #     vehicle_id=event.vehicle_id,
    #     event_mileage=event.mileage,
    # )
    return event


async def get_events_by_work_id(work_id: int, session: AsyncSession):
    statement = (
        select(Event).where(Event.work_id == work_id).order_by(Event.mileage)
    )
    return list(await session.scalars(statement=statement))


async def update_event(
    session: AsyncSession, event: EventSchema, event_update: EventUpdate
) -> EventSchema:
    for name, value in event_update.model_dump(exclude_unset=True).items():
        setattr(event, name, value)
    await session.commit()
    return event


async def delete_event(session: AsyncSession, event: EventSchema) -> None:
    await session.delete(event)
    await session.commit()
