"""
__author__ = <huyaro> huyaro.dev@outlook.com
__date__ = 2024-10-20
__version__ = 0.0.1
__description__ = 读取配置文件
"""

import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError
from pydantic_settings import BaseSettings

APP_NAME = "API-BASE"
DIR_APP_ROOT = Path(__file__).parent.parent
DIR_LOG = DIR_APP_ROOT.joinpath("logs")
STD_UTF8 = "utf-8"
DEFAULT_ENV_FILE = DIR_APP_ROOT.joinpath("app.env")


class DatabaseConfig(BaseModel):
    category: str = "postgresql"
    host: str = "127.0.0.1"
    port: int = 5432
    username: str
    password: str
    db: str
    pool_size: int = 10
    use_async: bool = False

    def build_url(self) -> str:
        """生成数据库连接 URL（支持主流关系型数据库）"""

        DRIVER_MAP = {
            "postgresql": {"sync": "psycopg2", "async": "asyncpg"},
            "mysql": {"sync": "pymysql", "async": "aiomysql"},
            "mariadb": {"sync": "pymysql", "async": "asyncmy"},
            "oracle": {"sync": "cx_oracle", "async": "oracledb"},
            "mssql": {
                "sync": "pyodbc",
                "async": "asyncpyodbc",  # 需要安装额外驱动
            },
        }

        # 验证数据库类型
        if self.category not in DRIVER_MAP:
            raise ValueError(f"Unsupported database: {self.category}")

        # 获取驱动配置
        driver_type = "async" if self.use_async else "sync"
        driver = DRIVER_MAP[self.category][driver_type]

        # 构建连接组件
        driver_prefix = f"+{driver}" if driver else ""
        auth = f"{self.username}:{self.password}@" if self.username and self.password else ""
        port = f":{self.port}" if self.port else ""

        # 特殊数据库处理
        if self.category == "oracle":
            # Oracle 使用 service_name 格式
            return f"oracle{driver_prefix}://{auth}{self.host}{port}/?service_name={self.db}"
        elif self.category == "mssql":
            # MSSQL 需要指定 ODBC 驱动
            odbc_params = "?driver=ODBC+Driver+17+for+SQL+Server"
            return f"mssql{driver_prefix}://{auth}{self.host}{port}/{self.db}{odbc_params}"
        else:
            # 标准格式
            return f"{self.category}{driver_prefix}://{auth}{self.host}{port}/{self.db}"


class RedisConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 6379
    password: str | None
    db: int = 0
    pool_size: int = 10

    def build_url(self) -> str:
        return f"redis://{self.host}:{self.port}/{self.db}"


class LogConfig(BaseModel):
    filename: str = "app"
    level: str = "INFO"
    base_dir: str = f"{DIR_LOG}"
    keep_days: int = 7


# --------------------------
# 配置加载主类
# --------------------------
class AppSettings:
    _instance = None  # 单例实例引用

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True

        self.active_env: str | None = None

        self.database: DatabaseConfig
        self.redis: RedisConfig
        self.log: LogConfig

        self.extra: dict[str, str] = {}

        # 加载流程
        self._load_config_files()
        self._parse_config()

    def _load_config_files(self):
        """加载并合并环境配置文件"""
        # 1. 加载默认配置
        if not DEFAULT_ENV_FILE.exists():
            raise FileNotFoundError(f"未找到 {DEFAULT_ENV_FILE} 文件, 请先创建配置文件")
        load_dotenv(DEFAULT_ENV_FILE, override=False)

        # 2. 加载环境特定配置
        self.active_env = os.getenv("ACTIVE_ENV")
        if self.active_env:
            env_file = DIR_APP_ROOT / f"app_{self.active_env}.env"
            if not env_file.exists():
                raise ValueError(f"未找到环境 {self.active_env} 配置文件: {env_file}")
            load_dotenv(env_file, override=True)

    def _parse_config(self):
        """解析环境变量到结构化配置"""
        # 提取所有环境变量（转换为小写）
        env_vars = {k.lower(): v for k, v in os.environ.items()}

        # 解析 Database 配置
        database_vars = self._extract_vars(env_vars, prefix="database_")
        try:
            self.database = DatabaseConfig(**database_vars)
        except ValidationError as e:
            raise ValueError(f"Invalid database config: {e}") from e

        # 解析 Redis 配置
        redis_vars = self._extract_vars(env_vars, prefix="redis_")
        try:
            self.redis = RedisConfig(**redis_vars)
        except ValidationError as e:
            raise ValueError(f"Invalid redis config: {e}") from e

        # 解析 Log 配置
        log_vars = self._extract_vars(env_vars, prefix="log_")
        try:
            self.log = LogConfig(**log_vars)
        except ValidationError as e:
            raise ValueError(f"Invalid log config: {e}") from e

        # 存储其他配置项
        exclude_prefix = ("database_", "redis_", "log_")
        self.extra = {k: v for k, v in env_vars.items() if not k.startswith(exclude_prefix)}

    @staticmethod
    def _extract_vars(env_vars: dict[str, str], prefix: str) -> dict[str, str]:
        """提取指定前缀的变量并去除前缀"""
        return {key[len(prefix) :]: value for key, value in env_vars.items() if key.startswith(prefix)}

    def show_config(self):
        """打印当前配置详情"""
        print(f"\n{' Active Environment ':~^40}")
        print(self.active_env or "default")

        print(f"\n{' Database Config ':~^40}")
        print(self.database.model_dump_json())

        print(f"\n{' Redis Config ':~^40}")
        print(self.redis.model_dump_json())

        print(f"\n{' Log Config ':~^40}")
        print(self.log.model_dump_json())

        print(f"\n{' Extra Config ':~^40}")
        for k, v in self.extra.items():
            print(f"{k}: {v}")


settings = AppSettings()
if __name__ == "__main__":
    settings.show_config()


class BizSettings(BaseSettings):
    """
    业务配置. 从数据库中读取后按module 放到不同的模块变量中
    """

    pk_cache_ns: str = "public:settings"
    mod_keyword: str = "__mod__"

    __mod__api: dict[str, Any] = {}
    __mod__user: dict[str, Any] = {}

    def get_module_names(self) -> list[str]:
        return [
            name.replace(self.mod_keyword, "").upper()
            for name, _ in self.model_fields
            if name.startswith(self.mod_keyword)
        ]


biz_settings = BizSettings()
