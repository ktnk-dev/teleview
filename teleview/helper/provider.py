# Types
from types import ModuleType
from typing import AsyncGenerator
from .. import exceptions

HEADERS: dict = {}
PROVIDER = False
VERSION: float = 2.0


class BaseProvider:
    REQUIRED_TELEVIEW_VERSION: float
    VERSION: float
    SUPPORTED: tuple

#     @staticmethod
#     async def getChannels(query: str | int) -> AsyncGenerator[models.constructor.ChannelConstructor, None]:
#         ...
    
#     @staticmethod 
#     async def getChannel(query: str | int) -> models.constructor.ChannelConstructor:
#         ...

#     @staticmethod
#     async def getPosts(channel: models.default.Channel) -> AsyncGenerator[models.constructor.PostConstructor, None]:
#         ...

#     @staticmethod 
#     async def getPost(channel: models.default.Channel, query: str | int) -> models.constructor.PostConstructor:
#         ...
    
#     @staticmethod
#     async def getComments(post: models.default.Post) -> AsyncGenerator[models.constructor.CommentConstructor, None]:
#         ...

#     @staticmethod
#     async def getComment(post: models.default.Post, query: str | int) -> models.constructor.CommentConstructor:
#         ...



def setProvider(module: ModuleType) -> None:
    """Set provider from provided module"""
    global PROVIDER
    provider: BaseProvider = module.Provider
    try: 
        if provider.REQUIRED_TELEVIEW_VERSION > VERSION:
            print(f'[teleview] Failed to load provider! Teleview v{provider.REQUIRED_TELEVIEW_VERSION} or newer required')
            raise exceptions.ProvderNotSupported()
    except:
        print(f'[teleview] Failed to load provider! REQUIRED_TELEVIEW_VERSION not specified')
        raise exceptions.ProvderNotSupported()

    PROVIDER = provider

def getProvider() -> BaseProvider:
    return PROVIDER

def setHeaders(headers: dict) -> None:
    """Set headers that will pass to requests"""
    global HEADERS
    HEADERS = headers

def getHeaders() -> dict:
    return HEADERS

