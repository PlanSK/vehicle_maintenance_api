from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.work_events.crud import get_event_by_id
from core.database import db_handler


async def get_event_by_id_or_exception(
    event_id: int,
    session: AsyncSession = Depends(db_handler.get_db),
):
    work_event_instance = await get_event_by_id(
        event_id=event_id, session=session
    )
    if not work_event_instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Work event with id {event_id} not found.",
        )
    return work_event_instance
