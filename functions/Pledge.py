from functions.Replyer import ReplyerDecorator

pledge_list = {}
pledge_reject = False


@ReplyerDecorator
def Pledge(msg):
    global pledge_list
    value = msg['arg']['value']
    addr = msg["addr"]
    loopid = msg['arg']["loopid"]
    if loopid not in pledge_list.keys():
        pledge_list[loopid] = {}
    pledge_list[loopid][addr] = value
    r = {}
    reply = {
        "view": msg['view'],
        "timestamp": msg['timestamp'],
        "c": msg['arg']['endpoint'],
        "c_addr": addr,
        "i": msg['i'],
        "r": r,
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
    }
    return reply
