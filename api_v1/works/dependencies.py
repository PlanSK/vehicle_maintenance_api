from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.works import crud
from core.database import db_handler


async def get_work_by_id_or_exception(
    work_id: int,
    session: AsyncSession = Depends(db_handler.get_db),
):
    work_instance = await crud.get_work_by_id(work_id=work_id, session=session)
    if not work_instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Work with id {work_id} not found.",
        )
    return work_instance
