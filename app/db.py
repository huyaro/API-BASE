"""
__author__ = <yanghu> yanghu@1000kx.com
__date__ = 2024-10-20
__version__ = 0.0.1
__description__ = 数据库及redis连接相关配置
"""
from contextlib import asynccontextmanager

import redis
from loguru import logger
from redis.asyncio import ConnectionPool, Redis
from sqlalchemy import Engine, event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.utils.converts import dumps_json

# =============================== DATABASE ===============================
ASYNC_DATABASE_URL = "postgresql+asyncpg://postgres:pgsql2023@localhost/example"
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=False,
    json_serializer=dumps_json,
    isolation_level="READ COMMITTED"
)
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    autoflush=False,
    class_=AsyncSession
)


async def use_db():
    async with AsyncSessionLocal() as session:
        yield session


# 不输出SQL 的表
ignore_tables = ["pg_catalog.pg_class"]


# 定义监听器函数
@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    if not any([True if tab in statement else False for tab in ignore_tables]):
        logger.debug(f"SQL    => {statement}")
        logger.debug(f"Params => {parameters}")


@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    if not any([True if tab in statement else False for tab in ignore_tables]):
        logger.info(f"Affected Rows  => {cursor.rowcount}")


# =============================== REDIS ===============================
REDIS_URL = "redis://localhost:6379/0"
redis_pool = ConnectionPool.from_url(REDIS_URL, max_connections=10)
# 异步redis
async_rds_pool = ConnectionPool.from_url(
    REDIS_URL,
    decode_responses=True,
    max_connections=10,
    health_check_interval=30,
    socket_timeout=5,  # 设置socket读取数据的超时时间（秒）
    socket_connect_timeout=5,  # 设置socket连接超时时间（秒）
    retry_on_timeout=True  # 在超时的情况下重新尝试连接
)
async_redis = Redis(connection_pool=async_rds_pool)


async def use_redis():
    """专门为fastapi的depends构建的依赖函数"""
    try:
        await async_redis.ping()
        yield async_redis
    except redis.exceptions.ConnectionError:
        yield Redis(connection_pool=async_rds_pool)


@asynccontextmanager
async def use_ctx_redis():
    """为普通异步函数中封装的上下文参数"""
    try:
        await async_redis.ping()
        yield async_redis
    except redis.exceptions.ConnectionError:
        yield Redis(connection_pool=async_rds_pool)


