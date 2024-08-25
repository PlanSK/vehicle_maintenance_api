from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import declared_attr, Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .vehicle import Vehicle

from .base import DB_PREFIX


class VehicleRelationMixin:
    _vehicle_back_populates: str | None = None

    @declared_attr
    def vehicle_id(cls) -> Mapped[int]:
        return mapped_column(
            ForeignKey(f"{DB_PREFIX}vehicles.id", ondelete="CASCADE")
        )

    @declared_attr
    def vehicle(cls) -> Mapped["Vehicle"]:
        return relationship(back_populates=cls._vehicle_back_populates)
