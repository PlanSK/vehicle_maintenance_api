from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import db_handler
from core.models import WorkEvent
from core.schemas.work_events import (
    WorkEventCreate,
    WorkEventSchema,
    WorkEventUpdate,
)

from . import crud, utils
from .dependencies import get_event_by_id_or_exception

router = APIRouter(prefix="/work_events", tags=["Work Events"])


@router.post(
    "/", response_model=WorkEventSchema, status_code=status.HTTP_201_CREATED
)
async def create_work_event(
    event_data: WorkEventCreate,
    # user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(db_handler.get_db),
):
    return await crud.create_work_event(session=session, event_data=event_data)


@router.patch("/{event_id}/")
async def update_work_event(
    event_update: WorkEventUpdate,
    event: WorkEventSchema = Depends(get_event_by_id_or_exception),
    session: AsyncSession = Depends(db_handler.get_db),
):
    return await crud.update_work_event(
        session=session, event=event, event_update=event_update
    )


@router.delete("/{event_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_work_event(
    event: WorkEventSchema = Depends(get_event_by_id_or_exception),
    session: AsyncSession = Depends(db_handler.get_db),
) -> None:
    return await crud.delete_work_event(session=session, event=event)


@router.get("/{event_id}/")
async def get_work_event_by_id(
    work_event: WorkEventSchema = Depends(get_event_by_id_or_exception),
):
    return work_event


@router.get("/by_work_id/{work_id}/")
async def get_work_events_by_work_id(
    work_id: int,
    session: AsyncSession = Depends(db_handler.get_db),
):
    return await crud.get_work_events_by_work_id(
        session=session, work_id=work_id
    )


@router.get("/average_interval/{work_id}/")
async def get_average_interval_km_for_event(
    work_id: int,
    session: AsyncSession = Depends(db_handler.get_db),
):
    events_list: list[WorkEvent] = await crud.get_work_events_by_work_id(
        session=session, work_id=work_id
    )
    return await utils.get_average_mileage_interval(events_list=events_list)
