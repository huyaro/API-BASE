"""
__author__ = <huyaro> huyaro.dev@outlook.com
__date__ = 2024-11-11
__version__ = 0.0.1
__description__ = settings service
"""

from collections.abc import Sequence
from typing import Annotated

from fastapi import Depends

from app.dao.settings import SettingsDao
from app.schema.settings import SettingsSchema


class SettingsService:
    SettingsDao = Annotated[SettingsDao, Depends()]

    def __init__(self, settings_dao: SettingsDao):
        self.settings_dao = settings_dao

    async def get_all(self) -> Sequence[SettingsSchema]:
        settings = await self.settings_dao.get_all()
        return [SettingsSchema.model_validate(st) for st in settings]
