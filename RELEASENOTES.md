# 3.0
Since changes may break existing software, major version tag has been changed
## `teleview` _library_

### User-side calls
- `teleview.setProxy` now accepts `None` to disable proxy
- `teleview.setProxy` now supports `socks` proxy format (with authorization)
- _new_ `teleview.setCacheTimeout`, accepts timeout in seconds, more in `Cache manager` section. Caching can be disabled by setting timeout to zero

### Models
- `Comment`, `Post` and `Channel` now have `id` field with `str | int | False` type
- in `Comment`, `Post` and `Channel` field `url` can be `False` since it is not required anymore

### Constructors
- Every constructor now shows what field raised `IncorrectConstructor` error
- `ChannelConstruct`, `PostConstructor` and `CommentConstructor` now have optional `id` field
- `ChannelConstructor` and `PostConstructor` now don't require `url` field for building
- `PostConstructor` now have `author` field set to `channel` by default, can be set to `AuthorConstructor`

### Support flags
- Now uses `enum.Flag` instead of string literals. Flags defined in `teleview.helper.enums`
- Previous supported flags now in `Supported` enum
- Added `CacheStrategy` enum for providers for cache manager

### `new` Cache manager
- `teleview.helper.caching` now has cache buffer implementation and `teleview.setCacheTimeout` for setting cache timeout from user-side
- Providers now have `CACHE_STRATEGY` field that accepts `CacheStrategy` enum values
- - `AutoByRequest` strategy automatically saves url response and returns it during cache timeout window
- - `CacheBuffer` strategy requires provider developers to implement caching mechanism by yourself, acting as key-value storage (yet, you can use buffer even without setting this flag, but anyway it's important to specify, if I decide to do something with it in future updates)
- - `NoCache` strategy just indicates library that your provider does not support caching (yet, it doesn't disallow to use buffer or own caching mechanism, more info in previous strategy)
- `teleview.helper.caching` now has `CacheBuffer` class acting as key-value storage for your cache implementation 


## `telegram` _provider_
- `id` copied from `internal` to `id` field where it was possible (`.internal['id']` still works to maintain backward compatibility)
- Now should use buffer and url response caching (`getPosts` and `getComments` fill cache buffer, `getPost` and `getComment` read if exist)
- [#3](https://github.com/ktnk-dev/teleview/issues/3) was resolved, now it should parse channel from scratch on each call


# Previous versions
_...does someone remember?_