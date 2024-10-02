from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

import api_v1.workpatterns.crud
from core.database import db_interface
from core.schemas.workpattern import (
    WorkPatternBase,
    WorkPatternSchema,
    WorkPatternUpdate,
)

router = APIRouter(prefix="/workpatterns", tags=["Work patterns"])


async def get_workppatten_by_id_or_exception(
    workpattern_id: int,
    session: AsyncSession = Depends(db_interface.scoped_session_dependency),
):
    if instance := await api_v1.workpatterns.crud.get_workpattern_by_id(
        workpattern_id=workpattern_id, session=session
    ):
        return instance
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Workpatten with id {workpattern_id} not found.",
    )


@router.post(
    "/", response_model=WorkPatternSchema, status_code=status.HTTP_201_CREATED
)
async def create_workpattern(
    work_pattern_data: WorkPatternBase,
    # user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(db_interface.scoped_session_dependency),
):
    return await api_v1.workpatterns.crud.create_workpattern(
        session=session, work_pattern_data=work_pattern_data
    )


@router.get("/", response_model=list[WorkPatternSchema])
async def get_all_workpatterns(
    session: AsyncSession = Depends(db_interface.scoped_session_dependency),
):
    return await api_v1.workpatterns.crud.get_all_workpatterns(session=session)


@router.get("/{workpattern_id}/")
async def get_workpattern_by_id(
    workpattern_id: int,
    session: AsyncSession = Depends(db_interface.scoped_session_dependency),
):
    return await api_v1.workpatterns.crud.get_workpattern_by_id(
        workpattern_id=workpattern_id, session=session
    )


@router.patch("/{workpattern_id}/")
async def update_workpattern(
    workpattern_update: WorkPatternUpdate,
    workpattern: WorkPatternSchema = Depends(
        get_workppatten_by_id_or_exception
    ),
    session: AsyncSession = Depends(db_interface.scoped_session_dependency),
):
    return await api_v1.workpatterns.crud.update_workpattern(
        session=session,
        workpattern=workpattern,
        workpattern_update=workpattern_update,
    )


@router.delete("/{workpattern_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workpattern(
    workpattern: WorkPatternSchema = Depends(
        get_workppatten_by_id_or_exception
    ),
    session: AsyncSession = Depends(db_interface.scoped_session_dependency),
) -> None:
    return await api_v1.workpatterns.crud.delete_workpattern(
        session=session, workpattern=workpattern
    )
