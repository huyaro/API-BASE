"""
__author__ = <huyaro> huyaro.dev@outlook.com
__date__ = 2024-10-20
__version__ = 0.0.1
__description__ = 统一异常处理
"""
from fastapi import FastAPI, HTTPException
from loguru import logger
from starlette.requests import Request

from app.ctx import APIResponse


class BizException(RuntimeError):
    def __init__(self, code=999, msg='Server exception occurred'):
        self.code = code
        self.msg = msg


async def biz_exception_handler(request: Request, exc: BizException):
    return APIResponse.failed(exc.code, exc.msg)


async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}")
    if isinstance(exc, ValueError):
        return APIResponse.failed(400, msg=f"{exc.args}")
    elif isinstance(exc, HTTPException):
        return APIResponse.failed(exc.status_code, msg=f"{exc.detail}")
    else:
        return APIResponse.failed(900, msg=f"{exc}")


def register_exception_handler(app: FastAPI):
    app.add_exception_handler(BizException, biz_exception_handler)
    app.add_exception_handler(Exception, global_exception_handler)