from functions.Replyer import ReplyerDecorator

elect_list = {}
elect_reject = False


@ReplyerDecorator
def Elect(msg):
    global elect_list
    value = msg['arg']['value']
    addr = msg['arg']["addr"]
    loopid = msg['arg']["loopid"]
    if loopid not in elect_list.keys():
        elect_list[loopid] = {}
    elect_list[loopid][addr] = value
    r = {}
    reply = {
        "view": msg['view'],
        "timestamp": msg['timestamp'],
        "c": msg['arg']['endpoint'],
        "i": msg['i'],
        "r": r,
    }
    return reply


@ReplyerDecorator
def StopElect(msg):
    global elect_reject
    elect_reject = True
    r = {}
    reply = {
        "view": msg['view'],
        "timestamp": msg['timestamp'],
        "c": msg['arg']['endpoint'],
        "i": msg['i'],
        "r": r,
    }
    return reply
