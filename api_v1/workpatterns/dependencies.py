from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.workpatterns import crud
from core.database import db_interface


async def get_workppatten_by_id_or_exception(
    workpattern_id: int,
    session: AsyncSession = Depends(db_interface.scoped_session_dependency),
):
    workpattern_instance = await crud.get_workpattern_by_id(
        workpattern_id=workpattern_id, session=session
    )
    if not workpattern_instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workpatten with id {workpattern_id} not found.",
        )
    return workpattern_instance
