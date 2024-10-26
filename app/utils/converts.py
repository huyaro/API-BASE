"""
__author__ = <yanghu> yanghu@1000kx.com
__date__ = 2024-10-25
__version__ = 0.0.1
__description__ = 各类转换工具(均为无依赖的纯函数)
"""
import re
from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal

import arrow
import ujson


# ===========================日期转换===========================
def dt_to_str(date_obj: datetime, pat="YYYY-MM-DD HH:mm:ss") -> str:
    """
        将日期对象转换为指定的pat 格式
    :param date_obj: 日期实例
    :param pat: 日期格式化模式
    :return:
    """
    return arrow.get(date_obj).format(pat)


# ===========================字符串转换===========================
def snake_to_camel(snake_str: str) -> str:
    """下划线转驼峰"""
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


def camel_to_snake(name: str) -> str:
    """驼峰转下划线"""
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


# ===========================JSON转换===========================
# 自定义序列化函数
def __decimal_serializer(obj):
    if isinstance(obj, Decimal):
        return float(format_decimal(obj))
    elif isinstance(obj, datetime):
        return dt_to_str(obj)
    raise TypeError(f"Type {type(obj)} not serializable")


def loads_json(json_str: str):
    return ujson.loads(json_str)


def dumps_json(json_obj: str | dict | list) -> str:
    """对json进行压缩,去除多余的空格,tab,换行"""
    if json_obj is None:
        return "{}"

    maybe_json_obj = json_obj
    if isinstance(json_obj, str | bytes):
        maybe_json_obj = loads_json(json_obj)

    return ujson.dumps(maybe_json_obj, ensure_ascii=False, separators=(",", ":"), default=__decimal_serializer)


# ===========================数值转换===========================
def format_decimal(value: Decimal | str | float | int | None, digits: int = 2) -> Decimal:
    # 检查是否为 None 或空字符串
    if value is None or value == "":
        return Decimal(0).quantize(Decimal(f"0.{'0' * digits}"), rounding=ROUND_HALF_UP)

    # 如果 value 已经是 Decimal 类型，直接使用
    if isinstance(value, Decimal):
        decimal_value = value
    else:
        # 尝试将值转换为 Decimal
        try:
            decimal_value = Decimal(value)
        except ValueError:
            raise ValueError(f"Invalid input[{value}]: must be a valid number.")

    # 这里使用了 ROUND_HALF_UP 来控制小数的舍入方式, 金额一般都是向上取四舍五入
    return decimal_value.quantize(Decimal(f"0.{'0' * digits}"), rounding=ROUND_HALF_UP)

