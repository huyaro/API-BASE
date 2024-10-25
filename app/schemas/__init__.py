"""
__author__ = <yanghu> yanghu@1000kx.com
__date__ = 2024-10-20
__version__ = 0.0.1
__description__ = 表单及响应模型基类
"""

from pydantic import BaseModel


class BaseSchema(BaseModel):
    __abstract__ = True

    class Config:
        from_attributes = True




