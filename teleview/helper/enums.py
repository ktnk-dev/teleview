from enum import (Flag, auto as _)

class Supported(Flag):
    StreamChannelOutput = _()
    StreamPostOutput = _()
    StreamCommentOutput = _()
    PostOutput = _()
    CommentOutput = _()

class CacheStrategy(Flag):
    NoCache = _()
    CacheBuffer = _()
    AutoByRequest = _()