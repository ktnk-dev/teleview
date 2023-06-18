from . import runtime, corotune
class Media:
    def __init__(self, url, type) -> None:
        self.url = url
        self.type = type

    async def toDict(self) -> dict:
        return {
            'url': self.url,
            'type': self.type
        }


class Author: 
    def __init__(self, name, username, photo) -> None:
        self.name = name
        self.username = username
        self.photo = photo
    
    async def toDict(self) -> dict:
        return {
            'name': self.name,
            'username': self.username,
            'photo': self.photo
        }


class Comment:
    def __init__(self, post, id, text, reply, author, datetime) -> None:
        self.post = post
        self.id = id
        self.text = text
        self.reply = reply
        self.author = author
        self.datetime = datetime

    async def toDict(self) -> dict:
        return {
            'post': self.post.url,
            'id': self.id,
            'text': self.text,
            'reply': self.reply,
            'author': await self.author.toDict(),
            'datetime': self.datetime
        }



class Post:
    def __init__(self, channel, url, id, text, media, views, datetime, data) -> None:
        self.channel = channel
        self.url = url
        self.id = id
        self.text = text
        self.media = media
        self.views = int(views) 
        self.datetime = datetime
        self.__data = data
    
    async def getComments(self, limit = 10) -> list[Comment] | None:
        """--- Асинхронная функция для получения последних комментариев "под" постом ---

Принимает: 
    * limit: лимит по количеству постов. максимум 100

Результат: 
    * list[Comment]: если комментарии есть 
    * None: если их под постом нету

""" 
        return await corotune.getComments(self, limit)
    
    async def getComment(self, id) -> Comment | None:
        """--- Асинхронная функция для поиска комментария по ID ---

Принимает: 
    * id: ID поста

Результат: 
    * Comment: если комментарий найден 
    * None: если под постом нету комментариев или комментарий не найден

"""
        return await corotune.getComment(self, id)

    async def toDict(self) -> dict:        
        return {
            'channel': self.channel.url,
            'url': self.url,
            'id': self.id,
            'text': self.text,
            'media': [await media.toDict() for media in self.media],
            'views': self.views,
            'datetime': self.datetime
        }
    
        


class Channel:
    def __init__(self, url, name, description, subscribers, picture, data) -> None:
        self.url = url
        self.name = name
        self.description = description
        self.subscribers = int(subscribers)
        self.picture = picture
        self.__data = data
        self.__posts = {}

    async def getPost(self, id = int) -> Post | None:
        """--- Асинхронная функция для поиска поста в канале ---

Принимает:
    * id: айди поста

Результат: 
    * Post: если пост найден
    * None: если пост НЕ найден
        """
        return await corotune.getPost(self, id)
    
    async def getLatest(self) -> list[Post]:
        """ --- Получает 20 актуальных постов, возращая от актуального к старому ---

Ничего не принимает 

Результат: 
    * list[Post]: список постов от актуального к старому
    """
        return [runtime.BStoPost(post, self) for post in self.__data.findAll(class_='tgme_widget_message')] 
    

    async def getAllPosts(self) -> list[Post]:
        """ --- Асинхронная функция которая получает все посты в канале ---

ВНИМАНИЕ: ВЫПОЛНЕНИЕ МОЖЕТ ЗАНЯТЬ ДЛИТЕЛЬНОЕ ВРЕМЯ!
ВНИМАНИЕ: МОЖЕТ ПРЕОДОЛЕТЬ ЛИМИТ ПО ЗАПРОСАМ!

Ничего не принимает

Результат: 
    * list[Post]: список всех постов от старого к новому
    """
        if not self.__posts: self.__posts = await corotune.getAllPosts(self)
        return self.__posts




    async def toDict(self) -> dict:
        return {
            'url': self.url,
            'name': self.name,
            'description': self.description,
            'subscribers': self.subscribers,
            'picture': self.picture
        }