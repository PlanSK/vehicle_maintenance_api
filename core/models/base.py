import re

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
)

DB_PREFIX = "api_"
camel_case_pattern = re.compile(r"(?<!^)(?=[A-Z])")


class BaseDbModel(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return (
            f"{DB_PREFIX}{camel_case_pattern.sub('_', cls.__name__).lower()}s"
        )

    id: Mapped[int] = mapped_column(primary_key=True)
