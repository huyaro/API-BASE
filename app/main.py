"""
__author__ = <huyaro> huyaro.dev@outlook.com
__date__ = 2024-10-20
__version__ = 0.0.1
__description__ = app 入口
"""

from fastapi import FastAPI
from loguru import logger

from .api import routers
from .ctx import app_life_span, configure_logging
from .exception import register_exception_handler
from .midware import register_middleware_cors, register_plugin_cache

app = FastAPI(lifespan=app_life_span)

# 加载所有模块路由
for r in routers:
    logger.info(f"...预加载路由: {r.prefix}")
    app.include_router(r)

# 日志处理器
configure_logging()

# 异常处理器
register_exception_handler(app)

# CORS
register_middleware_cors(app)

# Cache2
register_plugin_cache()
