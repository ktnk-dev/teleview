import bs4, requests
version = 0.6
source = 'https://github.com/ktnk-dev/py-tg-channel-fetcher'

class get():
    def __init__(self, name):
        url = f'https://t.me/s/{name}'  # ссылка на веб-версию тг с этим каналом
        web = requests.get(url, headers={"User-Agent":"1"}) # реквест
        bs = bs4.BeautifulSoup(web.text, "lxml") # переделка в bs4
        info = bs.find(class_='tgme_channel_info') # <div> с информацией о канале
        if not info: 
            self.status = None # если канала нет, то возвращается None
            return
        self.status = True
        self.channel_short = name 
        self.url = 'https://t.me/'+name
        self.name = info.find(class_='tgme_channel_info_header_title').text # название
        try: self.description = info.find(class_='tgme_channel_info_description').text # описание 
        except: self.description = None
        subs_str = info.find(class_='tgme_channel_info_counter').find(class_='counter_value').text.replace('.','') # получение кол-ва подписчиков
        if 'K' in subs_str: self.subscribers = int(float(subs_str[:-1])*1000) # конвертация в int 
        elif 'M' in subs_str: self.subscribers = int(float(subs_str[:-1])*1000*1000)
        else: self.subscribers = int(subs_str)
        try: self.picture = info.find(class_='tgme_page_photo_image').find('img').get('src') # фото канала
        except: self.picture = None
        self.latests = [self.post(0,bs=post) for post in bs.findAll(class_='tgme_widget_message')] # получение последних 20 постов (не ну а че, реквест уже сделан)
    
    def __bool__(self): return False if self.status == None else True
    def __call__(self): return None if self.status == None else True
     
    def chunk(self, id=0, full=False):
        id = id if id != 0 else self.latests[0].id 
        url = f'https://t.me/s/{self.channel_short}/{id}'  # ссылка на веб-версию тг с этим каналом
        web = requests.get(url, headers={"User-Agent":"1"}) # реквест
        bs = bs4.BeautifulSoup(web.text, "lxml") # переделка в bs4
        fulldata = [self.post(0,bs=post) for post in bs.findAll(class_='tgme_widget_message')]
        loaded_posts = [latest.id for latest in self.latests]
        data = [post for post in fulldata if post.id not in loaded_posts and post.id != id]
        self.latests = data + self.latests if id == self.latests[0].id and not full else ...
        

        return data if not full else fulldata
    
    def post(self, id, bs=None):
        if not self.status: return None
        name = self.channel_short  
        class Post():
            def __init__(self, post, single = True, channel_short = ''):
                self.channel_short = channel_short                
                
                if single: self.url = 'https://'+post.find(class_='tgme_widget_message_link').text  # получаем сссылку на пост (если single пост)
                else: self.url = 'https://t.me/'+post.get('data-post')                   # -> если не single
                
                self.id = int(self.url.split('/')[-1])  # записываем айди
                
                try: self.text = bs4.BeautifulSoup(str(post.find(class_='tgme_widget_message_text')).replace('<br/>','\n'), 'html.parser').text # получаем текст сообщения, форматируя <br/> в \n
                except AttributeError: self.text = None                                                                                        # -> если ловим ошибку значит текста нет
                
                if single: self.datetime = post.find(class_='datetime').get('datetime')  # получаем время (для single)
                else: self.datetime = post.find(class_='time').get('datetime')           # -> (не для одиночных постов)
                
                try:
                    views = post.find(class_='tgme_widget_message_views').text            # получение кол-ва просмотров
                    if 'K' in views: self.views = int(float(views[:-1])*1000)        # конвертация в int 
                    elif 'M' in views: self.views = int(float(views[:-1])*1000*1000)
                    else: self.views = int(views)
                except: self.views = 0 # если еще нет просмотров
                
                photos = post.findAll(class_='tgme_widget_message_photo_wrap')  # пробуем получить фотки
                if photos:                                                      # -> если они есть, то добовляем каждую фотку в список
                    self.media = []
                    for photo in photos:                                        # -> получаем ссылку из background-image в style свойстве <div> элементов картинки 
                        self.media.append(photo.get('style').split("background-image:url('")[1].split("')")[0])   
                else: self.media = None
                urlprev = post.findAll(class_='link_preview_image')
                if urlprev and not photos: self.media = [urlprev[0].get('style').split("background-image:url('")[1].split("')")[0]]
                    
                    
  
            def comments(self,id=None,limit=10): 
                name = self.channel_short
                ids = self.id
                url = f'https://t.me/{name}/{ids}?embed=1&discussion=1&comments_limit={limit}' if not id else f'https://t.me/{name}/{ids}?comment={id}&embed=1'# используется прямая ссылка на embed версию "дискуссии" или определенного сообщения
                web = requests.get(url, headers={"User-Agent":"1"}) # реквест
                bs = bs4.BeautifulSoup(web.text, "lxml") # переделка в bs4
                if id and bs.find(class_='tgme_widget_message_error') or bs.find(class_='tme_no_messages_found'): return None # если айди такого поста нет то вернет None
                comments = bs.findAll(class_='tgme_widget_message') # поиск <div> элементов комментария
                if comments:
                    result = []
                    class Comment():    
                        def __init__(self,msg, single=None):
                            self.id = int(msg.get('data-post-id')) # получаем айди поста, чтобы записать его как ключ в result (result[id])
                            class CommentAuthor():   # класс, чтобы просто создать атрибут user и в него пихнуть присущие ему данные
                                def __init__(self,msg):
                                    try:self.username = msg.find(class_='tgme_widget_message_user').find('a').get('href').split('/')[-1] # находим ссылку на аккаунт и достаем от туда username
                                    except: self.username = None                                                                         # -> если у юзера нету username, то пишем None
                                    self.name = msg.find(class_='tgme_widget_message_author_name').text # достаем имя пользователя
                                    try:self.photo = msg.find(class_='tgme_widget_message_user_photo').find('a').find('i').find('img').get('src') # достаем ссылку на картинку
                                    except: self.photo = None                                                                                     # -> если картинки нет, то пишем None
                            self.author = CommentAuthor(msg)   

                            try:  # если сообщение является ответом на другое, то пишем айди исходного сообщения сюда. пригодится для result[reply] который вернет готовый исходный пост
                                if single: self.reply = int(msg.find(class_='tgme_widget_message_reply').get('href').split('/')[-1])
                                else: self.reply = int(msg.find(class_='tgme_widget_message_reply').get('data-reply-to'))   
                            except:...

                            self.text = bs4.BeautifulSoup(str(msg.find(class_='js-message_text')).replace('<br/>','\n'), 'html.parser').text    # записываем текст, красиво заменяя все <br> на \n

                            self.url = msg.find(class_='tgme_widget_message_date').get('href') # странный способ получить ссылку на сообщение, зато рабочий

                            self.datetime = msg.find(class_='tgme_widget_message_date').find('time').get('datetime')    # дата и время отправки сообщения
                    
                    for comment in comments: result.append(Comment(comment, id))
                    if len(result) == 1: 
                        if id: return result[0]
                    return result 
                else: return None   # если коментов вообще нет

                
        if bs: return Post(bs, False, name) # загрузка из готового bs4 обьекта, сгенерированный при первом вызове класса
        elif id > 0: # если юзер выдал определенный айди поста [1..x]
            url = f'https://t.me/{name}/{id}?embed=1'   # используется прямая ссылка на embed версию поста. она грузится быстро очень, нежели искать по всему каналу
            web = requests.get(url, headers={"User-Agent":"1"}) # реквест
            bs = bs4.BeautifulSoup(web.text, "lxml") # переделка в bs4
            post = bs.find(class_='tgme_widget_message') # поиск <div> элемента поста
            try: 
                post.find(class_='tgme_widget_message_owner_name').text  # пробуем получить название канала
                return Post(post, channel_short=name)
            except: return None               # -> если не вышло, значит поста вообще нет, возвращаем None
            
        elif 0 > id: return self.latests[id]  # если юзер хочет получить одно из последних id:[-1..-20]; возвращаем элемент из latest[id]
        else: return None
