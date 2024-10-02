from pydantic import BaseModel, ConfigDict


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
