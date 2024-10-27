"""
__author__ = <huyaro> huyaro.dev@outlook.com
__date__ = 2024-10-27
__version__ = 0.0.1
__description__ = web 请求
"""
import time
import uuid
from typing import Optional

import httpx
from httpx import Auth
from loguru import logger
from ujson import JSONDecodeError

from app.utils.serials import dumps_json


class HttpxClient:

    def __init__(self):
        self._hooks = {"request": [self._logger_request], "response": [self._logger_response]}
        self._hooks_async = {"request": [self._logger_request_async], "response": [self._logger_response_async]}
        self._timeout = httpx.Timeout(30)

    @staticmethod
    async def _logger_request_async(request: httpx.Request):
        HttpxClient._logger_request(request=request)

    @staticmethod
    async def _logger_response_async(response: httpx.Response):
        await response.aread()
        HttpxClient.__logger_response_out(response=response)

    @staticmethod
    def _logger_response(response: httpx.Response):
        response.read()
        HttpxClient.__logger_response_out(response=response)

    @staticmethod
    def _logger_request(request: httpx.Request):
        # 在请求之前记录日志
        trace_id = uuid.uuid4()
        request.headers["X-Trace-ID"] = trace_id
        request.headers["start_time"] = str(time.time())  # 将开始时间存储在请求上下文中
        line = f"HttpxRequest[{trace_id}] => [{request.method}] | {request.url}"
        if request.content:
            line += f" | {dumps_json(request.content.decode('utf-8'))}"
        logger.info(line)

    @staticmethod
    def __logger_response_out(response: httpx.Response):
        # 在响应之后记录日志
        trace_id = response.request.headers.get("X-Trace-ID", "N/A")
        start_time = response.request.headers.get("start_time", None)
        duration = 0.00
        if start_time:
            duration = time.time() - float(start_time)  # 计算耗时

        # 有可能返回的是html无法被dumps
        try:
            resp_body = dumps_json(response.text)
        except JSONDecodeError:
            resp_body = response.text

        logger.debug(f"HttpxResponse[{trace_id}] => [{response.status_code}] | {resp_body}")
        logger.info(f"================Httpx[{trace_id}] Spend Time [{duration:.2f}S]=====================")

    def get(self, url: str, params: Optional[dict] = None) -> httpx.Response:
        with httpx.Client(event_hooks=self._hooks, timeout=self._timeout) as client:
            return client.get(url, params=params)

    def post(self, url: str, data: dict = None, auth: Auth | None = None) -> httpx.Response:
        with httpx.Client(event_hooks=self._hooks, timeout=self._timeout) as client:
            return client.post(url, json=data, auth=auth)

    async def get_async(self, url: str, params: Optional[dict] = None) -> httpx.Response:
        async with httpx.AsyncClient(event_hooks=self._hooks_async, timeout=self._timeout) as client:
            return await client.get(url, params=params)

    async def post_async(self, url: str, data: dict | None = None, auth: Auth | None = None) -> httpx.Response:
        async with httpx.AsyncClient(event_hooks=self._hooks_async, timeout=self._timeout) as client:
            return await client.post(url, json=data, auth=auth)


# 外部直接引用实例, 默认就是单例模式
httpxClient = HttpxClient()