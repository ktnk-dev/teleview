class ProvderNotSupported(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return 'This provider dont supported by current Teleview version'

class NotSupported(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return 'This call not supported by your provider'
    
class ChannelNotFound(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return 'Channel not found'
    
class PostNotFound(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return 'Post not found'
    
class CommentNotFound(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return 'Comment not found'
    
class IncorrectConstructor(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return 'Constructor failed to build object'