# *class*
```py
self.status = True # статус
self.url = <class 'str'> # ссылка на канал
self.name = <class 'str'> # название канала
self.description = <class 'str'> # описание канала
self.subscribers = <class 'int'> # кол-во подписчиков
self.picture = <class 'str'> # ссылка на аватарку канала
self.latests = <class 'list'> # последние 20 постов в канале
self.post(id) # функция для получения определенных постов
```
Если канала нет, то выдает 
```py
self.status = None
``` 
или 
```py
channel = pytgcf.get('123')
channel # -> None или False
```

# *class Post*
```py
self.text = <class 'str'>, # текст в этом посте, если текста нет, то возвращает None. 
self.id = <class 'int'>, # ID поста
self.url = <class 'str'>, # ссылка на пост
self.media = <class 'list'>, # список ссылок на прикрепленные фотографии. принимает None если фотографий нет
self.datetime = <class 'str'> # строка, в которой написана дата и время публикации. пользователь сам может конвертировать его в <class 'datetime.datetime'> при необходимости.
self.comments(limit=10) # функция для получения комментариев из поста
```

# *class Comment*
```py
self.id = <class 'int'> # айди комментария
self.reply = <class 'int'> # если этот комментарий написан в ответ на другой, то здесь будет id исходного комментария. иначе этого аргумента не существует
self.url = <class 'str'> # ссылка на комментарий
self.author.name = <class 'str'> # имя пользователя, написавший комментарий
self.author.username = <class 'str'> # username этого пользователя
self.author.photo = <class 'str'> # ссылка на фото профиля этого пользователя
self.text = <class 'str'> # текст комментария
self.datetime = <class 'str'> # дата отправки комментария, при необходимости пользователь сам может перевести его в <class 'datetime.datetime'>
```
