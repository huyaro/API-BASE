"""
__author__ = <yanghu> yanghu@1000kx.com
__date__ = 2024-10-20
__version__ = 0.0.1
__description__ = 
"""
from typing import TypeVar

from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column

from . import BaseOrm


class UserModel(BaseOrm):
    __tablename__ = 'user'


    username = mapped_column(String(50), unique=True, nullable=False)
    nickname = mapped_column(String(50), nullable=False)
    age = mapped_column(Integer)
    address = mapped_column(String(200))


T_MODEL = TypeVar("T_MODEL", bound=BaseOrm)