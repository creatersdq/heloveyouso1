from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.declarative import declared_attr


class TimestampMixin:
    @declared_attr
    def gmtCreated(cls):
        return Column(DateTime, default=func.now(), nullable=False)

    @declared_attr
    def gmtUpdated(cls):
        return Column(
            DateTime,
            default=func.now(),
            onupdate=func.now(),
            nullable=False,
        )