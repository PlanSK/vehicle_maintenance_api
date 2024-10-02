from pydantic import BaseModel, ConfigDict

from core.models.works import WorkType


class WorkPatternBase(BaseModel):
    title: str
    interval_month: int
    interval_km: int


class WorkPatternUpdate(BaseModel):
    title: str | None = None
    interval_month: int | None = None
    interval_km: int | None = None


class WorkPatternSchema(WorkPatternBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class WorkBase(BaseModel):
    title: str
    interval_month: int | None = None
    interval_km: int | None = None
    work_type: WorkType
    note: str = ""
    vehicle_id: int


class WorkUpdate(BaseModel):
    title: str | None = None
    interval_month: int | None = None
    interval_km: int | None = None
    work_type: WorkType | None = None
    note: str | None = None


class WorkSchema(WorkBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
