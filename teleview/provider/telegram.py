import bs4
import datetime
 
from typing import AsyncGenerator
from ..helper.supported import *
from ..models.constructor import *

from ..helper.provider import getHeaders
from ..helper.web import Request

#! Здесь бога нет
class Convert:
    @staticmethod
    def post(bs: bs4.BeautifulSoup):
        try: text = bs4.BeautifulSoup(str(bs.find(class_='tgme_widget_message_text')).replace('<br/>','\n'), 'html.parser').text # получаем текст сообщения, форматируя <br/> в \n
        except AttributeError: text = None   
        id = bs.get('data-post').split('/')[-1]

        try:
            views = bs.find(class_='tgme_widget_message_views').text
            if 'K' in views: views = int(float(views[:-1])*1000)
            elif 'M' in views: views = int(float(views[:-1])*1000*1000)
            else: views = int(views)
        except: views = 0
        
        media = []
        photos = bs.findAll(class_='tgme_widget_message_photo_wrap')
        videos = bs.findAll(class_='tgme_widget_message_video')

        if photos or videos:
            for photo in photos: media.append((photo.get('style').split("background-image:url('")[1].split("')")[0], 'image/jpeg'))
            for video in videos: media.append((video.get('src'), 'video/mp4'))

        roundvideo = bs.findAll(class_='tgme_widget_message_roundvideo')
        if roundvideo: media.append((roundvideo[0].get('src'), 'round_video/mp4'))
        voicemsg = bs.findAll(class_='tgme_widget_message_voice')
        if voicemsg: media.append((voicemsg[0].get('src'), 'voice/ogg'))

        try: datetime = bs.find(class_='datetime').get('datetime')
        except: datetime = bs.find(class_='time').get('datetime') 

        return int(id), text, media, views, datetime
    
    @staticmethod
    def comment(bs: bs4.BeautifulSoup):
        return int(bs.get('data-post-id')), bs4.BeautifulSoup(str(bs.find(class_='js-message_text')).replace('<br/>','\n'), 'html.parser').text, bs.find(class_='tgme_widget_message_date').find('time').get('datetime')

    @staticmethod
    def author(bs: bs4.BeautifulSoup):
        try: author_photo = bs.find(class_='tgme_widget_message_user_photo').find('a').find('i').find('img').get('src')
        except: author_photo = False
        return bs.find(class_='tgme_widget_message_author_name').text, author_photo


class Provider:
    REQUIRED_TELEVIEW_VERSION: float = 2.0
    VERSION: float = 1.0

    SUPPORTED: tuple = (
        #! StreamChannelOutput, #! Not supported 
        StreamPostOutput, 
        StreamCommentOutput, 
        PostOutput, 
        CommentOutput
    )

    @staticmethod 
    async def getChannel(query: str | int) -> ChannelConstructor:
        if type(query) != str: raise ChannelNotFound()

        # возможность кушать ссылки
        query = query.replace('@','')
        if '/' in query: query = query.split('/')[3]

        request = Request(f'https://t.me/s/{query}', getHeaders())
        await request.load()
        info = request.toBS().find(class_='tgme_channel_info')
        if not info: raise ChannelNotFound()

        channel = ChannelConstructor()

        channel.setUrl(f'https://t.me/{query}')
        channel.setName(info.find(class_='tgme_channel_info_header_title').text)

        # описание
        try: channel.setDescription(info.find(class_='tgme_channel_info_description').text)
        except: ...
            
        subs_str = info.find(class_='tgme_channel_info_counter').find(class_='counter_value').text # получение кол-ва подписчиков / исправление бага с некоректным подсчетом количества подписчиков
        if 'K' in subs_str: subscribers = float(subs_str[:-1])*1000 # конвертация из str в int 
        elif 'M' in subs_str: subscribers = float(subs_str[:-1])*1000*1000
        else: subscribers = int(subs_str)
        channel.setSubscribers(int(subscribers))

        try: 
            pictureUrl = info.find(class_='tgme_page_photo_image').find('img').get('src') # фото канала
            picture = MediaConstructor()
            picture.setUrl(pictureUrl)
            picture.setType('photo')
            picture.setMimetype('image/jpeg')
            channel.setPicture(picture)
        except: ...

        channel.setIternal({
            'id': query,
            'bs': request.toBS()
        })

        return channel

    @staticmethod
    async def getPosts(channel: Channel) -> AsyncGenerator[PostConstructor, None]:
        bsLatest: bs4.BeautifulSoup = channel._iternal['bs']
        lastId = 0
        bsList = bsLatest.findAll(class_='tgme_widget_message')
        bsList.reverse()
        for postBS in bsList:
            id, text, mediaList, views, date = Convert.post(postBS)
            lastId = id
            post = PostConstructor(channel)

            post.setUrl(f'{channel.url}/{id}')
            post.setText(text)
            post.setViews(views)

            mediaConstr = []
            for mediaInfo in mediaList:
                media = MediaConstructor()
                media.setUrl(mediaInfo[0])
                match (mediaInfo[1].split('/')[0]):
                    case 'image':
                        media.setType('photo')
                        media.setMimetype('image/jpeg')

                    case 'video':
                        media.setType('video')
                        media.setMimetype('video/mp4')

                    case 'round_video':
                        media.setType('round_video')
                        media.setMimetype('video/mp4')

                    case 'voice':
                        media.setType('voice_message')
                        media.setMimetype('audio/ogg')
                
                mediaConstr.append(media)

            post.setMedia(mediaConstr)

            post.setDatetime(datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z'))


            post.setIternal({
                'id': id,
                'bs': postBS
            })

            yield post
        
        while lastId > 1:
            requset = Request(f'https://t.me/s/{channel._iternal["id"]}/{lastId}')
            await requset.load()
            bs = requset.toBS()
            bsList = bs.findAll(class_='tgme_widget_message')
            bsList.reverse()
            for postBS in bsList:
                id, text, mediaList, views, date = Convert.post(postBS)
                if id >= lastId: continue
                lastId = id
                post = PostConstructor(channel)

                post.setUrl(f'{channel.url}/{id}')
                post.setText(text)
                post.setViews(views)

                mediaConstr = []
                for mediaInfo in mediaList:
                    media = MediaConstructor()
                    media.setUrl(mediaInfo[0])
                    match (mediaInfo[1].split('/')[0]):
                        case 'image':
                            media.setType('photo')
                            media.setMimetype('image/jpeg')

                        case 'video':
                            media.setType('video')
                            media.setMimetype('video/mp4')

                        case 'round_video':
                            media.setType('round_video')
                            media.setMimetype('video/mp4')

                        case 'voice':
                            media.setType('voice_message')
                            media.setMimetype('audio/ogg')
                    
                    mediaConstr.append(media)

                post.setMedia(mediaConstr)

                post.setDatetime(datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z'))


                post.setIternal({
                    'id': id,
                    'bs': postBS
                })

                yield post

    @staticmethod 
    async def getPost(channel: Channel, query: str | int) -> PostConstructor:
        if type(query) != int: raise PostNotFound()
        request = Request(f'{channel.url}/{query}?embed=1', getHeaders())
        await request.load()
        if request.toBS().find(class_='tgme_widget_message_error'): raise PostNotFound()
        id, text, mediaList, views, date = Convert.post(request.toBS().find(class_='tgme_widget_message'))
        post = PostConstructor(channel)


        post.setUrl(f'{channel.url}/{id}')
        post.setText(text)
        post.setViews(views)

        mediaConstr = []
        for mediaInfo in mediaList:
            media = MediaConstructor()
            media.setUrl(mediaInfo[0])
            match (mediaInfo[1].split('/')[0]):
                case 'image':
                    media.setType('photo')
                    media.setMimetype('image/jpeg')

                case 'video':
                    media.setType('video')
                    media.setMimetype('video/mp4')

                case 'round_video':
                    media.setType('round_video')
                    media.setMimetype('video/mp4')

                case 'voice':
                    media.setType('voice_message')
                    media.setMimetype('audio/ogg')
            
            mediaConstr.append(media)

        post.setMedia(mediaConstr)

        post.setDatetime(datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z'))
        # %Y-%m-%dT%H:%M:%S%z
        # 2024-07-26T18:18:13+00:00 


        post.setIternal({
            'id': id,
            'bs': request.toBS()
        })

        return post

    @staticmethod
    async def getComments(post: Post) -> AsyncGenerator[CommentConstructor, None]:
        request = Request(f'{post.url}?embed=1&discussion=1&comments_limit=100', getHeaders())
        await request.load()
        bs = request.toBS()


        if bs.find(class_='tgme_widget_message_error') or bs.find(class_='tme_no_messages_found'):
            raise CommentNotFound()
        
        bsList = bs.findAll(class_='tgme_widget_message')
        bsList.reverse()

        for bs in bsList:
            id, text, date = Convert.comment(bs)
            comment = CommentConstructor(post)

            author = AuthorConstructor()
            name, pictureUrl = Convert.author(bs)
            author.setName(name)
            if pictureUrl:
                picture = MediaConstructor()
                picture.setUrl(pictureUrl)
                picture.setType('photo')
                picture.setMimetype('image/jpeg')
            
            comment.setAuthor(author)
            
            comment.setText(text)
            comment.setDatetime(datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z'))
            comment.setIternal({'id': int(id)})

            yield comment
        


    @staticmethod
    async def getComment(post: Post, query: str | int) -> CommentConstructor:
        if type(query) != int: raise CommentNotFound()

        request = Request(f'{post.url}?comment={query}&embed=1', getHeaders())
        await request.load()
        bs = request.toBS()


        if bs.find(class_='tgme_widget_message_error') or bs.find(class_='tme_no_messages_found'): 
            raise CommentNotFound()
        
        bs = bs.findAll(class_='tgme_widget_message')[0]
        
        id, text, date = Convert.comment(bs)
        comment = CommentConstructor(post)

        author = AuthorConstructor()
        name, pictureUrl = Convert.author(bs)
        author.setName(name)
        if pictureUrl:
            picture = MediaConstructor()
            picture.setUrl(pictureUrl)
            picture.setType('photo')
            picture.setMimetype('image/jpeg')
        
        comment.setAuthor(author)

        comment.setText(text)
        comment.setDatetime(datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z'))
        comment.setIternal({'id': int(id)})

        return comment
