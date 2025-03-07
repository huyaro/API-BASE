"""
__author__ = <huyaro> huyaro.dev@outlook.com
__date__ = 2024-10-20
__version__ = 0.0.1
__description__ = 用户模型
"""

from app.model.user import TabUser
from app.utils.metas import create_schema

UserSchema = create_schema(TabUser)

UserSimple = create_schema(TabUser, include=[TabUser.id, TabUser.username, TabUser.age, TabUser.last_login_time])
