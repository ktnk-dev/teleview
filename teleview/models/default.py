# Types
from typing import AsyncGenerator
from datetime import datetime as Datetime

# Exceptions
from ..exceptions import *        
from ..helper.enums import Supported as _s
from ..helper.provider import getProvider
from ..docs import (ModelDocumentation as _ModelDocumentation, CallDocumentation as _CallDocumentation)

@_ModelDocumentation({
    'url': 'Direct URL to media',
    'type': "Kind of media, <b>depends on provider</b>"
}, index=999)
class Media:
    """Represents any media content (profile picuters, photos in posts, etc)"""
    __slots__ = ['url', 'type', 'mimetype']
    
    url: str 
    """Direct URL to media"""
    
    type: str
    """*Kind* of media `depends on provider`"""
    
    mimetype: str
    
    def __init__(self, constructor) -> None:
        self.url: str = constructor.url
        self.type: str = constructor.type
        self.mimetype: str = constructor.mimetype

    @_CallDocumentation('Media',[])
    async def toDict(self) -> dict:
        return {
            'url': self.url,
            'type': self.type,
            'mimetype': self.mimetype
        }

@_ModelDocumentation({
    'name': "Author's name",
    'picture?': "Author's profile picture"
}, index=999)
class Author:
    """Represents comment or post author"""
    __slots__ = ['name', 'picture']
    
    name: str
    """Author's name"""
    
    picture: Media | bool
    """Author's profile picture"""
    
    def __init__(self, constructor) -> None:
        self.name: str = constructor.name
        self.picture: Media | bool = constructor.picture.build() if constructor.picture else False
    
    @_CallDocumentation('Author',[])
    async def toDict(self) -> dict:
        return {
            'name': self.name,
            'picture': (await self.picture.toDict()) if self.picture else False  # pyright: ignore[reportAttributeAccessIssue]
        }



@_ModelDocumentation({
    'id?': '',
    'url?': '',
    'text?': '',
    'media': 'Media attached to comment',
    '_iternal': 'Any optional data that provider returned'
}, index=1)
class Channel:
    """Represents channel"""

    __slots__ = ['id', 'url', 'name', 'picture', 'description', 'subscribers', '_iternal']
    
    id: str | int | bool 
    url: str | bool 
    name: str
    picture: Media | bool
    """Channel's picture"""
    
    description: str | bool
    subscribers: int
    _iternal: dict
    """Any optional data that provider returned"""
    
    def __init__(self, constructor) -> None:
        self.id: str | int | bool = constructor.id
        self.url: str | bool = constructor.url
        self.name: str = constructor.name
        self.picture: Media | bool = constructor.picture.build() if constructor.picture else False
        self.description: str | bool = constructor.description
        self.subscribers: int = constructor.subscribers

        self._iternal: dict = constructor.iternal


    @_CallDocumentation(
        'Channel',['PostOutput'],
        exceptions=[PostNotFound, NotSupported]
    )
    async def getPost(self, query: str | int) -> 'Post':
        """Async function to get channel's post by query"""
        if _s.PostOutput not in getProvider().SUPPORTED:
            raise NotSupported()

        constructor = await getProvider().getPost(self, query) # pyright: ignore[reportAttributeAccessIssue]
        return constructor.build()



    @_CallDocumentation(
        'Channel', ['StreamPostOutput'],
        exceptions=[PostNotFound, NotSupported],
        args={'limit': 'Amount of posts, set to 0 to get all posts if possible'}
    )
    async def getPosts(self, limit: int = 20) -> AsyncGenerator['Post', None]:
        """Async function to get posts from channel"""
        if _s.StreamPostOutput not in getProvider().SUPPORTED:
            raise NotSupported()

        found = 0
        async for constructor in getProvider().getPosts(self): # pyright: ignore[reportAttributeAccessIssue]
            found += 1
            yield constructor.build()
            if limit and found >= limit: break
        

    @_CallDocumentation('Channel', [])
    async def toDict(self) -> dict:
        return {
            'id': self.id,
            'url': self.url,
            'name': self.name,
            'picture': (await self.picture.toDict()) if self.picture else False, # pyright: ignore[reportAttributeAccessIssue]
            'description': self.description,
            'subscribers': self.subscribers
        }

@_ModelDocumentation({
    'id?': '',
    'url?': '',
    'text?': '',
    'media': 'Media attached to comment',
    'views': 'Amount of views',
    '_iternal': 'Any optional data that provider returned',
}, index=3)
class Post:
    """Represents post's comment"""
    __slots__ = ['channel', 'author', 'id', 'url', 'text', 'views', 'media', 'datetime', '_iternal']
    
    channel: Channel    
    author: Channel | Author
    id: str | int | bool 
    url: str | bool 
    text: str | bool
    views: int
    """Amount of views"""
    media: list[Media]
    """Media attached to post"""
    datetime: Datetime
    _iternal: dict
    """Any optional data that provider returned"""
    
    def __init__(self, constructor) -> None:
        self.channel: Channel = constructor.channel
        self.author: Channel | Author = constructor.author.build() if constructor.author else self.channel
        self.id: str | int | bool = constructor.id
        self.url: str | bool = constructor.url
        self.text: str | bool = constructor.text
        self.views: int = constructor.views
        self.media: list[Media] = [media.build() for media in constructor.media]
        self.datetime: Datetime = constructor.datetime

        self._iternal: dict = constructor.iternal

    @_CallDocumentation(
        'Post', ['CommentOutput'],
        exceptions=[CommentNotFound, NotSupported],
    )
    async def getComment(self, query: str | int) -> 'Comment':
        """Async function to get post's comment by query"""
        if _s.CommentOutput not in getProvider().SUPPORTED:
            raise NotSupported()

        constructor = await getProvider().getComment(self, query) # pyright: ignore[reportAttributeAccessIssue]
        return constructor.build()



    @_CallDocumentation(
        'Post', ['StreamCommentOutput'],
        exceptions=[CommentNotFound, NotSupported],
        args={'limit': 'Amount of comments, set to 0 to get all comments if possible'}
    )
    async def getComments(self, limit: int = 20) -> AsyncGenerator['Comment', None]:
        """Async function to get comments from post"""
        if _s.StreamCommentOutput not in getProvider().SUPPORTED:
            raise NotSupported()

        found = 0
        async for constructor in getProvider().getComments(self): # pyright: ignore[reportAttributeAccessIssue]
            found += 1
            yield constructor.build()
            if limit and found >= limit: break

    @_CallDocumentation('Post', [])
    async def toDict(self) -> dict:
        return {
            'channel': await self.channel.toDict(),
            'author': await self.author.toDict(),
            'id': self.id,
            'url': self.url,
            'text': self.text,
            'views': self.views,
            'media': [await media.toDict() for media in self.media],
            'datetime': self.datetime.strftime('%Y.%m.%d %H:%M:%S')
        }


@_ModelDocumentation({
    'id?': '',
    'url?': '',
    'text?': '',
    'media': 'Media attached to comment',
    '_iternal': 'Any optional data that provider returned'
}, index=3)
class Comment:
    """Represents post's comment"""
    __slots__ = ['post', 'id', 'url', 'text', 'media', 'author', 'datetime', '_iternal']
    
    post: Post
    id: str | int | bool
    url: str | bool
    text: str | bool
    media: list[Media]
    """Media attached to comment"""
    author: Author
    datetime: Datetime
    _iternal: dict
    """Any optional data that provider returned"""
    
    def __init__(self, constructor) -> None:
        self.post: Post = constructor.post
        self.id: str | int | bool = constructor.id
        self.url: str | bool = constructor.url
        self.text: str | bool = constructor.text
        self.media: list[Media] = [media.build() for media in constructor.media]
        self.author: Author = constructor.author.build()
        self.datetime: Datetime = constructor.datetime

        self._iternal: dict = constructor.iternal
    
    @_CallDocumentation('Comment', [])
    async def toDict(self) -> dict:
        return {
            'post': await self.post.toDict(),
            'id': self.id,
            'url': self.url,
            'author': await self.author.toDict(),
            'text': self.text,
            'media': [await media.toDict() for media in self.media],
            'datetime': self.datetime.strftime('%Y.%m.%d %H:%M:%S')
        }
