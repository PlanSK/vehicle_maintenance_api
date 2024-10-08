from fastapi import Depends, HTTPException, status
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import db_interface
from core.models import Vehicle

from . import crud


async def get_vehicle_by_id_or_exceprion(
    vehicle_id: int,
    session: AsyncSession = Depends(db_interface.scoped_session_dependency),
):
    vehicle_instance: Vehicle | None = await crud.get_vehicle_by_id(
        vehicle_id=vehicle_id, session=session
    )
    if vehicle_instance:
        return vehicle_instance

    logger.error(f"Vehicle with {vehicle_id!r} not found in db.")
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Vehicle with {vehicle_id!r} not found in db.",
    )
