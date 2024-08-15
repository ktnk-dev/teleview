# Exceptions
from ..exceptions import *

# Types
from datetime import datetime as Datetime
from ..models.default import Channel, Post, Comment, Media, Author

class MediaConstructor:
    """Media Constructor object

All data must be specified

- type: str = this is name of media content (for example: voice_message, etc...)
    """
        
    def __init__(self) -> None:
        self.url = False
        self.type = False
        self.mimetype = False

    def setUrl(self, url: str) -> None:
        self.url = url

    def setType(self, type: str) -> None:
        self.type = type

    def setMimetype(self, mimetype: str) -> None:
        self.mimetype = mimetype
    
    def build(self) -> Media:
        if (self.url, self.type, self.mimetype).count(False): 
            print(f'''
[teleview] Failed to build Media from constructor
MediaConstructor(
    {self.url=}
    {self.type=}
    {self.mimetype=}
''')     
            raise IncorrectConstructor()
        
        return Media(self)


class ChannelConstructor:
    """Channel Constructor object

Must be sepcified to not raise an error
- url
- name
- subscribers

Anything else can be not-specified, it will False by default\n
You can also specify any other information using setIternal(dict_of_data)\n
For example to set channelID or any other important to parse information
    
    """
    def __init__(self) -> None:
        self.url = False
        self.name = False
        self.picture = False
        self.description = False
        self.subscribers = False

        self.iternal = {}

    def setUrl(self, url: str) -> None:
        self.url = url

    def setName(self, name: str) -> None:
        self.name = name

    def setPicture(self, picture: MediaConstructor) -> None:
        self.picture = picture

    def setDescription(self, description: str) -> None:
        self.description = description

    def setSubscribers(self, subscribers: int) -> None:
        self.subscribers = subscribers

    def setIternal(self, iternalInfo: dict) -> None:
        self.iternal = iternalInfo

    def build(self) -> Channel:
        if not self.url or not self.name or type(self.subscribers) != int: 
            print(f'''
[teleview] Failed to build Channel from constructor
ChannelConstructor(
    {self.url=}
    {self.name=}
    {self.picture=}
    {self.description=}
    {self.subscribers=}
    {self.iternal=}
)                  
''')
            raise IncorrectConstructor()
        
        return Channel(self)

class PostConstructor:
    """Post Constructor object

Must be sepcified to not raise an error
- url
- datetime

Anything else can be not-specified, it will False (views = 0, media = []) by default\n
You can also specify any other information using setIternal(dict_of_data)\n
For example to set postID or any other important to parse information
    
    """
    def __init__(self, channel: Channel) -> None:
        self.channel = channel

        self.url = False
        self.text = False
        self.views = 0
        self.media = []
        self.datetime = False

        self.iternal = {}

    def setUrl(self, url: str) -> None:
        self.url = url

    def setText(self, text: str) -> None:
        self.text = text

    def setViews(self, views: int) -> None:
        self.views = views

    def setMedia(self, media: list[MediaConstructor]) -> None:
        self.media = media

    def setDatetime(self, datetime: Datetime) -> None:
        self.datetime = datetime

    def setIternal(self, iternalInfo: dict) -> None:
        self.iternal = iternalInfo

    def build(self) -> Post:
        if not self.url or not self.datetime: 
            print(f'''
[teleview] Failed to build Post from constructor
PostConstructor(
    {self.channel=}
    {self.url=}
    {self.text=}
    {self.views=}
    {self.media=}
    {self.datetime=}
    {self.iternal=}
)                  
''')
            raise IncorrectConstructor()
        
        return Post(self)
    

class AuthorConstructor:
    """Media Constructor object

Must be sepcified to not raise an error
- name

    """
        
    def __init__(self) -> None:
        self.name = False
        self.picture = False

    def setName(self, name: str) -> None:
        self.name = name

    def setPicture(self, picture: MediaConstructor) -> None:
        self.picture = picture
    
    def build(self) -> Author:
        if self.name == False: 
            print(f'''
[teleview] Failed to build Author from constructor
AuthorConstructor(
    {self.name=}
    {self.picture=}
)
''')     
            raise IncorrectConstructor()
        
        return Author(self)

class CommentConstructor:
    """Comment Constructor object

Must be sepcified to not raise an error
- author
- datetime

Anything else can be not-specified, it will False (media = []) by default\n
You can also specify any other information using setIternal(dict_of_data)\n
For example to set commentID or any other important to parse information
    
    """
    def __init__(self, post: Post) -> None:
        self.post = post

        self.text = False
        self.media = []
        self.author = False
        self.datetime = False

        self.iternal = {}



    def setText(self, text: str) -> None:
        self.text = text

    def setAuthor(self, author: AuthorConstructor) -> None:
        self.author = author

    def setMedia(self, media: list[MediaConstructor]) -> None:
        self.media = media

    def setDatetime(self, datetime: Datetime) -> None:
        self.datetime = datetime

    def setIternal(self, iternalInfo: dict) -> None:
        self.iternal = iternalInfo

    def build(self) -> Comment:
        if not self.author or not self.datetime: 
            print(f'''
[teleview] Failed to build Post from constructor
CommentConstructor(
    {self.post=}
    {self.text=}
    {self.author=}
    {self.media=}
    {self.datetime=}
    {self.iternal=}
)                  
''')
            raise IncorrectConstructor()
        
        return Comment(self)