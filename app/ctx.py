"""
__author__ = <huyaro> huyaro.dev@outlook.com
__date__ = 2024-10-20
__version__ = 0.0.1
__description__ = app context manager
"""

import sys
from typing import Generic

from fastapi import FastAPI
from loguru import logger
from pydantic import BaseModel
from starlette.responses import JSONResponse
from typing_extensions import TypeVar

from .db import async_engine
from .model import BaseTable
from .settings import settings
from .utils.times import FMT_DATE, dt_to_str

T_TABLE = TypeVar("T_TABLE", bound=BaseTable)
T_SCHEMA = TypeVar("T_SCHEMA", bound=BaseModel)

T_RESP_BODY = T_SCHEMA | list[T_SCHEMA] | None


class APIResponse(BaseModel, Generic[T_SCHEMA]):
    code: int = 0
    msg: str = "ok"
    data: T_RESP_BODY = None

    @classmethod
    def success(cls, data: T_RESP_BODY) -> JSONResponse:
        content = APIResponse(data=data).model_dump(by_alias=True)
        return JSONResponse(content=content, status_code=200)

    @classmethod
    def failed(cls, code: int, msg: str) -> JSONResponse:
        content = APIResponse(code=code, msg=msg).model_dump_json()
        return JSONResponse(content=content, status_code=200)


async def __init_tables():
    logger.info("...初始化数据库表")
    async with async_engine.begin() as conn:
        await conn.run_sync(BaseTable.metadata.create_all)


def configure_logging():
    # 清除默认的 handler
    logger.remove()

    __format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level}</level> | "
        "<cyan>{name}:{line}</cyan> - <level>{message}</level>"
    )
    __level = "DEBUG"
    # 配置 Console 日志
    logger.add(sys.stdout, level=__level, colorize=True, format=__format)

    # 配置文件日志
    log_file_retention = f"{settings.log.keep_days} days"
    log_file_path = (
        f"{settings.log.base_dir}/{settings.log.filename}.{settings.active_env}.{dt_to_str(pat=FMT_DATE)}.log"
    )

    logger.add(
        log_file_path,
        level=__level,
        rotation="00:00",
        retention=log_file_retention,
        compression="zip",
        format=__format,
    )


async def app_life_span(app: FastAPI):
    await __init_tables()
    yield
    print("===done===")
