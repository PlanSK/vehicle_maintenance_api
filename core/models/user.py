from typing import Optional, TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseDbModel

if TYPE_CHECKING:
    from .vehicle import Vehicle


class User(BaseDbModel):
    login: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    first_name: Mapped[str]
    last_name: Mapped[Optional[str]]
    user_email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    vehicles: Mapped[list["Vehicle"]] = relationship()
