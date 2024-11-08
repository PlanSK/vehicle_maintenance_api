from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.auth.validate import get_current_active_user
from core.database import db_handler
from core.schemas.users import UserSchema
from core.schemas.vehicles import VehicleCreate, VehicleSchema, VehicleUpdate
from core.vin import vin_code_validator

from . import crud
from .dependencies import get_vehicle_by_id_or_exceprion

router = APIRouter(prefix="/vehicle", tags=["Vehicles"])


@router.post(
    "/", response_model=VehicleSchema, status_code=status.HTTP_201_CREATED
)
async def create_vehicle(
    vehicle_data: VehicleCreate,
    user: UserSchema = Depends(get_current_active_user),
    session: AsyncSession = Depends(db_handler.get_db),
):
    try:
        return await crud.create_vehicle(
            session=session, vehicle_data=vehicle_data, owner_id=user.id
        )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Incorrect incoming data.",
        )


@router.get("/", response_model=list[VehicleSchema])
async def get_all_vehicles(
    session: AsyncSession = Depends(db_handler.get_db),
):
    return await crud.get_all_vehicles(session=session)


@router.get("/{vehicle_id}/")
async def get_vehicle_by_id(
    vehicle: VehicleSchema = Depends(get_vehicle_by_id_or_exceprion),
):
    return vehicle


@router.get("/by_user_id/{user_id}/", response_model=list[VehicleSchema])
async def get_user_vehicles(
    user_id: int,
    session: AsyncSession = Depends(db_handler.get_db),
):
    return await crud.get_user_vehicles(user_id=user_id, session=session)


@router.patch("/{vehicle_id}/")
async def update_vehicle_partial(
    vehicle_update: VehicleUpdate,
    vehicle: VehicleSchema = Depends(get_vehicle_by_id_or_exceprion),
    session: AsyncSession = Depends(db_handler.get_db),
):
    return await crud.update_vehicle(
        session=session, vehicle=vehicle, vehicle_update=vehicle_update
    )


@router.delete("/{vehicle_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vehicle(
    vehicle: VehicleSchema = Depends(get_vehicle_by_id_or_exceprion),
    session: AsyncSession = Depends(db_handler.get_db),
) -> None:
    return await crud.delete_vehicle(session=session, vehicle=vehicle)


@router.get("/by_vin/{vehicle_vin}/", response_model=VehicleSchema)
async def get_vehicle_by_vin(
    vehicle_vin: str,
    session: AsyncSession = Depends(db_handler.get_db),
):
    try:
        vin_code_validator(vin_code=vehicle_vin)
    except AssertionError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="VIN Code format is incorrect or checksum is not valid.",
        )
    result = await crud.get_vehicle_by_vin(session=session, vin=vehicle_vin)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle with VIN {vehicle_vin} not found.",
        )
    return result
