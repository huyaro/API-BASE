"""
__author__ = <yanghu> yanghu@1000kx.com
__date__ = 2024-10-20
__version__ = 0.0.1
__description__ = 用户数据API
"""

from fastapi import APIRouter, Depends

from app.schemas.user import UserCreate, UserSchema
from app.service.user import UserService

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/", response_model=UserSchema)
async def create_user(user: UserCreate):
    ...


@router.get("/", response_model=UserSchema)
async def get_user(uid: int, service: UserService = Depends()):
    return service.get_by_id(uid)