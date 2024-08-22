from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    DeclarativeBase,
    declared_attr,
)

DB_PREFIX = "api_"


class BaseDbModel(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{DB_PREFIX}{cls.__name__.lower()}s"

    id: Mapped[int] = mapped_column(primary_key=True)
