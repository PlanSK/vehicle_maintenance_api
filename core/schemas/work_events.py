import datetime

from pydantic import BaseModel, ConfigDict


class WorkEventBase(BaseModel):
    work_date: datetime.date
    mileage: int
    work_id: int
    part_price: float
    work_price: float
    note: str


class WorkEventUpdate(BaseModel):
    work_date: datetime.date | None = None
    mileage: int | None = None
    part_price: float | None = None
    work_price: float | None = None
    note: str | None = None


class WorkEventCreate(WorkEventBase):
    pass


class WorkEventSchema(WorkEventBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
