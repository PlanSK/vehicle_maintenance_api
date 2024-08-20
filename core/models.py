import datetime
from typing import Optional

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
    DeclarativeBase,
    declared_attr,
)


class BaseDbModel(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"api_{cls.__name__.lower()}s"

    id: Mapped[int] = mapped_column(primary_key=True)


class User(BaseDbModel):
    login: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    first_name: Mapped[str]
    last_name: Mapped[Optional[str]]
    user_email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    vehicles: Mapped[list["Vehicle"]] = relationship()


class Vehicle(BaseDbModel):
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
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


class WorkPattern(BaseDbModel):
    title: Mapped[str]
    interval_month: Mapped[int]
    interval_km: Mapped[int]


class Work(WorkPattern):
    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey("vehicles.id", ondelete="CASCADE")
    )
    vehicle: Mapped["Vehicle"] = relationship(back_populates="works")
    work_type: Mapped[int]
    note: Mapped[str]


class Event(BaseDbModel):
    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey("vehicles.id", ondelete="CASCADE")
    )
    vehicle: Mapped["Vehicle"] = relationship(back_populates="events")
    work_date: Mapped[datetime.date]
    mileage: Mapped[int]
    work_id: Mapped[int] = mapped_column(
        ForeignKey("works.id", ondelete="CASCADE")
    )
    work: Mapped["Work"] = relationship()
    part_price: Mapped[float]
    work_price: Mapped[float]
    note: Mapped[str]


class MileageEvent(BaseDbModel):
    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey("vehicles.id", ondelete="CASCADE")
    )
    mileage_date: Mapped[datetime.date]
    mileage: Mapped[int]
