"""
__author__ = <yanghu> yanghu@1000kx.com
__date__ = 2024-10-20
__version__ = 0.0.1
__description__ = 字符串处理相关的工具函数
"""
import re
from datetime import datetime
from decimal import Decimal

import ujson

from app.utils.nums import format_decimal
from app.utils.times import dt_to_str


# ===========================String===========================
def snake_to_camel(snake_str: str) -> str:
    """下划线转驼峰"""
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


def camel_to_snake(name: str) -> str:
    """驼峰转下划线"""
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


# ===========================JSON===========================
app_json_encoders = {
    datetime: lambda dt: dt_to_str(dt),
    Decimal: lambda dct: float(format_decimal(dct)),
}


def custom_serializer(obj):
    """
        自定义序列化函数
    """
    if isinstance(obj, tuple(app_json_encoders.keys())):
        return app_json_encoders[type(obj)](obj)

    return obj


def loads_json(json_str: str):
    return ujson.loads(json_str)


def dumps_json(json_obj: str | dict | list) -> str:
    """对json进行压缩,去除多余的空格,tab,换行"""
    if json_obj is None:
        return "{}"

    maybe_json_obj = json_obj
    if isinstance(json_obj, str | bytes):
        maybe_json_obj = loads_json(json_obj)

    return ujson.dumps(maybe_json_obj, ensure_ascii=False, separators=(",", ":"), default=custom_serializer)