# Type hints
This file was NOT generated

## Generator
`AsyncGenerator` return type requires special `async for` loop to work, without `await` while calling function. For example: 
```py
async for post in channel.getPosts():
    print(post.id)
```
or 
```py
[post.id async for post in channel.getPosts()]
```