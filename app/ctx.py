"""
__author__ = <yanghu> yanghu@1000kx.com
__date__ = 2024-10-20
__version__ = 0.0.1
__description__ = 
"""
from typing import Optional, TypeVar, Generic, List, Type

from fastapi import FastAPI
from loguru import logger
from pydantic import BaseModel
from starlette.responses import JSONResponse
from typing_extensions import TypeVar

from app.db import async_engine
from app.models import BaseTable
from app.schemas import BaseSchema
from app.utils.converts import dumps_json

T_TABLE = TypeVar("T_TABLE", bound=BaseTable)
T_SCHEMA = TypeVar("T_SCHEMA", bound=BaseSchema)
SCHEMAS  = List[T_SCHEMA]

class CommonResponse(BaseModel, Generic[T_SCHEMA]):
    code: int = 0
    msg: str = "ok"
    data: Optional[T_SCHEMA] = None

    @staticmethod
    def ok(data: Optional[T_SCHEMA]) -> JSONResponse:
        content = dumps_json(CommonResponse(data=data).model_dump(by_alias=True))
        return JSONResponse(content=content, status_code=200)

    @staticmethod
    def fail(code: int, msg: str) -> JSONResponse:
        content = dumps_json(CommonResponse(code=code, msg=msg).model_dump(by_alias=True, exclude={'data'}))
        return JSONResponse(content=content, status_code=200)


async def __init_tables():
    logger.info("初始化数据库表...")
    async with async_engine.begin() as conn:
        await conn.run_sync(BaseTable.metadata.create_all)

async def app_life_span(app: FastAPI):
    await __init_tables()
    yield
    print("done")