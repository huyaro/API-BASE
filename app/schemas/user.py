"""
__author__ = <yanghu> yanghu@1000kx.com
__date__ = 2024-10-20
__version__ = 0.0.1
__description__ = 用户模型
"""

from app.schemas import BaseSchema


class UserSchema(BaseSchema):
    ...


class UserCreate(UserSchema):
    ...


class UserRead(UserSchema):
    ...