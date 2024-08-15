# Types
from typing import AsyncGenerator
from datetime import datetime as Datetime

# Exceptions
from ..exceptions import *        
from ..helper import supported
from ..helper.provider import getProvider

class Media:
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
    def __init__(self, constructor) -> None:
        self.name: str = constructor.name
        self.picture: Media | False = constructor.picture.build() if constructor.picture else False
        
    async def toDict(self) -> dict:
        if self.picture:
            return {
                'name': self.name,
                'picture': await self.picture.toDict()
            }
        else:
            return {
                'name': self.name,
                'picture': False
            }

class Comment:
    def __init__(self, constructor) -> None:
        self.post: Post = constructor.post
        
        self.text: str | False = constructor.text
        self.media: list[Media] = [media.build() for media in constructor.media]
        self.author: Author = constructor.author.build()
        self.datetime: Datetime = constructor.datetime

        self._iternal: dict = constructor.iternal
    

    async def toDict(self) -> dict:
        return {
            'post': await self.post.toDict(),
            'author': await self.author.toDict(),
            'text': self.text,
            'media': [await media.toDict() for media in self.media],
            'datetime': self.datetime.strftime('%Y.%m.%d %H:%M:%S')
        }

class Post:
    def __init__(self, constructor) -> None:
        self.channel: Channel = constructor.channel
        self.url: str = constructor.url
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
        if supported.CommentOutput not in getProvider().SUPPORTED:
            raise NotSupported()

        constructor = await getProvider().getComment(self, query)
        return constructor.build()




    async def getComments(self, limit: int= 20) -> AsyncGenerator[Comment, None]:
        """### Async function to get comments

Args:
* `limit` [int >= 0] = 20

Return: `AsyncGenerator[Comment]`

Exceptions:
* `CommentNotFound`
* `NotSupported`

"""
        if supported.StreamCommentOutput not in getProvider().SUPPORTED:
            raise NotSupported()

        found = 0
        async for constructor in getProvider().getComments(self):
            found += 1
            yield constructor.build()
            if limit and found >= limit: break

    
    async def toDict(self) -> dict:
        return {
            'channel': await self.channel.toDict(),
            'url': self.url,
            'text': self.text,
            'views': self.views,
            'media': [await media.toDict() for media in self.media],
            'datetime': self.datetime.strftime('%Y.%m.%d %H:%M:%S')
        }

class Channel:
    def __init__(self, constructor) -> None:
        self.url: str = constructor.url
        self.name: str = constructor.name
        self.picture: Media | False = False

        if constructor.picture:
            self.picture: Media | False = constructor.picture.build()

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
        if supported.PostOutput not in getProvider().SUPPORTED:
            raise NotSupported()

        constructor = await getProvider().getPost(self, query)
        return constructor.build()




    async def getPosts(self, limit: int = 20) -> AsyncGenerator[Post, None]:
        """### Async function to get post

Args:
* `limit` [int >= 0] = 20

Return: `AsyncGenerator[Post]`

Exceptions:
* `PostNotFound`
* `NotSupported`

"""
        if supported.StreamPostOutput not in getProvider().SUPPORTED:
            raise NotSupported()

        found = 0
        async for constructor in getProvider().getPosts(self):
            found += 1
            yield constructor.build()
            if limit and found >= limit: break
        


    async def toDict(self) -> dict:
        if self.picture:
            return {
                'url': self.url,
                'name': self.name,
                'picture': await self.picture.toDict(),
                'description': self.description,
                'subscribers': self.subscribers
            }
        else:
            return {
                'url': self.url,
                'name': self.name,
                'picture': False,
                'description': self.description,
                'subscribers': self.subscribers
            }