from .corotune import *
from .models import *

version = '1.2.1'
source = 'https://github.com/ktnk-dev/teleview'
random_UA = True
request_header = {
    'User-Agent': '1'
}

if random_UA:
    import random
    request_header['User-Agent'] = random.choice(['Windows','MacOS','Linux','iPhone', 'Android'])+'; '+random.choice(['Chrome 100', 'Firefox 93', 'Safari 14', 'Opera 30', 'Edge'])