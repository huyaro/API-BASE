"""
__author__ = <huyaro> huyaro.dev@outlook.com
__date__ = 2024-10-20
__version__ = 0.0.1
__description__ = 数据库模型的基类
"""
from typing import Any

from sqlalchemy import BIGINT, TIMESTAMP, func
from sqlalchemy import inspect as sa_inspect
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, mapped_column


class BaseTable(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id = mapped_column(BIGINT, primary_key=True, autoincrement=True, nullable=False, sort_order=-99)

    created_time = mapped_column(TIMESTAMP, nullable=False, sort_order=100, default=func.current_time)
    updated_time = mapped_column(TIMESTAMP, nullable=False, sort_order=101, default=func.current_time, onupdate=func.current_time)

    def __repr__(self) -> str:
        return str(self.to_dict())

    def to_dict(self, aliases: dict[str, str] = None, exclude_none=False) -> dict[str, Any]:
        """
        数据库模型转成字典
        :param aliases:  字段别名字典 eg: {"id": "user_id"}, 把id名称替换成 user_id
        :param exclude_none: 默认排除None值
        returns: dict
        """
        aliases = aliases or {}
        if exclude_none:
            return {
                aliases.get(c.name, c.name): getattr(self, c.name)
                for c in sa_inspect(type(self)).columns if getattr(self, c.name) is not None
            }
        else:
            return {
                aliases.get(c.name, c.name): getattr(self, c.name, None)
                for c in sa_inspect(type(self)).columns
            }