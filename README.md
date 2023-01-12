# О проекте 
- Python скрипт для получения информации о публичном телеграм канале и получения постов в этом канале. 
- [Документация Rest API](./WEB.md) 
- Зависимости: `requests`, `bs4`, `lxml`
- Версия: `release`/`1.0` (final release)
- Тесты: `15` из `15` успешно

# Какую информацию получает скрипт с канала
- `pytgcf.get(channel_short_name)` → [*class*](./REF.md#class) <br>
Выдает класс с информацией о посте (для удобства в дальнейшем будет использоваться как `channel`)

<hr></hr>

- `channel.post(id)` → [*class Post*](./REF.md#class-post) <br>
P.S: В `channel.latests` уже находится 20 актуальных постов <br>
*Если будет произведена попытка поиска несуществуюшего поста - функция вернет None*

- `channel.chunk()` → *list*  (состоящий из [*class Post*](./REF.md#class-post)) <br>
Данная функция вернет еще 10(на деле может быть меньше, учитывайте это) актуальных постов, а так же сама добавит их в `channel.latests` в верной последовательности
<hr></hr>

- `Post.comments(id)` → [*class Comment*](./REF.md#class-comment)
- `Post.comments(limit=10)` → *list* (состоящий из [*class Comment*](./REF.md#class-comment)) <br>
*Если будет произведена попытка поиска несуществуюшего комментария - функция вернет None*

# Как этим пользоваться 
- Получение информации о канале
```py
import pytgcf
channel = pytgcf.get('durov')

channel.name # -> Durov's Channel
channel.description # -> Thoughts from the Product Manager / CEO / Founder of Telegram.
```

- Так же мы можем получить определенный пост, используя функцию `self.post(id)` где первым аргументом вводим айди поста
```py
import pytgcf
channel = pytgcf.get('durov')

post = channel.post(200) # будет получен пост под id 200
post.text # текст с поздравлением с хелоуином
post.views # количество просмотров 
```

- Или получить один из последних постов на канале, для этого нужно вписать отрицательное число в параметр id (от -1 до -бесконечности)
```py
import pytgcf
channel = pytgcf.get('durov')

channel.post(-1) # будет получен самый актуальный (последний) пост канала
# эквивалент: channel.latests[-1]

channel.post(-2) # будет получен предпоследний пост с канала
# эквивалент: channel.latests[-2]
```
- Загрузить больше актуальных постов
```py
import pytgcf
channel = pytgcf.get('durov')
len(channel.latests) # 20

channel.chunk()
len(channel.latests) # 30 (в остальных каналах может добавить меньше постов)

channel.chunk()
len(channel.latests) # 40

firstposts = channel.chunk(1) # функции можно дать айди поста(если он есть), возле которого будет загрузка всех постов. при таком использовании они не добавятся в channel.latests
```

- Просмотр комментариев на пост
```py
import pytgcf
channel = pytgcf.get('contest') # возьмем в качестве примера канал @contest
post = channel.post(198) # получаем пост под айди 198

comments = post.comments(limit=5) # мы получаем 5 последних комментариев (список!)
comment = comments[-1] # это самый актуальный комментарий в посте
comment.author.name # -> имя автора комментария
comment.text        # -> текст комментария 

comment = post.comments(id=141108) # мы получаем определенный пост (не список!)
comment.author.name # -> Deleted Account 
comment.text        # -> Im Rassia......

durov = pytgcf.get('durov').post(37)
durov.comments() # -> None ; так как в канале дурова отключены комментарии. Так же будет, если еще никто не написал комментариев 
```

# TODO
- ~Аватарка канала~ (готово v0.2)
- ~Количество подписчиков~ (готово v0.2)
- ~Количество просмотров на посте~ (готово v0.2)
- ~Список реакций~ (невозможно)
- ~Комментарии~ (готово v0.4)
- ~Поддержка получения видео-сообщений через [telesco.pe](https://telesco.pe/)~ (готово v1.0, см [CHANGELOG](#changelog))
- ~В далеком будующем сделать на основе этого REST API~ (готово v0.6)


# CHANGELOG
- **1.0**:
добавлена возможность получения как видео-сообщений, так и видео-файлов и голосовых сообщений. добавлена переменная `media_type`, см [описание](./REF.md#media_type)

- **0.6**:
сделан REST API, добавлена возможность загружать больше актуальных постов, переписана документация

- **0.5**:
отредактирован выхлоп если информация отсуствует. переписан и выложен в открытый доступ тест

- **0.4**: 
добавлено `pytgcf.get(name).post(id).comments(comment_id, limit=10)` 

- **0.3**:
`pytgcf.get(name).posts(id)` заменен на `pytgcf.get(name).post(id)`, выдает теперь не список, а готовый класс с нужной информацией о посте 

- **0.2**:
теперь при вызове `pytgcf.get(name)` создается класс с информацией о канале, где `name` это сокращенное имя (link) на канал. реализован там почти половина TODO. посты получать в `pytgcf.get(name).posts(id)` или готовый `pytgcf.get(name).latests` где 20 последних постов

- **0.1**:
проект создан.
`pytgcf.get(name,id)` выводит список из словарей с информацией о посте
