"""
__author__ = <yanghu> yanghu@1000kx.com
__date__ = 2024-10-20
__version__ = 0.0.1
__description__ = 逻辑处理层
"""
from typing import Annotated, Sequence

from fastapi import Depends

from app.repository.user import UserRepository
from app.schemas.user import UserSchema, UserSimple


class UserService:

    USER_REPOS = Annotated[UserRepository, Depends()]

    def __init__(self, user_dao: USER_REPOS):
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