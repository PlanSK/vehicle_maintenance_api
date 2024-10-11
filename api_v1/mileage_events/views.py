from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import db_handler
from core.schemas.mileage_events import (
    MileageEventCreate,
    MileageEventSchema,
    MileageEventUpdate,
)

from . import crud
from .dependencies import get_mileage_work_event_by_id_or_exception

router = APIRouter(prefix="/mileage_events", tags=["Mileage Events"])


@router.post(
    "/", response_model=MileageEventSchema, status_code=status.HTTP_201_CREATED
)
async def create_mileage_event(
    milage_event_data: MileageEventCreate,
    # user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(db_handler.get_db),
):
    return await crud.create_mileage_event(
        session=session, mileage_event_data=milage_event_data
    )


@router.get("/{vehicle_id}/")
async def get_vehicle_mileage_events(
    vehicle_id: int,
    session: AsyncSession = Depends(db_handler.get_db),
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
    session: AsyncSession = Depends(db_handler.get_db),
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
    session: AsyncSession = Depends(db_handler.get_db),
) -> None:
    return await crud.delete_mileage_event(
        session=session, mileage_event=mileage_event
    )
