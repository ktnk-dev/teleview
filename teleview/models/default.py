# Types
from typing import AsyncGenerator
from datetime import datetime as Datetime

# Exceptions
from ..exceptions import *        
from ..helper.enums import Supported as _s
from ..helper.provider import getProvider

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


    async def toDict(self) -> dict:
        return {
            'url': self.url,
            'type': self.type,
            'mimetype': self.mimetype
        }

class Author:
    """Represents comment or post author"""
    __slots__ = ['name', 'picture']
    
    name: str
    """Author's name"""
    
    picture: Media | False
    """Author's profile picture"""
    
    def __init__(self, constructor) -> None:
        self.name: str = constructor.name
        self.picture: Media | False = constructor.picture.build() if constructor.picture else False
        
    async def toDict(self) -> dict:
        return {
            'name': self.name,
            'picture': (await self.picture.toDict()) if self.picture else False
        }
        
class Comment:
    """Represents post's comment"""
    __slots__ = ['post', 'id', 'url', 'text', 'media', 'author', 'datetime', '_iternal']
    
    post: Post    
    id: str | int | False 
    url: str | False 
    text: str | False
    media: list[Media]
    """Media attached to comment"""
    author: Author
    datetime: Datetime
    _iternal: dict
    """Any optional data that provider returned"""
    
    def __init__(self, constructor) -> None:
        self.post: Post = constructor.post
        self.id: str | int | False = constructor.id
        self.url: str | False = constructor.url
        self.text: str | False = constructor.text
        self.media: list[Media] = [media.build() for media in constructor.media]
        self.author: Author = constructor.author.build()
        self.datetime: Datetime = constructor.datetime

        self._iternal: dict = constructor.iternal
    

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

class Post:
    """Represents post's comment"""
    __slots__ = ['channel', 'author', 'id', 'url', 'text', 'views', 'media' 'datetime', '_iternal']
    
    channel: Channel    
    author: Author
    id: str | int | False 
    url: str | False 
    text: str | False
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
        self.id: str | int | False = constructor.id
        self.url: str | False = constructor.url
        self.text: str | False = constructor.text
        self.views: int = constructor.views
        self.media: list[Media] = [media.build() for media in constructor.media]
        self.datetime: Datetime = constructor.datetime

        self._iternal: dict = constructor.iternal

    async def getComment(self, query: str | int) -> Comment:
        """### Async function to get comment

Args:
* `query` [str | int]: something, that can be used to find your comment, depends on your provider

Return: `Comment`

Exceptions:
* `CommentNotFound`
* `NotSupported`

"""
        if _s.CommentOutput not in getProvider().SUPPORTED:
            raise NotSupported()

        constructor = await getProvider().getComment(self, query)
        return constructor.build()




    async def getComments(self, limit: int = 20) -> AsyncGenerator[Comment, None]:
        """### Async function to get comments

Args:
* `limit` [int >= 0] = 20

Return: `AsyncGenerator[Comment]`

Exceptions:
* `CommentNotFound`
* `NotSupported`

"""
        if _s.StreamCommentOutput not in getProvider().SUPPORTED:
            raise NotSupported()

        found = 0
        async for constructor in getProvider().getComments(self):
            found += 1
            yield constructor.build()
            if limit and found >= limit: break

    
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

class Channel:
    def __init__(self, constructor) -> None:
        self.id: str | int | False = constructor.id
        self.url: str | False = constructor.url
        self.name: str = constructor.name
        self.picture: Media | False = constructor.picture.build() if constructor.picture else False
        self.description: str | False = constructor.description
        self.subscribers: int = constructor.subscribers

        self._iternal: dict = constructor.iternal


    async def getPost(self, query: str | int) -> Post:
        """### Async function to get post

Args:
* `query` [str | int]: something, that can be used to find your post, depends on your provider

Return: `Post`

Exceptions:
* `PostNotFound`
* `NotSupported`

"""
        if _s.PostOutput not in getProvider().SUPPORTED:
            raise NotSupported()

        constructor = await getProvider().getPost(self, query)
        return constructor.build()




    async def getPosts(self, limit: int = 20) -> AsyncGenerator[Post, None]:
        """### Async function to get post

Args:
* `limit` [int >= 0] = 20; set to 0 to get all results if possible

Return: `AsyncGenerator[Post]`

Exceptions:
* `PostNotFound`
* `NotSupported`

"""
        if _s.StreamPostOutput not in getProvider().SUPPORTED:
            raise NotSupported()

        found = 0
        async for constructor in getProvider().getPosts(self):
            found += 1
            yield constructor.build()
            if limit and found >= limit: break
        


    async def toDict(self) -> dict:
        return {
            'id': self.id,
            'url': self.url,
            'name': self.name,
            'picture': (await self.picture.toDict()) if self.picture else False,
            'description': self.description,
            'subscribers': self.subscribers
        }