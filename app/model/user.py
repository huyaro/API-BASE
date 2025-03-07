"""
__author__ = <huyaro> huyaro.dev@outlook.com
__date__ = 2024-10-20
__version__ = 0.0.1
__description__ = 
"""

from sqlalchemy import BOOLEAN, SMALLINT, TIMESTAMP, String, func
from sqlalchemy.orm import mapped_column

from . import BaseTable


class TabUser(BaseTable):
    __tablename__ = 'user'
    __table_args__ = {'comment': '系统配置表'}

    username = mapped_column(String(50), unique=True, nullable=False)
    password = mapped_column(String(50), nullable=False)
    nickname = mapped_column(String(50))
    age = mapped_column(SMALLINT)
    last_login_time = mapped_column(TIMESTAMP, nullable=False, default=func.now)
    expired = mapped_column(BOOLEAN, nullable=False, default=False)
    locked = mapped_column(BOOLEAN, nullable=False, default=False)


