from sqlalchemy.orm import Mapped

from core.models.base import BaseDbModel


class WorkPattern(BaseDbModel):
    title: Mapped[str]
    interval_month: Mapped[int]
    interval_km: Mapped[int]
