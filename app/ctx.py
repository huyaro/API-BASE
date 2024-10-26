"""
__author__ = <yanghu> yanghu@1000kx.com
__date__ = 2024-10-20
__version__ = 0.0.1
__description__ = 
"""
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, Generic, List, Union

from fastapi import FastAPI
from loguru import logger
from pydantic import BaseModel
from starlette.responses import JSONResponse
from typing_extensions import TypeVar

from app.db import async_engine
from app.models import BaseTable
from app.utils.converts import dumps_json, dt_to_str, format_decimal

T_TABLE = TypeVar("T_TABLE", bound=BaseTable)
T_SCHEMA = TypeVar("T_SCHEMA", bound=BaseModel)

T_RESP_BODY = Union[T_SCHEMA | List[T_SCHEMA] | List[Dict[str, Any]] | Dict[str, Any] | None]


class APIResponse(BaseModel, Generic[T_SCHEMA]):
    code: int = 0
    msg: str = "ok"
    data: Any = None

    @classmethod
    def success(cls, data: T_RESP_BODY) -> JSONResponse:
        def serialize_item(item):
            # 用于递归检查并序列化 BaseModel
            if isinstance(item, BaseModel):
                return item.model_dump(by_alias=True)
            elif isinstance(item, list):
                return [serialize_item(sub_item) for sub_item in item]
            elif isinstance(item, dict):
                return {key: serialize_item(value) for key, value in item.items()}
            else:
                return dumps_json(item)

        serialized_data = serialize_item(data) if data is not None else {}
        content = APIResponse(data=serialized_data).model_dump()
        return JSONResponse(content=content, status_code=200)

    @classmethod
    def failed(cls, code: int, msg: str) -> JSONResponse:
        content = dumps_json(APIResponse(code=code, msg=msg).model_dump_json(exclude_unset=True))
        return JSONResponse(content=content, status_code=200)


async def __init_tables():
    logger.info("初始化数据库表...")
    async with async_engine.begin() as conn:
        await conn.run_sync(BaseTable.metadata.create_all)


async def app_life_span(app: FastAPI):
    await __init_tables()
    yield
    print("done")