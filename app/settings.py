"""
__author__ = <yanghu> yanghu@1000kx.com
__date__ = 2024-10-20
__version__ = 0.0.1
__description__ = 读取配置文件
"""
from pathlib import Path
from typing import Any

from pydantic_settings import BaseSettings

APP_NAME = "API-BASE"
DIR_APP_ROOT = Path(__file__).parent.parent
DIR_LOG = DIR_APP_ROOT.joinpath("logs")
STD_UTF8 = "utf-8"


class RunEnv:
    DEV = "dev"
    PROD = "prod"


class EnvSettings(BaseSettings):
    """
        当前环境配置
    """
    active: str = RunEnv.DEV

    class Config:
        env_file = DIR_APP_ROOT.joinpath(".env")
        env_file_encoding = STD_UTF8


# 加载主配置文件（.env）
env_settings = EnvSettings()
APP_ENV = RunEnv.PROD if env_settings.active.lower() == "prod" else RunEnv.DEV

if APP_ENV == RunEnv.PROD:
    print(r"""
██████╗ ██████╗  ██████╗ ██████╗ 
██╔══██╗██╔══██╗██╔═══██╗██╔══██╗
██████╔╝██████╔╝██║   ██║██║  ██║
██╔═══╝ ██╔══██╗██║   ██║██║  ██║
██║     ██║  ██║╚██████╔╝██████╔╝
╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═════╝                                                                       
""")
else:
    print(r""" 
.___________. _______     _______.___________.
|           ||   ____|   /       |           |
`---|  |----`|  |__     |   (----`---|  |----`
    |  |     |   __|     \   \       |  |     
    |  |     |  |____.----)   |      |  |     
    |__|     |_______|_______/       |__|
""")


class InitSettings(BaseSettings):
    """
    数据库与Redis 连接配置
    """
    db_host: str
    db_port: int = 5432
    db_username: str
    db_password: str
    db_name: str

    redis_host: str
    redis_port: int = 6379
    redis_password: str
    redis_db: int = 0

    class Config:
        env_file = DIR_APP_ROOT.joinpath(f"__{APP_ENV}.env")
        env_file_encoding = STD_UTF8


init_settings = InitSettings()


class BizSettings(BaseSettings):
    """
        业务配置. 从数据库中读取后按module 放到不同的模块变量中
    """
    mod_api: dict[str, Any]
    mod_user: dict[str, Any]


if __name__ == '__main__':
    print(init_settings)