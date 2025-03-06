"""
__author__ = <huyaro> huyaro.dev@outlook.com
__date__ = 2024-10-20
__version__ = 0.0.1
__description__ = 用户数据API
"""

from typing import Annotated, List

from fastapi import APIRouter, Depends

from app.ctx import APIResponse
from app.schema.user import UserSchema, UserSimple
from app.service.user import UserService

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/", response_model=APIResponse[List[UserSchema]])
async def get_user(service: Annotated[UserService, Depends()]):
    users = await service.get_all()
    return APIResponse.success(data=users)


@router.get("/simple", response_model=APIResponse[List[UserSimple]])
async def get_simple_user(service: Annotated[UserService, Depends()]):
    users = await service.get_all_simple()
    return APIResponse.success(data=users)
