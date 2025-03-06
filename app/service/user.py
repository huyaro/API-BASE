"""
__author__ = <huyaro> huyaro.dev@outlook.com
__date__ = 2024-10-20
__version__ = 0.0.1
__description__ = 逻辑处理层
"""

from collections.abc import Sequence
from typing import Annotated

from fastapi import Depends

from app.dao.user import UserDao
from app.schema.user import UserSchema, UserSimple


class UserService:
    UserDao = Annotated[UserDao, Depends()]

    def __init__(self, user_dao: UserDao):
        self.user_dao = user_dao

    async def get_by_id(self, data_id: int) -> UserSchema:
        res_model = await self.user_dao.get_by_id(data_id)
        return UserSchema.model_validate(res_model)

    async def get_all(self) -> Sequence[UserSchema]:
        users = await self.user_dao.get_all()
        # 类型转换 table => schema
        return [UserSchema.model_validate(user) for user in users]

    async def get_all_simple(self):
        users = await self.user_dao.get_all()
        return [UserSimple.model_validate(user) for user in users]
