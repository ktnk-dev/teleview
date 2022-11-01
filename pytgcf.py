import bs4, requests
def get(name, id=0):
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
        
        photos = post.findAll(class_='tgme_widget_message_photo_wrap')  # пробуем получить фотки
        if photos:                                                      # -> если они есть, то добовляем каждую фотку в список.
            result['photos'] = []
            for photo in photos:                                        # -> получаем ссылку из background-image в style свойстве <div> элементов картинки 
                result['photos'].append(photo.get('style').split("background-image:url('")[1].split("')")[0])   
        
        return result 

    if id > 0: # если юзер выдал определенный айди поста [1..x]
        url = f'https://t.me/{name}/{id}?embed=1'   # используется прямая ссылка на embed версию поста. она грузится быстро очень, нежели искать по всему каналу.
        web = requests.get(url, headers={"User-Agent":"1"}) # реквест
        bs = bs4.BeautifulSoup(web.text, "lxml") # переделка в bs4
        post = bs.find(class_='tgme_widget_message') # поиск <div> элемента поста
        posts = [postdata(post, name=name)]
        if posts == []: return {'status':None, 'text':'Channel not found'}

        # возвращается информация об одном посте
        data = { 'status':posts[0]['status'] }
        if not data['status']: data['text'] = data['posts'][0]['text']
        else: 
            data['name'] = posts[0]['name']
            data['posts'] = posts

        return data

    elif id > -21:   # если юзер хочет получить последние 20 сообщений (id:0) или одно из последних id:[-1..-20]
        url = f'https://t.me/s/{name}'  # ссылка на веб-версию тг с этим каналом
        web = requests.get(url, headers={"User-Agent":"1"}) # реквест
        bs = bs4.BeautifulSoup(web.text, "lxml") # переделка в bs4
        posts = bs.findAll(class_='tgme_widget_message') # поиск всех последних (20) постов в канале 
        results = [] # создание массива
        for post in posts: results.append(postdata(post, False)) # заполнение массива
        if results == []: return {'status':None, 'text':'Channel not found'}
        if id == 0: return {
            'name': results[0]['name'],
            'status': True,
            'posts': results
        }  # сравниваем айди, если 0 значит юзер хочет все последние посты, возвращаем results как есть
        elif -21 < id < 0: return {
            'name': results[0]['name'],
            'status': True,
            'posts': [results[id]]
        } # -> здесь айди <0, то есть юзер хочет определенный пост с конца. возвращаем элемент из results
    else: 
        return {
            'status': None,
            'text': 'id allowed only [-20..-1] and [0..x]'
        }





        
