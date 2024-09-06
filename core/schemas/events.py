import datetime

from pydantic import BaseModel, ConfigDict


class EventBase(BaseModel):
    work_date: datetime.date
    mileage: int
    work_id: int
    vehicle_id: int
    part_price: float
    work_price: float
    note: str


class EventUpdate(BaseModel):
    work_date: datetime.date | None = None
    mileage: int | None = None
    part_price: float | None = None
    work_price: float | None = None
    note: str | None = None


class EventCreate(EventBase):
    pass


class Event(EventBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


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
    pass
