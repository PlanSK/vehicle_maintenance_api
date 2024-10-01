import datetime

from pydantic import BaseModel, ConfigDict


class MileageEventBase(BaseModel):
    vehicle_id: int
    mileage_date: datetime.date
    mileage: int


class MileageEventUpdate(BaseModel):
    mileage_date: datetime.date | None = None
    mileage: int | None = None


class MileageEventCreate(MileageEventBase):
    pass


class MileageEvent(MileageEventBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
