import datetime

from sqlalchemy.orm import Mapped

from .base import BaseDbModel
from .mixins import VehicleRelationMixin


class MileageEvent(VehicleRelationMixin, BaseDbModel):
    _vehicle_back_populates = "mileage_events"

    mileage_date: Mapped[datetime.date]
    mileage: Mapped[int]
