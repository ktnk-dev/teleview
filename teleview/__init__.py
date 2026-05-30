# from .corotune import *
from .helper.provider import VERSION, setHeaders, setProvider
from .helper.web import setProxy
from .helper.caching import setCacheTimeout
# from .provider import telegram

from . import helper, models, exceptions, provider

from .corotune import (
    getChannels,
    getChannel,
    getPosts,
    getPost,
    getComments,
    getComment,
)

version: float = VERSION # alias

setProvider(provider.telegram)
setHeaders({'User-Agent': f'teleview {VERSION}'})
setCacheTimeout(300)