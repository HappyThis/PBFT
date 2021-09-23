from functools import wraps

import requests


def ReplyerDecorator(f):
    @wraps(f)
    def NewFunction(*args, **kwargs):
        reply = f(*args, **kwargs)
        ret = requests.post(reply["c"], json=reply)
        return ret

    return NewFunction
