import threading
from functools import wraps

lock = threading.Lock()

# 对该对象进行操作时要注意线程安全
message = {}


# 超时处理
def TimeOutHandler(msg):
    global message, lock
    lock.acquire()
    del message[msg["timestamp"]]
    lock.release()
    # 换节点
    func = msg['func']
    newUrl = ""
    if func == 'elect':
        from api.Elect import Elect
        Elect(msg['arg']['value'], newUrl)
    if func == 'stopElect':
        from api.Elect import StopElect
        StopElect(newUrl)
    if func == 'pledge':
        from api.Pledge import Pledge
        Pledge(msg['arg']['value'], newUrl)
    if func == 'stopPledge':
        from api.Pledge import StopPledge
        StopPledge(newUrl)


def SendCollecterDecorator(api):
    @wraps(api)
    def NewFunction(*args, **kwargs):
        ret = api(*args, **kwargs)
        if ret[0] != -1:
            global lock
            lock.acquire()
            message[ret[0]] = (
                ret[1], set(), threading.Timer(10, TimeOutHandler, kwargs={"msg": ret[1]})
            )
            lock.release()
        return ret

    return NewFunction


def ReplyCollecter(msg):
    global message, lock
    lock.acquire()
    timestamp = msg["timestamp"]
    sender = msg["addr"]
    senderSet = message[timestamp][1]
    senderSet.add(sender)
    from consensus.PbftProcess import pbftCore
    if len(senderSet) >= 2 * pbftCore.f + 1:
        del message[timestamp]
        print("get 2*f+1 reply:", timestamp)
    lock.release()
