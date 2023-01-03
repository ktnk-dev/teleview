import pytgcf
from colorama import (init as colorama_init, Fore as color)
colorama_init()
channel = True
nonexistchannel = False
summary = {
    'all': 0,
    'ok': 0,
    'warn': 0,
    'false': 0
}

def beauty(data):
    status_text = 'Успешно' if data['status'] == True else 'Провалено'
    status_color = color.LIGHTGREEN_EX if data['status'] == True else color.LIGHTRED_EX if data['status'] == False else ...
    title = f'——— {data["task"]} | {status_color}{status_text}{color.RESET} ———'
    output = title+''
    for test in data['tests']:
        test_status_text = 'Успешно' if test['status'] == True else 'Частично успешно' if test['status'] == None else 'Провалено'
        test_status_color = color.LIGHTGREEN_EX if test['status'] == True else color.LIGHTYELLOW_EX if test['status'] == None else color.LIGHTRED_EX
        result = f'• {test["text"]}: {test_status_color}{test_status_text}{color.RESET}'
        if test['status'] != True:
            result += f'\n  Несоотвествие: {color.LIGHTYELLOW_EX}{test["a"]} {color.LIGHTRED_EX}!= {color.LIGHTGREEN_EX}{test["b"]}{color.RESET}'
            result += f'\n  Примечание: {test["critical_text"]}{color.RESET}' if test['critical_text'] else ''
        output+='\n'+result     
    return output+'\n'

def equal(a, b, text, critical=None):
    result = {}
    summary['all'] += 1
    result['text'] = text if text else None
    result['a'] = a
    result['b'] = b
    if a == b:
        summary['ok'] += 1
        return {
            'status': True,
            'text': text if text else None,
            'a': a,
            'b': b
        }
    else:
        result['status'] = None if critical != True else False
        summary['warn']  += 1 if critical != True else 0
        summary['false'] += 1 if critical == True else 0
        result['critical_text'] = critical if type(critical) == str else None

    return result
        

def findchannel():
    global channel
    channel = pytgcf.get('durov')
    result = {}
    result['task'] = 'Поиск существующего канала'
    data = []
    if channel.status:
        result['status'] = True
        data.append(equal(channel.name, "Durov's Channel", 'Сравнение названия', 'Название канала может несоотвествовать'))
        data.append(equal(channel.description, "Thoughts from the Product Manager / CEO / Founder of Telegram.", 'Сравнение описания', 'Описание канала может несоотвествовать'))
        data.append(equal('telegram-cdn.org/file/' in channel.picture, True, 'Сравнение фотографии канала', 'Фотография канала может несоотвествовать'))
    else: 
        result['status'] = False
        data.append(equal(None, "Durov's Channel", 'Сравнение названия', True))
        data.append(equal(None, "Thoughts from the Product Manager / CEO / Founder of Telegram.", 'Сравнение описания', True))
        data.append(equal('telegram-cdn.org/file/' in '', True, 'Сравнение фотографии канала', True))
    result['tests'] = data
    return result

def findunexistchannel():
    global nonexistchannel
    result = {}
    result['task'] = 'Поиск несуществующего канала'
    nonexistchannel = pytgcf.get('channel-not-exists')
    result['status'] = not nonexistchannel.status
    result['tests'] = [equal(nonexistchannel.status, None,'Ненахождение этого канала', True)]
    return result


def findpostinunexistchannel():
    result = {}
    result['task'] = 'Поиск поста в несуществующем канале'
    r = nonexistchannel.post(99999)
    result['status'] = not r
    result['tests'] = [equal(r, None,'Ненахождение этого поста', True)]
    return result

def findunexistpostchannel():
    result = {}
    result['task'] = 'Поиск несуществующего поста в канале'
    r = channel.post(9999999)
    result['status'] = not r
    data = [equal(r, None,'Ненахождение этого поста', True)]
    result['tests'] = data
    return result

def findexistchannelpost():
    result = {}
    global post
    result['task'] = 'Поиск существующего поста в канале'
    post = channel.post(37)
    result['status'] = True if post else False
    if post: data = [equal(post.text,'I wonder who lit up all the candles in the cemetery 🎃' ,'Сравнение текста', 'Текст сообщения может отличаться'),
                    equal(post.datetime, '2015-10-31T19:41:48+00:00', 'Сравнение времини отправки', True),
                    equal('telegram-cdn.org/file/' in post.media[0], True, 'Сравнение фотографии', 'Ссылка на фотографию может отличаться')]
    else: data = [equal(None,'I wonder who lit up all the candles in the cemetery 🎃' ,'Сравнение текста', True),
                  equal(None, '2015-10-31T19:41:48+00:00', 'Сравнение времини отправки', True),
                  equal('telegram-cdn.org/file/' in '', True, 'Сравнение фотографии', True)]
    result['tests'] = data
    return result

def loadnonexistscommentsfrompost():
    result = {}
    result['task'] = 'Поиск несуществующих комментариев в посте'
    clim = post.comments()
    cid = post.comments(id=1234)
    if clim == cid == None: result['status'] = True
    else: result['status'] = False
    result['tests'] = [ equal(clim, None, 'Ненахождение последних комментариев', True),
                        equal(cid, None, 'Ненахождение определенннго комментария', True)]
    return result


def loadexistcomments():
    global channel
    result = {'task': 'Поиск существующего комментария'}
    channel = pytgcf.get('contest') 
    c = channel.post(198).comments(141108)
    result['status'] = True if c else False
    data = [
        equal(c.author.name, 'Deleted Account', 'Сравнение автора', 'Автор мог восстановить свой аккаунт'),
        equal(c.text, 'Im Rassia......', 'Сравнение текста', 'Текст может отличаться'),
        equal(c.datetime, '2021-01-09T20:05:40+00:00', 'Сравнение даты отправки', True),
        equal(c.reply, 130198, 'На какой комментарий был ответ', True),
    ] if c else [
        equal(None, 'Deleted Account', 'Сравнение автора', True),
        equal(None, 'Im Rassia......', 'Сравнение текста', True),
        equal(None, '2021-01-09T20:05:40+00:00', 'Сравнение даты отправки', True),
        equal(None, 130198, 'На какой комментарий был ответ', True),
    ]
    result['tests'] = data
    return result




print(beauty(findunexistchannel()))
print(beauty(findpostinunexistchannel()))

print(beauty(findchannel()))
print(beauty(findunexistpostchannel()))
print(beauty(findexistchannelpost()))
print(beauty(loadnonexistscommentsfrompost()))
print(beauty(loadexistcomments()))

print(f'''——— Тесты завершены ———
Успешно: {color.LIGHTRED_EX if summary['ok'] == 0 else color.LIGHTGREEN_EX}{summary['ok']}{color.RESET}
Частично успешно: {color.LIGHTGREEN_EX if summary['warn'] == 0 else color.LIGHTYELLOW_EX}{summary['warn']}{color.RESET}
Провалено: {color.LIGHTGREEN_EX if summary['false'] == 0 else color.LIGHTRED_EX}{summary['false']}{color.RESET}''')
