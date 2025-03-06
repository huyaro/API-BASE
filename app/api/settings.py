"""
__author__ = <huyaro> huyaro.dev@outlook.com
__date__ = 2024-11-11
__version__ = 0.0.1
__description__ = 系统配置 api
"""

from typing import Annotated, List

from fastapi import APIRouter, Depends

from app.ctx import APIResponse
from app.schema.settings import SettingsSchema
from app.service.settings import SettingsService

router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("/", response_model=APIResponse[List[SettingsSchema]])
async def read_settings(service: Annotated[SettingsService, Depends()]):
    settings = await service.get_all()
    return APIResponse.success(data=settings)
