"""
__author__ = <huyaro> huyaro.dev@outlook.com
__date__ = 2024-10-20
__version__ = 0.0.1
__description__ = 用户模型
"""

from app.model.settings import TabSettings
from app.utils.metas import create_schema

SettingsSchema = create_schema(TabSettings)
