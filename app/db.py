"""
__author__ = <huyaro> huyaro.dev@outlook.com
__date__ = 2024-10-20
__version__ = 0.0.1
__description__ = 数据库及redis连接相关配置
"""

from contextlib import asynccontextmanager
from typing import Any

import redis
from loguru import logger
from redis.asyncio import ConnectionPool, Redis
from sqlalchemy import Engine, event
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.model import BaseTable
from app.settings import settings
from app.utils.iterators import filter_dict_keys
from app.utils.serials import dumps_json

DB_POOL_SIZE = settings.database.pool_size
REDIS_POOL_SIZE = settings.redis.pool_size

# =============================== DATABASE ===============================
ASYNC_DATABASE_URL = settings.database.build_url()
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    pool_size=DB_POOL_SIZE,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=False,
    json_serializer=dumps_json,
    isolation_level="READ COMMITTED",
)
AsyncSessionLocal = sessionmaker(bind=async_engine, expire_on_commit=False, autoflush=False, class_=AsyncSession)


async def use_db():
    async with AsyncSessionLocal() as session:
        yield session


# 不输出SQL 的表
ignore_tables = ["pg_catalog.pg_class"]


# 定义监听器函数
@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    if not any([tab in statement for tab in ignore_tables]):
        logger.debug(f"SQL    => {statement}")
        logger.debug(f"Params => {parameters}")


@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    if not any([tab in statement for tab in ignore_tables]):
        logger.info(f"Affected Rows  => {cursor.rowcount}")


# =============================== REDIS ===============================
REDIS_URL = settings.redis.build_url()
redis_pool = ConnectionPool.from_url(REDIS_URL, max_connections=10)
# 异步redis
async_rds_pool = ConnectionPool.from_url(
    REDIS_URL,
    max_connections=REDIS_POOL_SIZE,
    decode_responses=True,
    health_check_interval=30,
    socket_timeout=5,  # 设置socket读取数据的超时时间（秒）
    socket_connect_timeout=5,  # 设置socket连接超时时间（秒）
    retry_on_timeout=True,  # 在超时的情况下重新尝试连接
)
async_redis = Redis(connection_pool=async_rds_pool)


async def dep_redis():
    """专门为fastapi的depends构建的依赖函数"""
    try:
        await async_redis.ping()
        yield async_redis
    except redis.exceptions.ConnectionError:
        yield Redis(connection_pool=async_rds_pool)


@asynccontextmanager
async def dep_async_redis():
    """为普通异步函数中封装的上下文参数"""
    try:
        await async_redis.ping()
        yield async_redis
    except redis.exceptions.ConnectionError:
        yield Redis(connection_pool=async_rds_pool)


async def pg_upsert(
    session: AsyncSession,
    table_type: type[BaseTable],
    values: list[dict[str, Any]],
    conflict_columns: set[str],
    ignore_columns: set[str] = None,
    batch_size=300,
) -> list[int]:
    """
        异步版本的upsert.

    :param session: AsyncSession
    :param table_type: 基于Base的声明式模型
    :param values: 要写入的值或模型
    :param conflict_columns: 模型中标记为unique的一列或多列
    :param ignore_columns: 要忽略update的列(一般是create_time,update_time之类的)
    :param batch_size: 单次写入多少数量. 默认300
    :return:
    """
    if not values:
        raise ValueError("values can't be empty")

    final_ignore_columns = ["id", "created_time", "updated_time"]
    if ignore_columns is not None:
        final_ignore_columns.extend(ignore_columns)

    fill_values = filter_dict_keys(values, exclude=final_ignore_columns)

    batch_result = []
    try:
        for i in range(0, len(fill_values), batch_size):
            batch_data = fill_values[i : i + batch_size]
            # 只有pg方言中导入的insert函数才有on_conflict_do_update方法
            insert_stmt = pg_insert(table_type).returning(table_type.id)
            update_columns = {
                col.name: col
                for col in insert_stmt.excluded
                if col.name not in [*conflict_columns, *final_ignore_columns]
            }

            upsert_stmt = insert_stmt.on_conflict_do_update(index_elements=conflict_columns, set_=update_columns)
            wait_res = await session.execute(upsert_stmt, batch_data)
            result = wait_res.all()
            batch_result.extend([_ids[0] for _ids in result])

        await session.commit()
        return batch_result
    except SQLAlchemyError as e:
        await session.rollback()
        raise e
