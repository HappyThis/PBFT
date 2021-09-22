elect_list = {}
elect_reject = False


def Elect(msg):
    global elect_list
    value = msg['value']
    addr = msg["addr"]
    loopid = msg["loopid"]
    if loopid not in elect_list.keys():
        elect_list[loopid] = {}
    elect_list[loopid][addr] = value


def StopElect(msg):
    global elect_reject
    elect_reject = True
