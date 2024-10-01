from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import WorkEvent
from core.schemas.work_events import WorkEvent as WorkEventSchema
from core.schemas.work_events import WorkEventCreate, WorkEventUpdate

from .utils import update_vehicle_mileage_from_work_event


async def get_event_by_id(
    event_id: int, session: AsyncSession
) -> WorkEvent | None:
    return await session.get(WorkEvent, event_id)


async def create_work_event(
    session: AsyncSession, event_data: WorkEventCreate
) -> WorkEvent:
    event = WorkEvent(**event_data.model_dump())
    session.add(event)
    await session.commit()
    await session.refresh(event)
    await update_vehicle_mileage_from_work_event(
        work_id=event.work_id, event_mileage=event.mileage, session=session
    )

    return event


async def get_work_events_by_work_id(work_id: int, session: AsyncSession):
    statement = (
        select(WorkEvent)
        .where(WorkEvent.work_id == work_id)
        .order_by(WorkEvent.mileage)
    )
    return list(await session.scalars(statement=statement))


async def update_work_event(
    session: AsyncSession,
    event: WorkEventSchema,
    event_update: WorkEventUpdate,
) -> WorkEventSchema:
    for name, value in event_update.model_dump(exclude_unset=True).items():
        setattr(event, name, value)
    await session.commit()
    return event


async def delete_work_event(
    session: AsyncSession, event: WorkEventSchema
) -> None:
    await session.delete(event)
    await session.commit()
