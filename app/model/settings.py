"""
__author__ = <huyaro> huyaro.dev@outlook.com
__date__ = 2024-10-27
__version__ = 0.0.1
__description__ = 业务配置表
"""

from sqlalchemy import BOOLEAN, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import mapped_column

from . import BaseTable


class TabSettings(BaseTable):
    __tablename__ = "sys_settings"
    __table_args__ = (UniqueConstraint("module", "key", name="pk_settings_module_key"), {"comment": "系统配置表"})

    module = mapped_column(String(50), nullable=False, comment="模块名称")
    key = mapped_column(String(50), nullable=False, index=True, comment="配置项名称")
    value = mapped_column(String(50), comment="配置项值")
    value_type = mapped_column(String(10), comment="配置项值类型")
    value_bundle = mapped_column(JSONB, comment="配置项值约束")
    description = mapped_column(String(100), comment="配置项描述")
    activated = mapped_column(BOOLEAN, comment="是否激活", default=True)
