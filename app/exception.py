"""
__author__ = <yanghu> yanghu@1000kx.com
__date__ = 2024-10-20
__version__ = 0.0.1
__description__ = 统一异常处理
"""
from starlette.requests import Request

from app.schemas import CommonResponse


class BizException(Exception):
    def __init__(self, code=0, msg='ok'):
        self.code = code
        self.msg = msg


async def biz_exception_handler(request: Request, exc: BizException):
    return CommonResponse.fail(exc.code, exc.msg)
