"""
__author__ = <yanghu> yanghu@1000kx.com
__date__ = 2024-10-20
__version__ = 0.0.1
__description__ = 
"""

from fastapi import FastAPI


def app_life_span(app:FastAPI):
    print("starting...")
    yield
    print("done")