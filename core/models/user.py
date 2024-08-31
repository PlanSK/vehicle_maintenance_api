from typing import TYPE_CHECKING, Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseDbModel

if TYPE_CHECKING:
    from .vehicle import Vehicle


class User(BaseDbModel):
    username: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    first_name: Mapped[str]
    last_name: Mapped[Optional[str]]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    vehicles: Mapped[list["Vehicle"]] = relationship(back_populates="owner")
