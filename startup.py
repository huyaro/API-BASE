"""
__author__ = <yanghu> yanghu@1000kx.com
__date__ = 2024-10-27
__version__ = 0.0.1
__description__ = app 启动
"""

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=9091, reload=True)