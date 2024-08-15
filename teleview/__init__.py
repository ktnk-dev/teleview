# from .corotune import *
from .helper.provider import VERSION, setHeaders, setProvider
# from .provider import telegram

from . import helper, models, exceptions, provider

from .corotune import *

version: float = VERSION # alias

setProvider(provider.telegram)
setHeaders({'User-Agent': f'teleview {VERSION}'})