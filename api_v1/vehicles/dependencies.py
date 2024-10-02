from fastapi import Depends, HTTPException, status
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.vehicles import crud
from core.database import db_interface
from core.models import Vehicle


async def get_vehicle_by_id_or_exceprion(
    vehicle_id: int,
    session: AsyncSession = Depends(db_interface.scoped_session_dependency),
) -> Vehicle:
    vehicle_instance = await crud.get_vehicle_by_id(
        vehicle_id=vehicle_id, session=session
    )
    if not vehicle_instance:
        logger.error(f"Vehicle with {vehicle_id!r} not found in db.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle with {vehicle_id!r} not found in db.",
        )
    return vehicle_instance
