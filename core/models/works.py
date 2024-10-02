from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseDbModel
from .mixins import VehicleRelationMixin

if TYPE_CHECKING:
    from .work_event import WorkEvent


class WorkType(Enum):
    MAINTENANCE = "Maintenance"
    REPAIR = "Repair"
    TUNING = "Tuning"


class Work(VehicleRelationMixin, BaseDbModel):
    _vehicle_back_populates = "works"

    title: Mapped[str]
    interval_month: Mapped[int | None]
    interval_km: Mapped[int | None]
    work_type: Mapped[WorkType] = mapped_column(default=WorkType.MAINTENANCE)
    note: Mapped[str] = mapped_column(default="")
    events: Mapped[list["WorkEvent"]] = relationship()
