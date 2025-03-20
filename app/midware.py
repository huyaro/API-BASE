"""
__author__ = <huyaro> huyaro.dev@outlook.com
__date__ = 2024-10-27
__version__ = 0.0.1
__description__ = 中间件
"""

import json
from typing import Any, Callable

from fastapi import FastAPI
from fastapi_cache import Coder, FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from loguru import logger
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from app.db import async_redis
from app.utils.encrypts import hash_md5
from app.utils.serials import dumps_json, loads_json


def register_middleware_cors(app: FastAPI):
    logger.info("...注册　CORS 中间件")
    origins = ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )


# ===============cache插件处理==============
def __md5_key_builder(
    func: Callable[..., Any],
    namespace: str = "",
    *,
    request: Request | None = None,
    response: Response | None = None,
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
) -> str:
    def is_serializable(obj):
        try:
            json.dumps(obj)
            return True
        except TypeError:
            return False

    # 根据请求的 path、query 参数等构建唯一的缓存键
    hash_keys = []
    if namespace == "":
        namespace = biz_settings.pk_cache_ns

    # 具体的key
    key = f"{namespace}:{request.url.path}" if request and request.url else f"{namespace}:{func.__name__}"

    if args:
        hash_keys.extend([arg for arg in args if is_serializable(arg)])
    if kwargs:
        hash_keys.extend([arg for arg in kwargs.values() if is_serializable(arg)])

    if hash_keys:
        key = f"{key}:{hash_md5("".join(hash_keys))}"

    return key


class UJsonCoder(Coder):
    @classmethod
    def encode(cls, value: Any) -> str:
        if isinstance(value, JSONResponse):
            return value.body
        return dumps_json(value)

    @classmethod
    def decode(cls, value: str) -> Any:
        return loads_json(value)


def register_plugin_cache():
    logger.info("...注册 FastAPI-cache2 插件")
    FastAPICache.init(
        RedisBackend(async_redis),
        prefix="api-cache",
        coder=UJsonCoder,
        key_builder=__md5_key_builder,
    )
