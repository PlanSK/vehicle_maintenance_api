from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import db_interface
from core.schemas.events import Event, EventCreate, EventUpdate

from . import crud, utils

router = APIRouter(prefix="/events", tags=["Events"])


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
        detail=f"Event with id {event_id} not found.",
    )


@router.post(
    "/",
    response_model=Event,
    status_code=status.HTTP_201_CREATED,
)
async def create_event(
    event_data: EventCreate,
    # user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(db_interface.scoped_session_dependency),
):
    return await crud.create_event(session=session, event_data=event_data)


@router.get("/{vehicle_id}/")
async def get_vehicle_events(
    vehicle_id: int,
    session: AsyncSession = Depends(db_interface.scoped_session_dependency),
):
    return await crud.get_vehicle_events(
        vehicle_id=vehicle_id, session=session
    )


@router.patch("/{event_id}/")
async def update_event(
    event_update: EventUpdate,
    event: Event = Depends(get_event_by_id_or_exception),
    session: AsyncSession = Depends(db_interface.scoped_session_dependency),
):
    return await crud.update_event(
        session=session, event=event, event_update=event_update
    )


@router.delete("/{event_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(
    event: Event = Depends(get_event_by_id_or_exception),
    session: AsyncSession = Depends(db_interface.scoped_session_dependency),
) -> None:
    return await crud.delete_event(session=session, event=event)


@router.get("/by_work_id/{vehicle_id}/{work_id}/")
async def get_events_by_work_id(
    vehicle_id: int,
    work_id: int,
    session: AsyncSession = Depends(db_interface.scoped_session_dependency),
):
    return await crud.get_events_for_vehicle_by_type(
        session=session, vehicle_id=vehicle_id, work_id=work_id
    )


@router.get("/average_interval/{vehicle_id}/{work_id}/")
async def get_average_interval_km_for_event(
    vehicle_id: int,
    work_id: int,
    session: AsyncSession = Depends(db_interface.scoped_session_dependency),
):
    events_list = await crud.get_events_for_vehicle_by_type(
        session=session, vehicle_id=vehicle_id, work_id=work_id
    )
    return await utils.get_average_mileage_interval(events_list=events_list)
