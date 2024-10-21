"""
__author__ = <yanghu> yanghu@1000kx.com
__date__ = 2024-10-20
__version__ = 0.0.1
__description__ = app 入口
"""

from fastapi import FastAPI

from .api import routers
from .ctx import app_life_span

app = FastAPI(lifespan=app_life_span)

for r in routers:
    app.include_router(r)


