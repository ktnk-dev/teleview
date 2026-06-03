from functools import wraps as _wraps


_TEMPLATES = './teleview/docs/templates/'
_DB = {
    ''
}

def _AddModel(cls):
    ...

def ModelDocumentation(cls):
    _DB['models'] = _AddModel(cls)
    return cls


def CallDocumentation(
    origin: str,
    raises: list[BaseException],
    support_required: list[str]
):
    ...