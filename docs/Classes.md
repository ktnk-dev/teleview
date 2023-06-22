## *class* `Channel`
- *prop* `url [str]` - Ссылка на канал 
- *prop* `name [str]` - Название канала
- *prop* `description [str]` - Описание канала
- *prop* `subscribers [int]` - Количество подписчиков на канал
- *prop* `picture [str | None]` - Ссылка на картинку канала
- *prop* `private [bool]` - Приватный канал или нет
<!-- <hr> -->

- *async func* [`getPost`](./Functions.md#function-getpost) - Функция для получения поста в канале по ID 
- *async func* [`getLatest`](./Functions.md#function-getlatest) - Функция для получения последних 20 постов в канале
- *async func* [`getAllPosts`](./Functions.md#function-getallposts) - Функция для получения **всех** постов в канале
- *async func* [`isPublic`](./Functions.md#function-ispublic) - Узнать приватный канал или нет
- *async func* [`isPrivate`](./Functions.md#function-isprivate) - Узнать публичный канал или нет
- *async func* [`toDict`](./Functions.md#function-todict) - Функция для отображения всех данных в формате словаря
<hr>

## *class* `Post`
- *prop* `channel [class `[`Channel`](#class-channel)`]` - обьект канала
- *prop* `url [str]` - ссылка на пост 
- *prop* `id [int]` - ID поста
- *prop* `text [str | None]` - текст поста
- *prop* `media [list[`[`Media`](#class-media)`]]` - список Медиа обьектов (фото, видео итд)
- *prop* `views [int]` - количество просмотров 
- *prop* `datetime [str]` - строка с датой и временем отправки поста в GMT+0
<!-- <hr> -->

- *async func* [`getComments`](./Functions.md#function-getcomments) - Функция для получения последних комментариев "под" постом
- *async func* [`getComment`](./Functions.md#function-getcomment) - Функция для получения комментария по ID
- *async func* [`toDict`](./Functions.md#function-todict) - Функция для отображения всех данных в формате словаря
<hr>

## *class* `Media`
- *prop* `url [str]` - ссылка на загрузку медиа-контента
- *prop* `type [str]` - тип медиа-контента (*photo, video, round_video, voice* / *jpg, mp4, mp4, ogg* )
<!-- <hr> -->

- *async func* [`toDict`](./Functions.md#function-todict) - Функция для отображения всех данных в формате словаря
<hr>

## *class* `Comment`
- *prop* `post [class `[`Post`](#class-post)`]` - обьект поста
- *prop* `id [int]` - ID комментария
- *prop* `text [str]` - текст комментария
- *prop* `reply [int | None]` - ID комментария на который был произведен ответ
- *prop* `author [class `[`Author`](#class-author)`]` - класс где хранится информация об авторе комментария
- *prop* `datetime [str]` - строка с датой и временем отправки комментария в GMT+0
<!-- <hr> -->

- *async func* [`toDict`](./Functions.md#function-todict) - Функция для отображения всех данных в формате словаря

<hr>

## *class* `Author`
- *prop* `name [str]` - имя пользователя
- *prop* `username [str | None]` - ЮЗ пользователя
- *prop* `photo [str | None]` - ссылка на фотографию профиля 
<!-- <hr> -->

- *async func* [`toDict`](./Functions.md#function-todict) - Функция для отображения всех данных в формате словаря
<!-- <hr> -->





