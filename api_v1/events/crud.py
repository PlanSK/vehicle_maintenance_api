from sqlalchemy import Result, desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.vehicles.crud import update_vehicle_mileage_from_event
from core.models.events import Event, MileageEvent
from core.schemas.events import Event as EventSchema
from core.schemas.events import EventCreate, EventUpdate
from core.schemas.events import MileageEvent as MileageEventSchema
from core.schemas.events import MileageEventCreate, MileageEventUpdate


async def _get_objects_list_from_statement(
    model, vehicle_id: int, session: AsyncSession, order_by_argument: str
) -> list:
    statement = (
        select(model)
        .where(model.vehicle_id == vehicle_id)
        .order_by(desc(getattr(model, order_by_argument)))
    )
    result: Result = await session.execute(statement)
    events_list: list = list(result.scalars().all())
    return events_list


async def _add_element_to_db(element, session: AsyncSession) -> None:
    session.add(element)
    await session.commit()
    await session.refresh(element)


async def get_event_by_id(
    event_id: int, session: AsyncSession
) -> Event | None:
    return await session.get(Event, event_id)


async def get_mileage_event_by_id(
    event_id: int, session: AsyncSession
) -> MileageEvent | None:
    return await session.get(MileageEvent, event_id)


async def create_event(
    session: AsyncSession, event_data: EventCreate
) -> Event:
    event = Event(**event_data.model_dump())
    await _add_element_to_db(element=event, session=session)
    await update_vehicle_mileage_from_event(
        session=session,
        vehicle_id=event.vehicle_id,
        event_mileage=event.mileage,
    )
    return event


async def get_vehicle_events(
    vehicle_id: int, session: AsyncSession
) -> list[Event]:
    events_list = await _get_objects_list_from_statement(
        model=Event,
        vehicle_id=vehicle_id,
        session=session,
        order_by_argument="work_date",
    )
    return events_list


async def create_mileage_event(
    session: AsyncSession, mileage_event_data: MileageEventCreate
) -> MileageEvent:
    mileage_event = MileageEvent(**mileage_event_data.model_dump())
    await _add_element_to_db(element=mileage_event, session=session)
    await update_vehicle_mileage_from_event(
        session=session,
        vehicle_id=mileage_event.vehicle_id,
        event_mileage=mileage_event.mileage,
    )
    return mileage_event


async def get_vehicle_mileage_events(
    vehicle_id: int, session: AsyncSession
) -> list[MileageEvent]:
    events_list = await _get_objects_list_from_statement(
        model=MileageEvent,
        vehicle_id=vehicle_id,
        session=session,
        order_by_argument="mileage_date",
    )
    return events_list


async def update_event(
    session: AsyncSession, event: EventSchema, event_update: EventUpdate
) -> EventSchema:
    for name, value in event_update.model_dump(exclude_unset=True).items():
        setattr(event, name, value)
    await session.commit()
    return event


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


async def delete_event(session: AsyncSession, event: EventSchema) -> None:
    await session.delete(event)
    await session.commit()


async def delete_mileage_event(
    session: AsyncSession, event: MileageEventSchema
) -> None:
    await session.delete(event)
    await session.commit()


async def get_events_for_vehicle_by_type(
    session: AsyncSession, vehicle_id: int, work_id: int
):
    statement = select(Event).where(
        (Event.vehicle_id == vehicle_id) & (Event.work_id == work_id)
    )
    result = await session.scalars(statement)
    return list(result)
