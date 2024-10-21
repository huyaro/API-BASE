"""
__author__ = <yanghu> yanghu@1000kx.com
__date__ = 2024-10-20
__version__ = 0.0.1
__description__ = 
"""

from typing import Generic, Type

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import T_MODEL


class BaseRepository(Generic[T_MODEL]):
    def __init__(self, model: Type[T_MODEL], db: AsyncSession):
        self.model = model
        self.db = db

    async def get_by_id(self, model_id: int) -> T_MODEL:
        result = await self.db.execute(self.model.select().where(self.model.id == model_id))
        return result.scalar_one_or_none()

    async def create(self, obj_in: T_MODEL) -> T_MODEL:
        self.db.add(obj_in)
        await self.db.commit()
        await self.db.refresh(obj_in)
        return obj_in