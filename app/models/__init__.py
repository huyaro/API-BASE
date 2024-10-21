"""
__author__ = <yanghu> yanghu@1000kx.com
__date__ = 2024-10-20
__version__ = 0.0.1
__description__ = 
"""
from sqlalchemy import BIGINT, TIMESTAMP, func
from sqlalchemy.orm import DeclarativeBase, mapped_column


class BaseOrm(DeclarativeBase):
    __abstract__ = True

    id = mapped_column(BIGINT, primary_key=True, autoincrement=True, nullable=False, sort_order=-99)

    created_time = mapped_column(TIMESTAMP, nullable=False, sort_order=100, insert_default=func.now)
    updated_time = mapped_column(TIMESTAMP, nullable=False, sort_order=101, insert_default=func.now, onupdate=func.now)
