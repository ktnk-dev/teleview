# Teleview models
Basic models that are used in teleview library
 
# Channel
> Represents channel
## Fields
- `id`: _str_ | _int_ | _False_ 
- `url`: _str_ | _False_ 
- `name`: _str_ 
- `picture`: [_Media_](./MODELS.md#Media) | _bool_ 
- `description`: _str_ | _bool_ 
- `subscribers`: _str_ 
- `_iternal`: _dict_ — Any optional data that provider returned
## Channel.getPost
> Async function to get channel's post by query

_async_  `Channel.getPost(query)` → [`Post`](./MODELS.md#Post)
### Arguments
- `query`: _str_ | _int_ — Something, that can be used to find content. Type and kind depends on provider
### Support required: `PostOutput`
### Exceptions: [`PostNotFound`](./EXCEPTIONS.md#PostNotFound), [`NotSupported`](./EXCEPTIONS.md#NotSupported)

## Channel.getPosts
> Async function to get posts from channel

_async_ [_generator_](./TYPE_HINTS.md#Generator)  `Channel.getPosts(limit)` → [`Post`](./MODELS.md#Post)
### Arguments
- `limit`: _int_ — Amount of posts, set to 0 to get all posts if possible
### Support required: `StreamPostOutput`
### Exceptions: [`PostNotFound`](./EXCEPTIONS.md#PostNotFound), [`NotSupported`](./EXCEPTIONS.md#NotSupported)

## Channel.toDict
> Returns dict representation of object

_async_  `Channel.toDict()` → `dict`
### Dont require arguments

# Post
> Represents post's comment
## Fields
- `channel`: [_Channel_](./MODELS.md#Channel) 
- `author`: [_Author_](./MODELS.md#Author) 
- `id`: _str_ | _int_ | _False_ 
- `url`: _str_ | _False_ 
- `text`: _str_ | _False_ 
- `views`: _int_ — Amount of views
- `media`: _list[Media]_ — Media attached to comment
- `datetime`: _datetime_ 
- `_iternal`: _dict_ — Any optional data that provider returned
## Post.getComment
> Async function to get post's comment by query

_async_  `Post.getComment(query)` → [`Comment`](./MODELS.md#Comment)
### Arguments
- `query`: _str_ | _int_ — Something, that can be used to find content. Type and kind depends on provider
### Support required: `CommentOutput`
### Exceptions: [`CommentNotFound`](./EXCEPTIONS.md#CommentNotFound), [`NotSupported`](./EXCEPTIONS.md#NotSupported)

## Post.getComments
> Async function to get comments from post

_async_ [_generator_](./TYPE_HINTS.md#Generator)  `Post.getComments(limit)` → [`Comment`](./MODELS.md#Comment)
### Arguments
- `limit`: _int_ — Amount of comments, set to 0 to get all comments if possible
### Support required: `StreamCommentOutput`
### Exceptions: [`CommentNotFound`](./EXCEPTIONS.md#CommentNotFound), [`NotSupported`](./EXCEPTIONS.md#NotSupported)

## Post.toDict
> Returns dict representation of object

_async_  `Post.toDict()` → `dict`
### Dont require arguments

# Comment
> Represents post's comment
## Fields
- `post`: [_Post_](./MODELS.md#Post) 
- `id`: _str_ | _int_ | _False_ 
- `url`: _str_ | _False_ 
- `text`: _str_ | _False_ 
- `media`: _list[Media]_ — Media attached to comment
- `author`: [_Author_](./MODELS.md#Author) 
- `datetime`: _datetime_ 
- `_iternal`: _dict_ — Any optional data that provider returned
## Comment.toDict
> Returns dict representation of object

_async_  `Comment.toDict()` → `dict`
### Dont require arguments

# Media
> Represents any media content (profile picuters, photos in posts, etc)
## Fields
- `url`: _str_ — Direct URL to media
- `type`: _str_ — Kind of media, <b>depends on provider</b>
- `mimetype`: _str_ 
## Media.toDict
> Returns dict representation of object

_async_  `Media.toDict()` → `dict`
### Dont require arguments

# Author
> Represents comment or post author
## Fields
- `name`: _str_ — Author's name
- `picture`: [_Media_](./MODELS.md#Media) | _False_ — Author's profile picture
## Author.toDict
> Returns dict representation of object

_async_  `Author.toDict()` → `dict`
### Dont require arguments
