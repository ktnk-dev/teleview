# Teleview calls
Here are functions that can be called in `teleview` module

## teleview.setProvider
> Set provider from provided module

_sync_  `teleview.setProvider(module)` → `None`
### Arguments
- `module`: _module_ — This call excepts <b>module</b> instead class
### Exceptions: [`ProvderNotSupported`](./EXCEPTIONS.md#ProvderNotSupported)

## teleview.setHeaders
> Set headers that will pass to requests

_sync_  `teleview.setHeaders(headers)` → `None`
### Arguments
- `headers`: _dict_ 

## teleview.setProxy
> Set `http` or `socks` proxy for all requests.
Format: `http://user:password@proxy_host:port`


_sync_  `teleview.setProxy(proxy_url)` → `None`
### Arguments
- `proxy_url`: _str_ | _None_ 

## teleview.getChannels
> Async function to get multiple channels by query

_async_ [_generator_](./TYPE_HINTS.md#Generator)  `teleview.getChannels(query, limit)` → [`Channel`](./MODELS.md#Channel)
### Arguments
- `query`: _str_ | _int_ — Something, that can be used to find content. Type and kind depends on provider
- `limit`: _int_ — Amount of channels to find, set to 0 to get all channels
### Support required: `StreamChannelOutput`
### Exceptions: [`NotSupported`](./EXCEPTIONS.md#NotSupported)

## teleview.getChannel
> Async function to get single channel by query

_async_  `teleview.getChannel(query)` → [`Channel`](./MODELS.md#Channel)
### Arguments
- `query`: _str_ | _int_ — Something, that can be used to find content. Type and kind depends on provider
### Exceptions: [`ChannelNotFound`](./EXCEPTIONS.md#ChannelNotFound)

## teleview.getPosts
> Alias to [`Channel.getPosts()`](./MODELS.md#Channel.getPosts)

_async_ [_generator_](./TYPE_HINTS.md#Generator)  `teleview.getPosts(channel, limit)` → [`Post`](./MODELS.md#Post)

## teleview.getPost
> Alias to [`Channel.getPost()`](./MODELS.md#Channel.getPost)

_async_  `teleview.getPost(channel, query)` → [`Post`](./MODELS.md#Post)

## teleview.getComments
> Alias to [`Post.getComments()`](./MODELS.md#Post.getComments)

_async_ [_generator_](./TYPE_HINTS.md#Generator)  `teleview.getComments(post, limit)` → [`Comment`](./MODELS.md#Comment)

## teleview.getComment
> Alias to [`Post.getComment()`](./MODELS.md#Post.getComment)

_async_  `teleview.getComment(post, query)` → [`Comment`](./MODELS.md#Comment)
