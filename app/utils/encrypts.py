"""
__author__ = <yanghu> yanghu@1000kx.com
__date__ = 2024-10-27
__version__ = 0.0.1
__description__ =
"""

import hashlib

from app.settings import STD_UTF8


def hash_md5(text: int | str) -> str:
    _text = text
    if isinstance(text, int):
        _text = str(text)
    return hashlib.md5(_text.encode(STD_UTF8)).hexdigest()
