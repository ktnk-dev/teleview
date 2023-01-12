# О проекте 
- Сервер создается на базе `http.server`. Проблем с `CORS` возникнуть не должно
- [Документация библеотеки](./README.md) 
- Зависимости: `pytgcf`, `http.server`
- Версия `pytgcf`: `>= 0.6`

# Конфигурация
- Основной скрипт: `web.py`
- Используемый порт: `9191`. Его можно отредактировать в переменной `serverPort`
- Хостнейм: любой. Редактируется переменной `hostName`
- Путь к API (/путь_к_апи/...): не используется. Можно указать в переменной `api_path`

# Документация
Все запросы отправляются как `GET`. Весь ответ приходит ввиде `application/json`. Все данные возвращаются как и в библеотеке за исключением `chunk`
{} - обязательно, () - необязательно
<br>

- `/{CHANNEL_SHORT_NAME}/` → [*class*](./REF.md#class)
- `/{CHANNEL_SHORT_NAME}/post/{POST_ID}` → [*class Post*](./REF.md#class-post)
- `/{CHANNEL_SHORT_NAME}/post/{POST_ID}/comments/(LIMIT)` → *list* состоящий из [*class Comment*](./REF.md#class-comment)
- `/{CHANNEL_SHORT_NAME}/post/{POST_ID}/comment/{COMMENT_ID}` → [*class Comment*](./REF.md#class-comment)
- `/{CHANNEL_SHORT_NAME}/chunk/{LAST_LOADED_POST_ID}` → *list* состоящий из [*class Post*](./REF.md#class-post)<br> 
Прошу обратить внимание, что в данном случае запрос вернет **ВСЕ** посты, находящиеся возле поста с id `LAST_LOADED_POST_ID`, вам надо **самостоятельно** написать фильтрацию получаемых данных, если это необходимо<br>
Правильное использование: `LAST_LOADED_POST_ID` = `channel.latests[0].id` с последующим добавлением в `channel.latests` только тех постов, которых нет. добавлять полученные данные в **начало** списка (`chunk_data` + `channel.latests`) 
