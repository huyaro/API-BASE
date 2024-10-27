"""
__author__ = <huyaro> huyaro.dev@outlook.com
__date__ = 2024-10-20
__version__ = 0.0.1
__description__ = 
"""
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao import BaseDao
from app.db import use_db
from app.models.user import TabUser


class UserDao(BaseDao[TabUser]):
    DB_SESSION = Annotated[AsyncSession, Depends(use_db)]

    def __init__(self, db: DB_SESSION):
        super().__init__(model=TabUser, db=db)
        ...