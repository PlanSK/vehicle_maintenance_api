from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import db_interface
from core.schemas.works import WorkBase, WorkSchema, WorkUpdate

from . import crud

router = APIRouter(prefix="/works", tags=["Works"])


async def get_work_by_id_or_exception(
    work_id: int,
    session: AsyncSession = Depends(db_interface.scoped_session_dependency),
):
    if instance := await crud.get_work_by_id(work_id=work_id, session=session):
        return instance
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Work with id {work_id} not found.",
    )


@router.post(
    "/", response_model=WorkSchema, status_code=status.HTTP_201_CREATED
)
async def create_work(
    work_data: WorkBase,
    # user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(db_interface.scoped_session_dependency),
):
    return await crud.create_work(session=session, work_data=work_data)


@router.get("/{vehicle_id}/")
async def get_works_by_vehice_id(
    vehicle_id: int,
    session: AsyncSession = Depends(db_interface.scoped_session_dependency),
):
    return await crud.get_works_by_vehicle_id(
        session=session, vehicle_id=vehicle_id
    )


@router.get("/{work_id}/")
async def get_work_by_id(
    work_id: int,
    session: AsyncSession = Depends(db_interface.scoped_session_dependency),
):
    return get_work_by_id_or_exception(work_id=work_id, session=session)


@router.patch("/{workpattern_id}/")
async def update_work(
    work_update: WorkUpdate,
    work: WorkSchema = Depends(get_work_by_id_or_exception),
    session: AsyncSession = Depends(db_interface.scoped_session_dependency),
):
    return await crud.update_work(
        session=session, work=work, work_update=work_update
    )


@router.delete("/{work_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_work(
    work: WorkSchema = Depends(get_work_by_id_or_exception),
    session: AsyncSession = Depends(db_interface.scoped_session_dependency),
) -> None:
    return await crud.delete_work(session=session, work=work)
