"""
__author__ = <yanghu> yanghu@1000kx.com
__date__ = 2024-10-27
__version__ = 0.0.1
__description__ = 集合相关转换工具
"""

from typing import Any, Dict, List, Optional


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


def filter_dict_keys(
    data: List[Dict[str, Any]], include: Optional[List[str]] = None, exclude: Optional[List[str]] = None
) -> List[Dict[str, Any]]:
    """
    从list[dict]中过滤出指定的key. include 与exclude 只能一个有值.
    """
    # 检查 include 和 exclude 是否同时有值
    if include and exclude:
        raise ValueError("Only one of 'include' or 'exclude' can be provided.")

    filtered_data = []

    for item in data:
        # 如果 `include` 有值，则只保留 `include` 中的键
        if include:
            filtered_item = {k: v for k, v in item.items() if k in include}
        # 如果 `exclude` 有值，则排除 `exclude` 中的键
        elif exclude:
            filtered_item = {k: v for k, v in item.items() if k not in exclude}
        else:
            # 如果两者都为空，保留原始字典
            filtered_item = item

        filtered_data.append(filtered_item)

    return filtered_data
