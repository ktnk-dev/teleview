import bs4, requests
version = 0.2
source = 'https://github.com/ktnk-dev/py-tg-channel-fetcher'

class get():
    def __init__(self, name):
        url = f'https://t.me/s/{name}'  # ссылка на веб-версию тг с этим каналом
        web = requests.get(url, headers={"User-Agent":"1"}) # реквест
        bs = bs4.BeautifulSoup(web.text, "lxml") # переделка в bs4
        info = bs.find(class_='tgme_channel_info') # <div> с информацией о канале
        if not info: # если канала нет, то возвращается ошибка
            self.status = None 
            self.text = 'Channel not found'
            return
        else: self.status = True 
        self.channel_short = name 
        self.url = 'https://t.me/'+name
        self.name = info.find(class_='tgme_channel_info_header_title').text # название
        self.description = info.find(class_='tgme_channel_info_description').text # описание 
        subs_str = info.find(class_='tgme_channel_info_counter').find(class_='counter_value').text.replace('.','') # получение кол-ва подписчиков
        if 'K' in subs_str: self.subscribers = int(float(subs_str[:-1])*1000) # конвертация в int 
        elif 'M' in subs_str: self.subscribers = int(float(subs_str[:-1])*1000*1000)
        else: self.subscribers = int(subs_str)
        self.picture = info.find(class_='tgme_page_photo_image').find('img').get('src') # фото канала
        self.latests = [self.posts(bs=post) for post in bs.findAll(class_='tgme_widget_message')] # получение последних 20 постов (не ну а че, реквест уже сделан)

    def posts(self, id=0, bs=None):
        name = self.channel_short   
        def postdata(post, single = True, name = None):  # функция, для получения информации из <div> обьекта, в котором хранится пост
            result = {}
            try: result['name'] = post.find(class_='tgme_widget_message_owner_name').text  # пробуем получить название канала
            except: return {'status':None,'text':'Post not found',}                # -> если не вышло, значит поста вообще нет, возвращаем ошибку
            
            result['status'] = True  # раз мы успешно получили название, то ставим статус Тру, означающий, что ошибки нет
            
            if single: result['url'] = post.find(class_='tgme_widget_message_link').text  # получаем сссылку на пост (если single пост)
            else: result['url'] = 'https://t.me/'+post.get('data-post')                   # -> если не single
            
            result['id'] = int(result['url'].split('/')[-1])  # записываем айди
            
            try: result['text'] = bs4.BeautifulSoup(str(post.find(class_='tgme_widget_message_text')).replace('<br/>','\n'), 'html.parser').text # получаем текст сообщения, форматируя <br/> в \n
            except AttributeError:  result['text'] = None                                                                                        # -> если ловим ошибку значит текста нет
            
            if single: result['datetime'] = post.find(class_='datetime').get('datetime')  # получаем время (для single)
            else: result['datetime'] = post.find(class_='time').get('datetime')           # -> (не для одиночных постов)
            
            views = post.find(class_='tgme_widget_message_views').text            # получение кол-ва просмотров
            if 'K' in views: result['views'] = int(float(views[:-1])*1000)        # конвертация в int 
            elif 'M' in views: result['views'] = int(float(views[:-1])*1000*1000)
            else: result['views'] = int(views)
            
            photos = post.findAll(class_='tgme_widget_message_photo_wrap')  # пробуем получить фотки
            if photos:                                                      # -> если они есть, то добовляем каждую фотку в список.
                result['photos'] = []
                for photo in photos:                                        # -> получаем ссылку из background-image в style свойстве <div> элементов картинки 
                    result['photos'].append(photo.get('style').split("background-image:url('")[1].split("')")[0])   
            return result 
        if bs: return postdata(bs, False) # загрузка из готового bs4 обьекта, сгенерированный при первом вызове класса
        elif id > 0: # если юзер выдал определенный айди поста [1..x]
            url = f'https://t.me/{name}/{id}?embed=1'   # используется прямая ссылка на embed версию поста. она грузится быстро очень, нежели искать по всему каналу.
            web = requests.get(url, headers={"User-Agent":"1"}) # реквест
            bs = bs4.BeautifulSoup(web.text, "lxml") # переделка в bs4
            post = bs.find(class_='tgme_widget_message') # поиск <div> элемента поста
            posts = [postdata(post, name=name)]
            if posts == []: return {'status':None, 'text':'Channel not found'}

            # возвращается информация об одном посте
            if not posts[0]['status']: 
                data = {}
                data['status'] = None
                data['text'] = posts[0]['text']
                return data
            else: return posts  

        elif id > -21:   # если юзер хочет получить последние 20 сообщений (id:0) или одно из последних id:[-1..-20]
            if id == 0: return {
                'status': True,
                'posts': self.latests
            }  # сравниваем айди, если 0 значит юзер хочет все последние посты, возвращаем latest как есть
            elif -21 < id < 0: return {
                'status': True,
                'posts': [self.latests[id]]
            } # -> здесь айди < 0, то есть юзер хочет определенный пост с конца. возвращаем элемент из latest
        else: 
            return {
                'status': None,
                'text': 'id allowed only [-20..-1] and [0..x]'
            }





        
