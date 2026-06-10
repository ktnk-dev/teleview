# Types
from .models import default
from typing import AsyncGenerator

# Helper
from .helper.provider import getProvider
from .helper.enums import Supported as _s
from .docs import CallDocumentation as _d
# Exceptions
from . import exceptions

@_d(
    'teleview', ['StreamChannelOutput'],
    args={'limit': 'Amount of channels to find, set to 0 to get all channels'},
    exceptions=[exceptions.NotSupported],index=0
)
async def getChannels(query: str | int, limit: int = 0) -> AsyncGenerator[default.Channel, None]:
    """Async function to get multiple channels by query"""
    if _s.StreamChannelOutput not in getProvider().SUPPORTED:
        raise exceptions.NotSupported()

    found = 0
    async for constructor in getProvider().getChannels(query):
        found += 1
        yield constructor.build()
        if limit and found >= limit: break

@_d('teleview', [], exceptions=[exceptions.ChannelNotFound], index=1)
async def getChannel(query: str | int) -> default.Channel:
    """Async function to get single channel by query"""
    constructor = await getProvider().getChannel(query)
    return constructor.build()

@_d(
    'teleview', [],
    alias='Channel.getPosts',
    index=2
)
async def getPosts(channel: default.Channel, limit: int = 20) -> AsyncGenerator[default.Post, None]:
    """Alias to `Channel.getPosts`"""
    async for data in channel.getPosts(limit): yield data


@_d(
    'teleview', [],
    alias='Channel.getPost',
    index=3
)
async def getPost(channel: default.Channel, query: str | int) -> default.Post:
    """Alias to `Channel.getPost`"""
    return await channel.getPost(query)

@_d(
    'teleview', [],
    alias='Post.getComments',
    index=4
)
async def getComments(post: default.Post, limit: int = 20) -> AsyncGenerator[default.Comment, None]:
    """Alias to `Post.getComments`"""
    async for data in post.getComments(limit): yield data


@_d(
    'teleview', [],
    alias='Post.getComment',
    index=5
)
async def getComment(post: default.Post, query: str | int) -> default.Comment:
    """Alias to `Post.getComment`"""
    return await post.getComment(query)

