from pydantic import BaseModel, ConfigDict

from core.models.works import WorkType


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
