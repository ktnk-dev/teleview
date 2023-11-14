from .models import *
import bs4, aiohttp

def BStoChannel(bs, name) -> Channel:
    info = bs.find(class_='tgme_channel_info')
    try: description = info.find(class_='tgme_channel_info_description').text # описание 
    except: description = None 
        
    subs_str = info.find(class_='tgme_channel_info_counter').find(class_='counter_value').text # получение кол-ва подписчиков / исправление бага с некоректным подсчетом количества подписчиков
    if 'K' in subs_str: subscribers = float(subs_str[:-1])*1000//1 # конвертация из str в int 
    elif 'M' in subs_str: subscribers = float(subs_str[:-1])*1000*1000//1
    else: subscribers = int(subs_str)

    try: picture = info.find(class_='tgme_page_photo_image').find('img').get('src') # фото канала
    except: picture = None
    
    return Channel(f'https://t.me/{name}', info.find(class_='tgme_channel_info_header_title').text, description, subscribers, picture, bs)


def BStoPost(bs, channel) -> Post:
    try: text = bs4.BeautifulSoup(str(bs.find(class_='tgme_widget_message_text')).replace('<br/>','\n'), 'html.parser').text # получаем текст сообщения, форматируя <br/> в \n
    except AttributeError: text = None   
    id = bs.get('data-post').split('/')[-1]
    try:
        views = bs.find(class_='tgme_widget_message_views').text
        if 'K' in views: views = float(views[:-1])*1000//1
        elif 'M' in views: views = float(views[:-1])*1000*1000//1
        else: views = int(views)
    except: views = 0
    
    media = []
    photos = bs.findAll(class_='tgme_widget_message_photo_wrap')
    videos = bs.findAll(class_='tgme_widget_message_video')
    if photos or videos:
        for photo in photos: media.append(Media(photo.get('style').split("background-image:url('")[1].split("')")[0], 'photo/jpg'))
        for video in videos: media.append(Media(video.get('src'), 'video/mp4'))
    roundvideo = bs.findAll(class_='tgme_widget_message_roundvideo')
    if roundvideo: media.append(Media(roundvideo[0].get('src'), 'round_video/mp4'))
    voicemsg = bs.findAll(class_='tgme_widget_message_voice')
    if voicemsg: media.append(Media(voicemsg[0].get('src'), 'voice/ogg'))

    try: datetime = bs.find(class_='datetime').get('datetime')
    except: datetime = bs.find(class_='time').get('datetime') 

    return Post(channel, f'{channel.url}/{id}', int(id), text, media, views, datetime, bs)


def BStoComments(msg, post) -> list[Comment]: 
    try: reply = int(msg.find(class_='tgme_widget_message_reply').get('data-reply-to'))   
    except: reply = None

    return Comment(post, int(msg.get('data-post-id')), bs4.BeautifulSoup(str(msg.find(class_='js-message_text')).replace('<br/>','\n'), 'html.parser').text, reply, BStoAuthor(msg), msg.find(class_='tgme_widget_message_date').find('time').get('datetime'))


def BStoComment(msg, post) -> Comment: 
    try: reply = int(msg.find(class_='tgme_widget_message_reply').get('href').split('/')[-1])   
    except: reply = None

    return Comment(post, int(msg.get('data-post-id')), bs4.BeautifulSoup(str(msg.find(class_='js-message_text')).replace('<br/>','\n'), 'html.parser').text, reply, BStoAuthor(msg), msg.find(class_='tgme_widget_message_date').find('time').get('datetime'))

def BStoAuthor(msg) -> Author:
    try: author_username = msg.find(class_='tgme_widget_message_user').find('a').get('href').split('/')[-1]
    except: author_username = None
    try: author_photo = msg.find(class_='tgme_widget_message_user_photo').find('a').find('i').find('img').get('src')
    except: author_photo = None
    return Author(msg.find(class_='tgme_widget_message_author_name').text, author_username, author_photo)


