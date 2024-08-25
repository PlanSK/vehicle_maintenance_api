from sqlalchemy.orm import Mapped

from .base import BaseDbModel
from .mixins import VehicleRelationMixin


class WorkPattern(BaseDbModel):
    title: Mapped[str]
    interval_month: Mapped[int]
    interval_km: Mapped[int]


class Work(VehicleRelationMixin, BaseDbModel):
    _vehicle_back_populates="works"

    title: Mapped[str]
    interval_month: Mapped[int]
    interval_km: Mapped[int]
    work_type: Mapped[int]
    note: Mapped[str]
