from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import db_interface
from core.schemas.mileage_events import (
    MileageEventCreate,
    MileageEventSchema,
    MileageEventUpdate,
)

from . import crud

router = APIRouter(prefix="/mileage_events", tags=["Mileage Events"])


async def get_mileage_work_event_by_id_or_exception(
    mileage_event_id: int,
    session: AsyncSession = Depends(db_interface.scoped_session_dependency),
):
    if instance := await crud.get_mileage_event_by_id(
        event_id=mileage_event_id, session=session
    ):
        return instance
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Work event with id {mileage_event_id} not found.",
    )


@router.post(
    "/",
    response_model=MileageEventSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_mileage_event(
    milage_event_data: MileageEventCreate,
    # user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(db_interface.scoped_session_dependency),
):
    return await crud.create_mileage_event(
        session=session, mileage_event_data=milage_event_data
    )


@router.get("/{vehicle_id}/")
async def get_vehicle_mileage_events(
    vehicle_id: int,
    session: AsyncSession = Depends(db_interface.scoped_session_dependency),
):
    return await crud.get_vehicle_mileage_events(
        vehicle_id=vehicle_id, session=session
    )


@router.patch("/{mileage_event_id}/")
async def update_mileage_event(
    mileage_event_update: MileageEventUpdate,
    mileage_event: MileageEventSchema = Depends(
        get_mileage_work_event_by_id_or_exception
    ),
    session: AsyncSession = Depends(db_interface.scoped_session_dependency),
):
    return await crud.update_mileage_event(
        session=session,
        mileage_event=mileage_event,
        mileage_event_update=mileage_event_update,
    )


@router.delete("/{mileage_event_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_mileage_event(
    mileage_event: MileageEventSchema = Depends(
        get_mileage_work_event_by_id_or_exception
    ),
    session: AsyncSession = Depends(db_interface.scoped_session_dependency),
) -> None:
    return await crud.delete_mileage_event(
        session=session, mileage_event=mileage_event
    )
