import json
import typing
import inspect
import collections

from functools import wraps as _wraps
from datetime import datetime as _dt

from .helper.version import VERSION as _VERSION
_QUEUE = []
_DB = {
    'metadata': {
        'build_at': _dt.now().isoformat(),
        'version': _VERSION
    },
    'exceptions': {},
    'models': {},
    'calls': {}
}
def ModelDocumentation(params_docs: dict[str, str], index: int = 0):
    def wrapper(cls):
        if cls.__name__ not in _DB['calls']: _DB['calls'][cls.__name__] = {}
        if cls.__name__ not in _DB['models']: _DB['models'][cls.__name__] = {}
        params = {}
        hints = typing.get_type_hints(cls)
        for param_name in cls.__slots__:
            param_type = hints.get(param_name)

            if param_type == inspect.Parameter.empty:
                param_actual_type = [None]
            
            if param_type.__name__ == 'list':
                param_actual_type = [f'list[{str(typing.get_args(param_type)[0].__name__).split(".")[-1]}]']
            
            elif ' | ' in str(param_type): 
                types = str(param_type)
                if param_name+'?' in params_docs:
                    types = types.replace('bool', 'False')
                    
                param_actual_type = [p.split('.')[-1] for p in types.split(' | ')]
                
            else: 
                param_actual_type = [param_type.__name__]
            
            if param_name == 'query':
                params[param_name] = 'Something, that can be used to find content. Type and kind depends on provider'
            
            docs = params_docs.get(param_name, params_docs.get(param_name+'?', None))
            params[param_name] = {
                'types': param_actual_type,
                'docs': docs if docs != '' else None
            }
    
        _DB['models'][cls.__name__] = {
            'params': params,
            'docs': cls.__doc__,
            'index': index
        }
        return cls
    return wrapper


def CallDocumentation(
    origin: str,
    support_required: list[str],
    exceptions: list[BaseException] = [],
    args: dict[str, str] = {},
    index: int = 0,
    alias: str | None = None
):
    def outer(func):
        def worker():
            if origin not in _DB['calls']: _DB['calls'][origin] = {}
            for e in exceptions:
                if e not in _DB['exceptions']: 
                    _DB['exceptions'][e.__name__] = str(e())
            
            hints = typing.get_type_hints(func)
            sig = inspect.signature(func)
            arguments = {}
            for param_name, param in sig.parameters.items():
                if param_name == 'self': continue
                param_type = hints.get(param_name, param.annotation)
                if param_type == inspect.Parameter.empty:
                    param_actual_type = [None]
                elif ' | ' in str(param_type): 
                    param_actual_type = str(param_type).split(' | ')
                else: 
                    param_actual_type = [param_type.__name__]
                
                if param_name == 'query':
                    args[param_name] = 'Something, that can be used to find content. Type and kind depends on provider'
                
                arguments[param_name] = {
                    'types': param_actual_type,
                    'docs': args.get(param_name, None)
                }

            return_type = hints.get('return')
            origin_return = typing.get_origin(return_type)
            is_async_generator = origin_return is typing.AsyncGenerator or origin_return is collections.abc.AsyncGenerator
            actual_return_type = typing.get_args(return_type)[0] if is_async_generator else return_type
            if func.__name__ == 'toDict': func.__doc__ = 'Returns dict representation of object'
            symbols = {
                'support_required': support_required,
                'arguments': arguments,
                'docs': func.__doc__ if not alias else '',
                'exceptions': [e.__name__ for e in exceptions],
                'is_async': inspect.iscoroutinefunction(func) or is_async_generator, # FIXME: inspect.iscoroutinefunction always returns false for some reason if return type is AsyncGenerator
                'is_async_generator': is_async_generator,
                'return': actual_return_type.__name__.replace('NoneType', 'None'),
                'index': index,
                'alias': alias
            }
            _DB['calls'][origin][func.__name__] = symbols
            # print(symbols)
        _QUEUE.append(worker)
        
        _wraps(func)
        def wrapper(*args, **kwargs): return func(*args, **kwargs)
        return wrapper
    return outer


def build_md(path: str):
    def generate_argument_docs(name, data):
        return f'''- `{name}`: {' | '.join([f'[_{t}_](./MODELS.md#{t})' if t in _DB["models"] else f'_{t}_'  for t in data['types']])} {f'— {data["docs"]}' if data['docs'] else ''}'''
    
    def generate_func_doc(name, func, origin):
        ident = '#'*(3 if origin == 'teleview' else 3)
        text = f'''\
{ident[:-1]} {origin}.{name}
'''
        if func['alias']:
            cls: str = func['alias'].split('.')[0]
            func_name: str = func['alias'].split('.')[1]
            ref = f'[`{cls}.{func_name}()`](./MODELS.md#{cls}.{func_name})' if cls in _DB['calls'] and func_name in _DB['calls'][cls] else f'`{cls}.{func_name}()`'
            text += f'> Alias to {ref}\n'
        else:
            text += f"> {func['docs']}\n"
        
        text += f'\n{'_async_ ' if func['is_async'] else '_sync_ '}{'[_generator_](./TYPE_HINTS.md#Generator) ' if func['is_async_generator'] else ''} `{origin}.{name}({', '.join([k for k in func['arguments'].keys()])})` → {f'[`{func['return']}`](./MODELS.md#{func['return']})' if func['return'] in _DB['models'] else f'`{func['return']}`'}\n'
        if func['alias']: return text
        
        
        if func['arguments']:
            text += f'''{ident} Arguments\n'''
            for arg, data in func['arguments'].items():
                text += generate_argument_docs(arg, data)+'\n'
        else: text += f'''{ident} Dont require arguments\n'''
        
        if func['support_required']: 
            text += f'''{ident} Support required: {', '.join([f'`{_}`' for _ in func['support_required']])}\n'''
        
        if func['exceptions']:
            text += f'''{ident} Exceptions: {', '.join([f'[`{_}`](./EXCEPTIONS.md#{_})' for _ in func['exceptions']])}\n'''
        
        
        return text
    
    if path[-1] == '/': path = path[:-1]
    with open(f'{path}/README.md', 'w', encoding='utf-8') as file:
        file.write(f'''
# Teleview Docs
- Version: `{_VERSION}`
- Generated at: `{_DB['metadata']['build_at']}`

### [Calls](./CALLS.md)
### [Models](./MODELS.md)
### [First steps](./INTRO.md)
### [Exceptions](./EXCEPTIONS.md)
### [Type hints](./TYPE_HINTS.md)
### [Creating provider ↗](../../teleview/provider/demo.py)
''')
    
    with open(f'{path}/CALLS.md', 'w', encoding='utf-8') as file:
        sorted_keys = {k: v['index'] for k, v in _DB['calls']['teleview'].items()}
        call_names = list(sorted(sorted_keys, key=lambda d: sorted_keys[d]))
        texts = []
        
        for name in call_names:
            func = _DB['calls']['teleview'][name]
            texts.append(generate_func_doc(name, func, 'teleview'))
            
        file.write(f'''\
# Teleview calls
Here are functions that can be called in `teleview` module

'''+'\n'.join(texts))    
    
    with open(f'{path}/MODELS.md', 'w', encoding='utf-8') as file:
        sorted_keys = {k: v['index'] for k, v in _DB['models'].items()}
        model_names = list(sorted(sorted_keys, key=lambda d: sorted_keys[d]))
        texts = []
        
        for model_name in model_names:
            texts.append(f'# {model_name}')
            texts.append(f'> {_DB['models'][model_name]['docs']}')
            texts.append(f'## Fields')
            
            for param_name, data in _DB['models'][model_name]['params'].items():
                texts.append( generate_argument_docs(param_name, data))
            
            for func_name, func in _DB['calls'][model_name].items():
                texts.append(generate_func_doc(func_name, func, model_name))
            
        file.write(f'''\
# Teleview models
Basic models that are used in teleview library
 
'''+'\n'.join(texts))  
    
    with open(f'{path}/EXCEPTIONS.md', 'w', encoding='utf-8') as file:
        exceptions = [f'## {e}\n{s}\n' for e, s in _DB['exceptions'].items()]
        file.write(f'''\
# Teleview exceptions
Exceptions can be imported from `teleview.exceptions`

{'\n'.join(exceptions)}
''')
    

def build_web(path: str): # TODO
    if path[-1] == '/': path = path[:-1]
    with open(f'{path}/symbols.json', 'w', encoding='utf-8') as symbols:
        data = json.dumps(_DB, ensure_ascii=False, indent=2)
        symbols.write(data)
        # print(data)
        

def build():
    [f() for f in _QUEUE]
    build_md('./docs/md')
    build_web('./docs/web')
    