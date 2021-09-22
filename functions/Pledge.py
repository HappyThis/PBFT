from functions.Replyer import ReplyerDecorator

pledge_list = {}
pledge_reject = False


@ReplyerDecorator
def Pledge(msg):
    global pledge_list
    value = msg['value']
    addr = msg["addr"]
    loopid = msg["loopid"]
    if loopid not in pledge_list.keys():
        pledge_list[loopid] = {}
    pledge_list[loopid][addr] = value


@ReplyerDecorator
def StopPledge(msg):
    global pledge_reject
    pledge_reject = True
