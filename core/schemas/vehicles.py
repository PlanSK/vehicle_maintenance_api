import datetime

from pydantic import BaseModel, ConfigDict

from core.vin import VIN_Type


class VehicleBase(BaseModel):
    vin_code: VIN_Type
    vehicle_manufacturer: str
    vehicle_model: str
    vehicle_body: str
    vehicle_year: int
    vehicle_mileage: int
    vehicle_last_update_date: datetime.date


class VehicleCreate(VehicleBase):
    pass

class VehicleUpdate(BaseModel):
    vin_code: VIN_Type | None = None
    vehicle_manufacturer: str | None = None
    vehicle_model: str | None = None
    vehicle_body: str | None = None
    vehicle_year: int | None = None
    vehicle_mileage: int | None = None


class Vehicle(VehicleBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    owner_id: int
