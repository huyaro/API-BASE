"""
__author__ = <yanghu> yanghu@1000kx.com
__date__ = 2024-10-20
__version__ = 0.0.1
__description__ = 逻辑处理层
"""
from typing import List, Sequence

from fastapi import Depends

from app.models.user import TabUser
from app.repository.user import UserRepository
from app.schemas.user import UserSchema


class UserService:

    def __init__(self, user_dao: UserRepository = Depends()):
        self.user_dao = user_dao

    async def get_by_id(self, data_id: int) -> UserSchema:
        res_model = await self.user_dao.get_by_id(data_id)
        return UserSchema.model_validate(res_model)

    async def get_all(self) -> Sequence[TabUser]:
        return await self.user_dao.get_all()