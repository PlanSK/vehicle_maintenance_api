from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.mileage_events import crud
from core.database import db_interface


async def get_mileage_work_event_by_id_or_exception(
    mileage_event_id: int,
    session: AsyncSession = Depends(db_interface.scoped_session_dependency),
):
    mileage_event_instance = await crud.get_mileage_event_by_id(
        event_id=mileage_event_id, session=session
    )
    if not mileage_event_instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Work event with id {mileage_event_id} not found.",
        )
    return mileage_event_instance
