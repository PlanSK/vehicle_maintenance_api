from sqlalchemy import Result, desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.vehicles.crud import update_vehicle_mileage_from_event
from core.models import Event
from core.schemas.events import Event as EventSchema
from core.schemas.events import EventCreate, EventUpdate


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


# Events CRUD
async def get_event_by_id(
    event_id: int, session: AsyncSession
) -> Event | None:
    return await session.get(Event, event_id)


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


async def get_vehicle_events_by_work_id(
    vehicle_id: int, work_id: int, session: AsyncSession
):
    statement = (
        select(Event)
        .where((Event.vehicle_id == vehicle_id) & (Event.work_id == work_id))
        .order_by(Event.mileage)
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


async def get_events_for_vehicle_by_type(
    session: AsyncSession, vehicle_id: int, work_id: int
):
    statement = select(Event).where(
        (Event.vehicle_id == vehicle_id) & (Event.work_id == work_id)
    )
    result = await session.scalars(statement)
    return list(result)
