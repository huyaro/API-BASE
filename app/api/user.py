"""
__author__ = <yanghu> yanghu@1000kx.com
__date__ = 2024-10-20
__version__ = 0.0.1
__description__ = 用户数据API
"""

from fastapi import APIRouter, Depends

from app.ctx import CommonResponse
from app.schemas.user import UserSchema
from app.service.user import UserService

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/", response_model=CommonResponse[UserSchema])
async def get_user(service: UserService =  Depends()):
    users = await service.get_all()
    data = [UserSchema(**user.to_dict()) for user in users]
    return CommonResponse.ok(data=data)
