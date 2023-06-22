import aiohttp, bs4
from . import runtime

from .models import *
from .__init__ import request_header


async def getChannel(url: str) -> Channel | None:
    """--- Асинхронная функция для получения инфомрации о канале ---

Принимает:
    * url: Ссылка или ЮЗ канала

Результат: 
    * Channel: при успешном получении информации о канале
    * None: если канала не существует или он приватный
"""
    name = url.replace('@','')
    if '/' in url: name = name.split('/')[3]

    async with aiohttp.ClientSession() as client:
        async with client.get(f'https://t.me/s/{name}', headers=request_header) as resp: bs = bs4.BeautifulSoup(await resp.text('utf-8'), 'html.parser')
    info = bs.find(class_='tgme_channel_info') # <div> с информацией о канале
    
    if not info: return None
    else: return runtime.BStoChannel(bs, name)

    


async def getPost(channel: Channel | str, id: int) -> Post | None:
    """--- Асинхронная функция для поиска поста в канале ---

Принимает:
    * channel: обьект Channel ИЛИ ссылка/ЮЗ канала
    * id: айди поста

Результат: 
    * Post: если пост найден
    * None: если пост НЕ найден
"""
    if type(channel) == str: channel = await getChannel(channel)
    if not channel: return None

    async with aiohttp.ClientSession() as client:
            async with client.get(f'https://t.me/{channel.url.split("/")[-1]}/{id}?embed=1', headers=request_header) as resp: bs = bs4.BeautifulSoup(await resp.text('utf-8'), 'html.parser')
    if bs.find(class_='tgme_widget_message_error'): return None
    else: return runtime.BStoPost(bs.find(class_='tgme_widget_message'), channel)


async def getComments(post: Post, limit: int = 10) -> list[Comment] | None:
    """--- Асинхронная функция для получения последних комментариев "под" постом ---

Принимает: 
    * post: обьект Post
    * limit: лимит по количеству постов. максимум 100

Результат: 
    * list[Comment]: если комментарии есть 
    * None: если их под постом нету

"""
    async with aiohttp.ClientSession() as client:
        async with client.get(f'{post.url}?embed=1&discussion=1&comments_limit={limit}', headers=request_header) as resp: bs = bs4.BeautifulSoup(await resp.text('utf-8'), 'html.parser')
    if bs.find(class_='tgme_widget_message_error') or bs.find(class_='tme_no_messages_found'): return None
    comments = []
    for msg in bs.findAll(class_='tgme_widget_message'): comments.append(runtime.BStoComments(msg, post))
    comments.reverse()
    return comments

async def getComment(post: Post, id: int) -> Comment | None:
    """--- Асинхронная функция для поиска комментария по ID ---

Принимает: 
    * post: обьект Post
    * id: ID поста

Результат: 
    * Comment: если комментарий найден 
    * None: если под постом нету комментариев или комментарий не найден

"""
    async with aiohttp.ClientSession() as client:
        async with client.get(f'{post.url}?comment={id}&embed=1', headers=request_header) as resp: bs = bs4.BeautifulSoup(await resp.text('utf-8'), 'html.parser')
    if bs.find(class_='tgme_widget_message_error') or bs.find(class_='tme_no_messages_found'): return None
    return runtime.BStoComment(bs.findAll(class_='tgme_widget_message')[0], post)




async def getAllPosts(channel: Channel) -> list[Post]:
    """ --- Асинхронная функция которая получает все посты в канале ---

ВНИМАНИЕ: ВЫПОЛНЕНИЕ МОЖЕТ ЗАНЯТЬ ДЛИТЕЛЬНОЕ ВРЕМЯ!
ВНИМАНИЕ: МОЖЕТ ПРЕОДОЛЕТЬ ЛИМИТ ПО ЗАПРОСАМ!

Принимает: 
    * channel: обьект Channel

Результат: 
    * list[Post]: список всех постов от старого к новому
    """
    posts = {}
    latest = await channel.getLatest()
    for p in latest: posts[p.id] = p
    print(list(posts.keys()))
    while True:
        pids = list(posts.keys())
        pids.sort()
        last_pid = pids[0]
        url = f'https://t.me/s/{channel.url.split("/")[-1]}/{last_pid}'
        async with aiohttp.ClientSession() as client:
            async with client.get(url, headers=request_header) as resp:  bs = bs4.BeautifulSoup(await resp.text('utf-8'), 'html.parser')
        loaded_posts = bs.findAll(class_='tgme_widget_message')
        for post in loaded_posts: 
            post_object = runtime.BStoPost(post, channel)
            posts[post_object.id] = post_object
        if 1 in posts.keys(): break
        
    pids = list(posts.keys())
    pids.sort()
    result = []
    for id in pids: result.append(posts[id])
    return result
            
        

