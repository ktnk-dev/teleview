 [Release notes](./docs/RELEASENOTES.md) | [Documentation](./docs/md/README.md) | [Installation](./docs/INSTALLATION.md) `WIP`

# About *Teleview*
- Async Python library to get channels, posts and comments
- Version: `release`/`3.2`
- Providers: `telegram` (by default)
- Dependencies: `aiohttp`, `bs4`

# What are *providers*
- Providers allow to get info from different social networks using only *Teleview* package!
- Output is standardized and prototyped. You can change providers *on the fly* without changing your code!

### *Teleview* capabilities with `telegram` provider
- Get channel information: name, description, photo and more...
- Get posts in channel: by ID, latest, even *all* posts in channel
- Get text, media, views and datetime from posts
- Get comments sent in post: by ID or 100 latest

# TODO
- [*telegram*] Get media from comments
- [*teleview*] `TGstat` and `VK` providers
