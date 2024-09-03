from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import db_interface
from core.models import vehicle
from core.schemas.vehicles import Vehicle, VehicleCreate, VehicleUpdate

from . import crud
from .utils import get_vehicle_by_id_or_exceprion

router = APIRouter(prefix="/vehicle", tags=["Vehicles"])


@router.post("/", response_model=Vehicle, status_code=status.HTTP_201_CREATED)
async def create_vehicle(
    vehicle_data: VehicleCreate,
    session: AsyncSession = Depends(db_interface.scoped_session_dependency),
):
    return await crud.create_vehicle(
        session=session, vehicle_data=vehicle_data
    )


@router.get("/", response_model=list[Vehicle])
async def get_all_vehicles(
    session: AsyncSession = Depends(db_interface.scoped_session_dependency),
):
    return await crud.get_all_vehicles(session=session)


@router.get("/{vehicle_id}/", response_model=Vehicle)
async def get_vehicle_by_id(
    vehicle_id: int,
    session: AsyncSession = Depends(db_interface.scoped_session_dependency),
):
    return await get_vehicle_by_id_or_exceprion(
        vehicle_id=vehicle_id, session=session
    )


@router.get("/by_user_id/{user_id}/", response_model=list[Vehicle])
async def get_users_vehicles(
    user_id: int,
    session: AsyncSession = Depends(db_interface.scoped_session_dependency),
):
    return await crud.get_users_vehicles(user_id=user_id, session=session)


@router.patch("/{vehicle_id}/")
async def update_vehicle_partial(
    vehicle_update: VehicleUpdate,
    vehicle: Vehicle = Depends(get_vehicle_by_id_or_exceprion),
    session: AsyncSession = Depends(db_interface.scoped_session_dependency),
):
    return await crud.update_vehicle(
        session=session, vehicle=vehicle, vehicle_update=vehicle_update
    )


@router.delete("/{vehicle_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    vehicle: Vehicle = Depends(get_vehicle_by_id_or_exceprion),
    session: AsyncSession = Depends(db_interface.scoped_session_dependency),
) -> None:
    return await crud.delete_vehicle(session=session, vehicle=vehicle)
