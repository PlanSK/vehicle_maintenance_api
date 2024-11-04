from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.exc import IntegrityError

from core.database import db_handler
from core.schemas.works import WorkBase, WorkSchema, WorkUpdate

from . import crud
from .dependencies import get_work_by_id_or_exception

router = APIRouter(prefix="/works", tags=["Works"])


@router.post(
    "/", response_model=WorkSchema, status_code=status.HTTP_201_CREATED
)
async def create_work(
    work_data: WorkBase,
    # user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(db_handler.get_db),
):
    try:
        return await crud.create_work(session=session, work_data=work_data)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Incorrect incoming data.",
        )


@router.get("/{work_id}/")
async def get_work_by_id(
    work: WorkSchema = Depends(get_work_by_id_or_exception),
):
    return work


@router.get("/vehicle_id/{vehicle_id}/")
async def get_works_by_vehice_id(
    vehicle_id: int,
    session: AsyncSession = Depends(db_handler.get_db),
):
    return await crud.get_works_by_vehicle_id(
        session=session, vehicle_id=vehicle_id
    )


@router.patch("/{work_id}/")
async def update_work(
    work_update: WorkUpdate,
    work: WorkSchema = Depends(get_work_by_id_or_exception),
    session: AsyncSession = Depends(db_handler.get_db),
):
    return await crud.update_work(
        session=session, work=work, work_update=work_update
    )


@router.delete("/{work_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_work(
    work: WorkSchema = Depends(get_work_by_id_or_exception),
    session: AsyncSession = Depends(db_handler.get_db),
) -> None:
    return await crud.delete_work(session=session, work=work)
