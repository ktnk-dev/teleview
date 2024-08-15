# Supported calls
from ..helper.supported import *

# Constructors and default types
from ..models.constructor import *

# Exceptions
from ..exceptions import *

# Types
from typing import AsyncGenerator

# Get headers
#? You can use user-provided headers to pass them in Request's
from ..helper.provider import getHeaders

# Get Request class, helps to deal with request
#? More info can be found in Docs > Creating Provider > Request
from ..helper.web import Request

# Put random data just to show that this provider works
import random 
import datetime

#! Name MUST be "Provider". Any other will be ignored
class Provider:
    """This is Demo provider, just to showcase the code and understand how it works"""

    #? Required teleview version in float
    #! If not specified: raise ProvderNotSupported
    #! If teleview version lower: raise ProvderNotSupported
    REQUIRED_TELEVIEW_VERSION: float = 2.0
    

    #? Your Provider version. Can be any float
    #! If not specified: nothing happens
    VERSION: float = 0.1

    #? List (tuple) of supported calls
    #? Supported calls can be found in teleview.helper.supported
    #? Your provider must fetch at-least channels (thats why it doesnt need to include in SUPPORTED)
    #! If something not included in SUPPORTED: even if call exist, it will raise NotSupported
    SUPPORTED: tuple = (
        StreamChannelOutput, 
        StreamPostOutput, 
        StreamCommentOutput, 
        PostOutput, 
        CommentOutput
    )

    @staticmethod #! StreamChannelOutput required in SUPPORTED
    async def getChannels(query: str | int) -> AsyncGenerator[ChannelConstructor, None]:
        #? Query can be string or integer depends on your platform
        #* string example: channel name, channel url
        #* integer example: channel id

        #! You can raise ChannelNotFound here if no channels found
        if random.random() < 0.05: raise ChannelNotFound()

        for _ in range(random.randint(5, 15)):
            
            channel = ChannelConstructor()
            channel.setIternal({'id': random.randint(10000, 99999)})

            randomNumber = random.randint(1000, 9999)
            channel.setUrl(f'https://example.com/channels/@{query}{randomNumber}')
            channel.setName(f'{query} {randomNumber}')

            channel.setSubscribers(random.randint(0, 99))

            #! You MUST yield result, instead returning list of results
            yield channel
        

    @staticmethod 
    async def getChannel(query: str | int) -> ChannelConstructor:
        #? Query can be string or integer depends on your platform
        #* string example: channel name, channel url
        #* integer example: channel id

        if random.random() < 0.05: raise ChannelNotFound()

        channel = ChannelConstructor()
        channel.setIternal({'id': random.randint(10000, 99999)})

        channel.setUrl(f'https://example.com/channels/@{query}')
        channel.setName(f'{query} {random.randint(1000, 9999)}')
        channel.setSubscribers(random.randint(0, 99))

        return channel


    @staticmethod #! StreamPostOutput required in SUPPORTED
    async def getPosts(channel: Channel) -> AsyncGenerator[PostConstructor, None]:
        #? limit handled by teleview lib, just yield ALL posts in channel from newest to oldest

        if random.random() < 0.05: raise PostNotFound()

        for _ in range(random.randint(20, 40)):
            randomNumber = random.randint(1000, 9999)

            post = PostConstructor(channel)
            post.setIternal({'id': randomNumber})

            post.setUrl(f'{channel.url}/posts/{randomNumber}')
            post.setDatetime(datetime.datetime.now())
            post.setViews(random.randint(0, 999))

            post.setText(f'This is pretty text {randomNumber}')

            mediaList = []
            for _ in range(random.randint(0, 3)):
                media = MediaConstructor()
                
                if random.random() < 0.3:
                    media.setUrl(f'{post.url}/download/{random.randint(100000,999999)}.ogg')
                    media.setType('voice_message')
                    media.setMimetype('audio/ogg')

                else: 
                    media.setUrl(f'{post.url}/download/{random.randint(100000,999999)}.jpeg')
                    media.setType('photo')
                    media.setMimetype('image/jpeg')

                mediaList.append(media)

            post.setMedia(mediaList)

            yield post

    @staticmethod #! PostOutput required in SUPPORTED
    async def getPost(channel: Channel, query: str | int) -> PostConstructor:
        #? For example query: int (post id)
        if type(query) != int: raise PostNotFound()

        if random.random() < 0.05: raise PostNotFound()

        post = PostConstructor(channel)
        post.setIternal({'id': query})

        post.setUrl(f'{channel.url}/posts/{query}')
        post.setDatetime(datetime.datetime.now())
        post.setViews(random.randint(0, 999))

        post.setText(f'This is pretty text {random.randint(0, 999)}')

        mediaList = []
        for _ in range(random.randint(0, 3)):
            media = MediaConstructor()
            
            if random.random() < 0.3:
                media.setUrl(f'{post.url}/download/{random.randint(100000,999999)}.ogg')
                media.setType('voice_message')
                media.setMimetype('audio/ogg')

            else: 
                media.setUrl(f'{post.url}/download/{random.randint(100000,999999)}.jpeg')
                media.setType('photo')
                media.setMimetype('image/jpeg')

            mediaList.append(media)

        post.setMedia(mediaList)

        return post
    
    @staticmethod #! StreamCommentOutput required in SUPPORTED
    async def getComments(post: Post) -> AsyncGenerator[CommentConstructor, None]:
        #? limit handled by teleview lib, just yield ALL comments in post from newest to oldest

        if random.random() < 0.05: raise CommentNotFound()

        for _ in range(random.randint(20, 40)):
            comment = CommentConstructor(post)
            
            author = AuthorConstructor()
            author.setName(f'Name {random.randint(100,999)}')

            profilePicture = MediaConstructor()
            profilePicture.setUrl(f'https://example.com/account/{random.randint(1000, 9999)}/profile.jpeg')
            profilePicture.setType('photo')
            profilePicture.setMimetype('image/jpeg')

            author.setPicture(profilePicture)

            comment.setAuthor(author)

            if random.random() < 0.3:
                mediaInComment = MediaConstructor()
                mediaInComment.setUrl(f'https://example.com/assets/{random.randint(1000, 9999)}.jpeg')
                mediaInComment.setType('photo')
                mediaInComment.setMimetype('image/jpeg') 
                
                comment.setMedia([mediaInComment])


            comment.setText(f'Comment text {random.randint(100,999)}')
            comment.setDatetime(datetime.datetime.now())
            
            
            yield comment

    @staticmethod #! CommentOutput required in SUPPORTED
    async def getComment(post: Post, query: str | int) -> CommentConstructor:
        #? For example query: int (comment id)
        if type(query) != int: raise PostNotFound()

        if random.random() < 0.05: raise CommentNotFound()

        comment = CommentConstructor(post)
        
        author = AuthorConstructor()
        author.setName(f'Name {random.randint(100,999)}')

        profilePicture = MediaConstructor()
        profilePicture.setUrl(f'https://example.com/account/{random.randint(1000, 9999)}/profile.jpeg')
        profilePicture.setType('photo')
        profilePicture.setMimetype('image/jpeg')

        author.setPicture(profilePicture)

        comment.setAuthor(author)

        if random.random() < 0.3:
            mediaInComment = MediaConstructor()
            mediaInComment.setUrl(f'https://example.com/assets/{random.randint(1000, 9999)}.jpeg')
            mediaInComment.setType('photo')
            mediaInComment.setMimetype('image/jpeg') 
            
            comment.setMedia([mediaInComment])


        comment.setText(f'Comment text {random.randint(100,999)}')
        comment.setDatetime(datetime.datetime.now())
        
        
        return comment