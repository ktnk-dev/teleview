import aiohttp, bs4, json
from aiohttp_socks import ProxyConnector as _pc
from typing import Any

from .caching import CacheBuffer as _cb
from .enums import CacheStrategy as _cs
from .provider import getProvider as _pb

_PROXY_URL = None

def setProxy(proxy_url: str | None):
    """### Set `http` proxy for all requests
    Format: `http://user:password@proxy_host:port`
    """
    global _PROXY_URL
    _PROXY_URL = proxy_url

class Request:
    def __init__(self, url: str, headers: dict = {}) -> None:
        """Async GET request to url with custom headers
After init you must call `await request.load()`
- "text" property contains url content
"""

        self.url: str = url
        self.headers: dict = headers
        self.text: str = False

    async def load(self) -> str:
        """Updates self.text and returns it"""
        
        if _cs.AutoByRequest in _pb().CACHE_STRATEGY:
            cached = _cb.get(self.url)
            if cached:
                self.text = cached
                return self.text

        args = {}
        if 'socks' in str(_PROXY_URL):
            args['connector'] = _pc.from_url(_PROXY_URL)
        if 'http' in str(_PROXY_URL):
            args['proxy'] = _PROXY_URL
        
        async with aiohttp.ClientSession(**args) as client:
            async with client.get(self.url, headers=self.headers, ssl=False) as resp: 
                self.text = await resp.text('utf-8')
        
        if _cs.AutoByRequest in _pb().CACHE_STRATEGY:
            _cb.set(self.url, self.text)
        
        return self.text

    def toBS(self) -> bs4.BeautifulSoup:
        """Generates BeautifulSoup object from self.text"""
        return bs4.BeautifulSoup(self.text, 'html.parser')
    
    def fromJSON(self) -> Any:
        """Loads JSON from self.text"""
        if not self.text: return {}
        return json.loads(self.text)
