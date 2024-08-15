# Types
from .models import default
from typing import AsyncGenerator

# Helper
from .helper.provider import getProvider
from .helper import supported

# Exceptions
from . import exceptions

async def getChannels(query: str | int, limit: int = 0) -> AsyncGenerator[default.Channel, None]:
    """### Async function to search channels

Args:
* `query` [str | int]: something, that can be used to find your channel, depends on your provider
* `limit` [int >= 0]: channels output limit

Return: `Generator[Channel]`

Exceptions:
* `ChannelNotFound`
* `NotSupported`

"""
    if supported.StreamChannelOutput not in getProvider().SUPPORTED:
        raise exceptions.NotSupported()

    found = 0
    async for constructor in getProvider().getChannels(query):
        found += 1
        yield constructor.build()
        if limit and found >= limit: break


async def getChannel(query: str | int) -> default.Channel:
    """### Async function to get channel

Args:
* `query` [str | int]: something, that can be used to find your channel, depends on your provider

Return: `Channel`

Exceptions:
* `ChannelNotFound`

"""
    constructor = await getProvider().getChannel(query)
    return constructor.build()


async def getPosts(channel: default.Channel, limit: int = 20) -> AsyncGenerator[default.Post, None]:
    """### Async function to get post

Args:
* `channel` [Channel]
* `limit` [int >= 0] = 20

Return: `AsyncGenerator[Post]`

Exceptions:
* `PostNotFound`
* `NotSupported`

"""
    if supported.StreamPostOutput not in getProvider().SUPPORTED:
        raise exceptions.NotSupported()

    found = 0
    async for constructor in getProvider().getPosts(channel):
        found += 1
        yield constructor.build()
        if limit and found >= limit: break





async def getPost(channel: default.Channel, query: str | int) -> default.Post:
    """### Async function to get post

Args:
* `channel` [Channel]
* `query` [str | int]: something, that can be used to find your post, depends on your provider

Return: `Post`

Exceptions:
* `PostNotFound`
* `NotSupported`

"""
    if supported.PostOutput not in getProvider().SUPPORTED:
        raise exceptions.NotSupported()

    constructor = await getProvider().getPost(channel, query)
    return constructor.build()



async def getComments(post: default.Post, limit: int = 20) -> AsyncGenerator[default.Comment, None]:
    """### Async function to get comments

Args:
* `post` [Post]
* `limit` [int >= 0] = 20

Return: `AsyncGenerator[Comment]`

Exceptions:
* `CommentNotFound`
* `NotSupported`

"""
    if supported.StreamCommentOutput not in getProvider().SUPPORTED:
        raise exceptions.NotSupported()

    found = 0
    async for constructor in getProvider().getComments(post):
        found += 1
        yield constructor.build()
        if limit and found >= limit: break







async def getComment(post: default.Post, query: str | int) -> default.Comment:
    """### Async function to get comment

Args:
* `post` [Post]
* `query` [str | int]: something, that can be used to find your comment, depends on your provider

Return: `Comment`

Exceptions:
* `CommentNotFound`
* `NotSupported`

"""
    if supported.CommentOutput not in getProvider().SUPPORTED:
        raise exceptions.NotSupported()

    constructor = await getProvider().getComment(post, query)
    return constructor.build()


