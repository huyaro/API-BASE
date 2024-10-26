"""
__author__ = <yanghu> yanghu@1000kx.com
__date__ = 2024-10-20
__version__ = 0.0.1
__description__ = 表单及响应模型基类
"""
import json
from datetime import datetime
from decimal import Decimal
from functools import partial
from typing import Any

from pydantic import BaseModel, ConfigDict, alias_generators, field_serializer

from app.utils.converts import dt_to_str, format_decimal


class DateTimeEncoder(json.JSONEncoder):

    def encode(self, o):
        return dt_to_str(o) if isinstance(o, datetime) else o


class DecimalEncoder(json.JSONEncoder):

    def encode(self, o):
        return float(format_decimal(o)) if isinstance(o, Decimal) else o


class BaseSchema(BaseModel):
    __abstract__ = True

    # class Config:
    #     alias_generator = alias_generators.to_camel
    #     from_attributes = True
    #     populate_by_name = True
    #     arbitrary_types_allowed = True
    #     json_encoders = {
    #         datetime: lambda dt: dt_to_str(dt),
    #         Decimal: lambda v: float(format_decimal(v)),
    #     }
    model_config = ConfigDict(
        alias_generator=alias_generators.to_camel,
        from_attributes=True,
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

    @field_serializer('*')
    def serialize_dt(self, item: Any, _info):
        if isinstance(item, datetime):
            return dt_to_str(item)
        elif isinstance(item, Decimal):
            return float(format_decimal(item))
        else:
            return item



