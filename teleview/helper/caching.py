# from .enums import CacheStrategy as _cs
# from .provider import getProvider as _gp
import datetime as _dt
from typing import Any as _Any


_GLOBAL_CACHE_POOL: dict[str, tuple[_dt.datetime, _Any]] = {}
_GLOBAL_CACHE_TIMEOUT = _dt.timedelta(seconds=300) 
class CacheBuffer:
    @staticmethod
    def get(key):
        if not _GLOBAL_CACHE_TIMEOUT: return
        global _GLOBAL_CACHE_POOL
        
        v = _GLOBAL_CACHE_POOL.get(key)
        if not v: return 
        if v[0]+_GLOBAL_CACHE_TIMEOUT < _dt.datetime.now():
            CacheBuffer.clean()
            return
        return v[1]


    @staticmethod
    def set(key, value):
        if not _GLOBAL_CACHE_TIMEOUT: return
        global _GLOBAL_CACHE_POOL

        _GLOBAL_CACHE_POOL[key] = (_dt.datetime.now(), value) 
        
    @staticmethod
    def clean():
        if not _GLOBAL_CACHE_TIMEOUT: return
        global _GLOBAL_CACHE_POOL
        now = _dt.datetime.now()
        expired_keys = [key for key, (created, _) in _GLOBAL_CACHE_POOL.items() if created+_GLOBAL_CACHE_TIMEOUT < now]
        for key in expired_keys:
            del _GLOBAL_CACHE_POOL[key]
    
    @staticmethod
    def empty():
        if not _GLOBAL_CACHE_TIMEOUT: return
        global _GLOBAL_CACHE_POOL
        _GLOBAL_CACHE_POOL.clear()
        

def setCacheTimeout(timeout: int):
    """### Setting cache timeout
* `timeout`: The timeout value in seconds
    """
    global _GLOBAL_CACHE_TIMEOUT
    _GLOBAL_CACHE_TIMEOUT = _dt.timedelta(seconds=timeout) if timeout > 1 else None