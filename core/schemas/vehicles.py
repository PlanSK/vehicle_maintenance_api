import datetime

from pydantic import BaseModel, ConfigDict

from core.vin import VIN_Type


class VehicleBase(BaseModel):
    owner_id: int
    vin_code: VIN_Type
    vehicle_manufacturer: str
    vehicle_model: str
    vehicle_body: str
    vehicle_year: int
    vehicle_mileage: int
    vehicle_last_update_date: datetime.date


class VehicleCreate(VehicleBase):
    pass


class Vehicle(VehicleBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
