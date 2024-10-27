"""
__author__ = <yanghu> yanghu@1000kx.com
__date__ = 2024-10-27
__version__ = 0.0.1
__description__ = 
"""
import re
from decimal import ROUND_HALF_UP, Decimal


def is_valid_number(s: str) -> bool:
    # 正则表达式解释:
    # ^[-+]? : 可选的负号或正号
    # \d+ : 至少一个整数部分数字
    # (\.\d{1,5})?$ : 可选的小数点后跟 1 到 5 位小数数字
    pattern = r"^[-+]?\d+(\.\d{1,5})?$"
    return bool(re.match(pattern, s))


def format_decimal(value: Decimal | str | float | int | None, digits: int = 2) -> Decimal:
    """
        将value转换为decimal
    """
    if value is None or value == "":
        return Decimal(0).quantize(Decimal(f"0.{'0' * digits}"), rounding=ROUND_HALF_UP)

    if not is_valid_number(value):
        raise ValueError("value[{value}] is not a valid number!")

    # 如果 value 已经是 Decimal 类型，直接使用
    if isinstance(value, Decimal):
        decimal_value = value
    else:
        # 尝试将值转换为 Decimal
        try:
            decimal_value = Decimal(value)
        except ValueError:
            raise

    return decimal_value.quantize(Decimal(f"0.{'0' * digits}"), rounding=ROUND_HALF_UP)