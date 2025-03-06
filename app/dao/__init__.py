"""
__author__ = <huyaro> huyaro.dev@outlook.com
__date__ = 2024-10-20
__version__ = 0.0.1
__description__ =
"""

from typing import Any, Generic, List, Sequence, Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ctx import T_TABLE
from app.db import pg_upsert


class BaseDao(Generic[T_TABLE]):
    def __init__(self, table: Type[T_TABLE], db: AsyncSession):
        self.table = table
        self.db = db

    async def get_all(self) -> Sequence[T_TABLE]:
        result = await self.db.scalars(select(self.table))
        return result.all()

    async def get_by_id(self, model_id: int) -> T_TABLE:
        result = await self.db.execute(select(self.table).where(self.table.id == model_id))
        return result.scalar_one_or_none()

    async def create(self, obj_in: T_TABLE) -> T_TABLE:
        self.db.add(obj_in)
        await self.db.commit()
        await self.db.refresh(obj_in)
        return obj_in

    async def update(self, obj_in: T_TABLE, new_values: dict[str, Any]) -> T_TABLE:
        """
        更新数据
        Args:
            obj_in:　待更新的数据对象
            new_values:　待更新的值

        Returns:　更新后的对象
        """
        assert obj_in.id, f"The data to be updated [{obj_in}] does not have an id and cannot be updated!"
        True and [setattr(obj_in, k, v) for k, v in new_values if hasattr(obj_in, k)]
        await self.db.commit()
        await self.db.refresh(obj_in)
        return obj_in

    async def save_or_update(self, obj_ins: List[T_TABLE], ignore_cols: set[str]) -> List[int]:
        """
        保存或更新多个对象
        Args:
            obj_ins: 待更新的数据集
            ignore_cols: 需要忽略更新的字段

        Returns:
            更新后的数据ID 合集
        """
        pks = self.table.get_biz_primary_keys()
        assert pks and any(pks), "Table {T_TABLE} has no biz primary keys!"
        return await pg_upsert(self.db, self.table, obj_ins, conflict_columns=pks, ignore_columns=ignore_cols)
