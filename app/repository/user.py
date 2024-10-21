"""
__author__ = <yanghu> yanghu@1000kx.com
__date__ = 2024-10-20
__version__ = 0.0.1
__description__ = 
"""
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models.user import UserModel
from app.repository import BaseRepository


class UserRepository(BaseRepository[UserModel]):
    def __init__(self, db_session: AsyncSession = Depends(get_db)):
        super().__init__(model=UserModel, db=db_session)
        ...