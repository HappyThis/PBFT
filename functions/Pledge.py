from functions.Replyer import ReplyerDecorator

pledge_list = {}
pledge_reject = False


@ReplyerDecorator
def Pledge(msg):
    global pledge_list
    value = msg['arg']['value']
    addr = msg["addr"]
    pledge_list[addr] = value
    r = {}
    reply = {
        "view": msg['view'],
        "timestamp": msg['timestamp'],
        "c": msg['arg']['endpoint'],
        "c_addr": addr,
        "i": msg['i'],
        "r": r,
        "func": "pledge",
    }
    return reply


@ReplyerDecorator
def StopPledge(msg):
    global pledge_reject
    pledge_reject = True
    addr = msg["addr"]
    r = {}
    reply = {
        "view": msg['view'],
        "timestamp": msg['timestamp'],
        "c": msg['arg']['endpoint'],
        "c_addr": addr,
        "i": msg['i'],
        "r": r,
        "func": "stopPledge",
    }
    return reply
