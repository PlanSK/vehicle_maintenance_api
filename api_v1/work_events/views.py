from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import db_interface
from core.schemas.work_events import (
    WorkEvent,
    WorkEventCreate,
    WorkEventUpdate,
)

from . import crud, utils

router = APIRouter(prefix="/work_events", tags=["Work Events"])


async def get_event_by_id_or_exception(
    event_id: int,
    session: AsyncSession = Depends(db_interface.scoped_session_dependency),
):
    if instance := await crud.get_event_by_id(
        event_id=event_id, session=session
    ):
        return instance
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Work event with id {event_id} not found.",
    )


@router.post(
    "/",
    response_model=WorkEvent,
    status_code=status.HTTP_201_CREATED,
)
async def create_work_event(
    event_data: WorkEventCreate,
    # user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(db_interface.scoped_session_dependency),
):
    return await crud.create_work_event(session=session, event_data=event_data)


@router.patch("/{event_id}/")
async def update_work_event(
    event_update: WorkEventUpdate,
    event: WorkEvent = Depends(get_event_by_id_or_exception),
    session: AsyncSession = Depends(db_interface.scoped_session_dependency),
):
    return await crud.update_work_event(
        session=session, event=event, event_update=event_update
    )


@router.delete("/{event_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_work_event(
    event: WorkEvent = Depends(get_event_by_id_or_exception),
    session: AsyncSession = Depends(db_interface.scoped_session_dependency),
) -> None:
    return await crud.delete_work_event(session=session, event=event)


@router.get("/by_work_id/{work_id}/")
async def get_work_events_by_work_id(
    work_id: int,
    session: AsyncSession = Depends(db_interface.scoped_session_dependency),
):
    return await crud.get_work_events_by_work_id(
        session=session, work_id=work_id
    )


@router.get("/average_interval/{work_id}/")
async def get_average_interval_km_for_event(
    work_id: int,
    session: AsyncSession = Depends(db_interface.scoped_session_dependency),
):
    events_list = await crud.get_work_events_by_work_id(
        session=session, work_id=work_id
    )
    return await utils.get_average_mileage_interval(events_list=events_list)
