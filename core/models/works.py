from enum import Enum

from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseDbModel
from .mixins import VehicleRelationMixin


class WorkType(Enum):
    MAINTENANCE = "Maintenance"
    REPAIR = "Repair"
    TUNING = "Tuning"


class WorkPattern(BaseDbModel):
    title: Mapped[str]
    interval_month: Mapped[int]
    interval_km: Mapped[int]


class Work(VehicleRelationMixin, BaseDbModel):
    _vehicle_back_populates = "works"

    title: Mapped[str]
    interval_month: Mapped[int]
    interval_km: Mapped[int]
    work_type: Mapped[WorkType] = mapped_column(default=WorkType.MAINTENANCE)
    note: Mapped[str]
