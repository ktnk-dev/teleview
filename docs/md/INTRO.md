# First steps in Teleview
This file was NOT generated. Teleview version - `3.0`

This is fully async library, so you should create new async function to run library
 

```python
import teleview, asyncio

async def main():
    # Your code here

asyncio.run(main())
```

By default library using Telegram provider. It allows to get Telegram channels, lets get Durov's channel. You can use t.me link or @. I used @ in this example

```python
channel = await teleview.getChannel('@durov')
print(channel.name) # -> Pavel Durov
print(channel.description) # -> Founder of Telegram
```

Goverment blocked Telegram? You can set proxy server in Teleview

```python
teleview.setProxy('socks5://example.com:1080')
```

By the way, you can also set custom headers

```python
teleview.setHeaders({
    'User-Agent': '...', 
    ...
})
```

Now lets get 20 latest Durov's posts in channel

```python
async for post in channel.getPosts(limit = 20):
    print(post.url, post.text)
```

Then lets get specific post by its ID


```python
post = await channel.getPost(37)
print(post.url) # -> https://t.me/durov/37
print(post.text) # -> I wonder who lit up all the candles in the cemetery 🎃
print(post.media[0].url)
```

Every [model](./MODELS.md) support `.toDict()` call, lets try it 

```python
print(await channel.toDict()) 
"""
{
    "id": "durov",
    "url": "https://t.me/durov",
    "name": "Pavel Durov",
    "picture": {
        "url": "https://cdn.telesco.pe/file/XXXXXX.jpg",
        "type": "photo",
        "mimetype": "image/jpeg"
    },
    "description": "Founder of Telegram.",
    "subscribers": XXXXXX
}
"""

print(await post.toDict()) 
"""
{
    "channel": {...},
    "author": {...},
    "id": 37,
    "url": "https://t.me/durov/37",
    "text": "I wonder who lit up all the candles in the cemetery 🎃",
    "views": XXXXXX,
    "media": [
        {
            "url": "https://cdn.telesco.pe/file/XXXXXX.jpg",
            "type": "photo",
            "mimetype": "image/jpeg"
        }
    ],
    "datetime": "2015.10.31 19:41:48"
}
"""
```

Now lets get comments in post. Durov disabled comments in his channels, so lets change channel


```python
channel = await teleview.getChannel('@d_code')
post = await channel.getPost(19927)

async for comment in post.getComments(limit = 100): 
	# Note: here is only ~20 comments, so only ~20 will returned from newest to oldest
	print(f'{comment.author.name}: {comment.text}')

# We also can get comment by ID
comment = await post.getComment(566783)
print(comment.text) # -> Всё равно ВК Видео залупа
```

Comments also support `.toDict()`