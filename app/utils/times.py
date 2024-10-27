"""
__author__ = <yanghu> yanghu@1000kx.com
__date__ = 2024-10-20
__version__ = 0.0.1
__description__ = 日期时间相关的工具函数
"""
from datetime import datetime
from typing import Union

import arrow

FMT_DATE = "YYYY-MM-DD"
FMT_TIME = "HH:mm:ss"
FMT_DT = f"{FMT_DATE} {FMT_TIME}"


def dt_to_str(date_obj: datetime, pat=FMT_DT) -> str:
    """
        将日期对象转换为指定的pat 格式
    :param date_obj: 日期实例
    :param pat: 日期格式化模式
    :return:
    """
    return arrow.get(date_obj).format(pat)


def adjust_datetime(
    date_input: Union[datetime, str],
    *,
    year: int = 0,
    month: int = 0,
    day: int = 0,
    hour: int = 0,
    minute: int = 0,
    second: int = 0,
) -> datetime:
    """
    根据给定的日期和时间增量进行日期调整，并返回不带时区的 datetime。

    :param date_input: 起始日期，支持 datetime 或 str 类型
    :param year: 年份调整值（正负整数）
    :param month: 月份调整值（正负整数）
    :param day: 天数调整值（正负整数）
    :param hour: 小时调整值（正负整数）
    :param minute: 分钟调整值（正负整数）
    :param second: 秒调整值（正负整数）
    :return: 调整后的不带时区的 datetime 对象
    """

    date = arrow.get(date_input)
    date = date.shift(years=year, months=month, days=day, hours=hour, minutes=minute, seconds=second)

    # 返回不带时区的 naive datetime
    return date.naive