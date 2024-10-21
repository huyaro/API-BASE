"""
__author__ = <yanghu> yanghu@1000kx.com
__date__ = 2024-10-20
__version__ = 0.0.1
__description__ = 响应模型泛型
"""
from typing import Generic, Optional, TypeVar

import ujson
from pydantic import BaseModel
from starlette.responses import JSONResponse


class BaseSchema(BaseModel):
    __abstract__ = True

    class Config:
        from_attributes = True


T_SCHEMA = TypeVar("T_SCHEMA", bound=BaseSchema)


class CommonResponse(BaseModel, Generic[T_SCHEMA]):
    code: int = 0
    msg: str = "ok"
    data: Optional[T_SCHEMA] = None

    @staticmethod
    def ok(data: Optional[T_SCHEMA]) -> JSONResponse:
        content = ujson.dumps(CommonResponse(data=data).model_dump(by_alias=True), ensure_ascii=True)
        return JSONResponse(content=content, status_code=200)

    @staticmethod
    def fail(code: int, msg: str) -> JSONResponse:
        content = ujson.dumps(CommonResponse(code=code, msg=msg).model_dump(by_alias=True, exclude={'data'}), ensure_ascii=True)
        return JSONResponse(content=content, status_code=200)

