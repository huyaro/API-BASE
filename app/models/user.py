"""
__author__ = <yanghu> yanghu@1000kx.com
__date__ = 2024-10-20
__version__ = 0.0.1
__description__ = 
"""

from sqlalchemy import BOOLEAN, SMALLINT, TIMESTAMP, String
from sqlalchemy.orm import mapped_column

from . import BaseTable


class TabUser(BaseTable):
    __tablename__ = 'user'

    username = mapped_column(String(50), unique=True, nullable=False)
    password = mapped_column(String(50), nullable=False)
    nickname = mapped_column(String(50))
    age = mapped_column(SMALLINT)
    last_login_time = mapped_column(TIMESTAMP, nullable=False)
    expired = mapped_column(BOOLEAN, nullable=False)
    locked = mapped_column(BOOLEAN, nullable=False)


