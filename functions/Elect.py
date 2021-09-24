from functions.Replyer import ReplyerDecorator

elect_list = {}
elect_reject = False


@ReplyerDecorator
def Elect(msg):
    global elect_list
    addr = msg["addr"]
    elect_list[addr] = msg['initMsg']
    r = {}
    reply = {
        "view": msg['view'],
        "timestamp": msg['timestamp'],
        "c": msg['arg']['endpoint'],
        "c_addr": addr,
        "i": msg['i'],
        "r": r,
        "func": "elect",
    }
    return reply


@ReplyerDecorator
def StopElect(msg):
    global elect_reject
    elect_reject = True
    addr = msg["addr"]
    r = {}
    reply = {
        "view": msg['view'],
        "timestamp": msg['timestamp'],
        "c": msg['arg']['endpoint'],
        "c_addr": addr,
        "i": msg['i'],
        "r": r,
        "func": "stopElect",
    }
    return reply
