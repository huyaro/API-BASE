"""
__author__ = <huyaro> huyaro.dev@outlook.com
__date__ = 2024-10-20
__version__ = 0.0.1
__description__ = 表单及响应模型基类
"""
from typing import Any

from pydantic import BaseModel, ConfigDict, alias_generators, field_serializer

from app.utils.serials import custom_serializer


class BaseSchema(BaseModel):
    """所有 schema 的基类"""
    __abstract__ = True

    model_config = ConfigDict(
        alias_generator=alias_generators.to_camel,
        from_attributes=True,
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

    @field_serializer('*')
    def serialize_dt(self, item: Any, _info):
        return custom_serializer(item)



