import aiohttp, bs4, json
from typing import Any


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
        async with aiohttp.ClientSession() as client:
            async with client.get(self.url, headers=self.headers) as resp: 
                self.text = await resp.text('utf-8')
        
        return self.text

    def toBS(self) -> bs4.BeautifulSoup:
        """Generates BeautifulSoup object from self.text"""
        return bs4.BeautifulSoup(self.text, 'html.parser')
    
    def fromJSON(self) -> Any:
        """Loads JSON from self.text"""
        if not self.text: return {}
        return json.loads(self.text)
