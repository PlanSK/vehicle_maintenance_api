import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseDbModel, DB_PREFIX

if TYPE_CHECKING:
    from .user import User
    from .events import Event
    from .works import Work


class Vehicle(BaseDbModel):
    owner_id: Mapped[int] = mapped_column(
        ForeignKey(f"{DB_PREFIX}users.id", ondelete="CASCADE")
    )
    owner: Mapped["User"] = relationship(back_populates="vehicles")
    vin_code: Mapped[str] = mapped_column(String(17), unique=True, index=True)
    vehicle_manufacturer: Mapped[str]
    vehicle_model: Mapped[str]
    vehicle_body: Mapped[str]
    vehicle_year: Mapped[int]
    vehicle_mileage: Mapped[int]
    vehicle_last_update_date: Mapped[datetime.date]
    events: Mapped[list["Event"]] = relationship()
    works: Mapped[list["Work"]] = relationship()
