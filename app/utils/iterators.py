"""
__author__ = <yanghu> yanghu@1000kx.com
__date__ = 2024-10-27
__version__ = 0.0.1
__description__ = 集合相关转换工具
"""
from typing import Any


def get_dict_deep_value(data: dict, keys: list[str], default_value=None):
    """
        获取嵌套的字典的值. 如果值不存在就抛异常
    :param data: 字典
    :param keys: 多个key构成的list
    :param default_value: 默认值
    :return:
    """
    for key in keys:
        try:
            data = data[key]
        except (KeyError, TypeError):
            return default_value if default_value is not None else None
    return data


def filter_dict_keys(data: list[dict[str, Any]], keys: list[str]) -> list[dict[str, Any]]:
    """从list包含的字典中筛选出指定的Key重新组成list[dict]返回"""
    if data is None:
        return []
    if not isinstance(data[0], dict):
        raise ValueError("数据格式不符合要求, data中必须是dict")
    if not keys:
        return data

    return [{k: d[k] for k in keys if k in d} for d in data]