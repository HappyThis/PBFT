import threading
import time
from functools import wraps

import requests

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
    func = msg['arg']['func']
    # 为了简单，还是之前的节点
    newUrl = "http://127.0.0.1:5000/recvNodesMessage"
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
        global message, lock
        timestamp = str(int(round(time.time() * 1000000)))
        # 时间戳注射
        # 回调地址注射
        # 地址注射
        kwargs["timestamp"] = timestamp
        kwargs["endpoint"] = "http://127.0.0.1:5000/recvCommitteesReply"
        kwargs["addr"] = ""
        url = kwargs["url"]
        msg = api(*args, **kwargs)
        # 线程安全保护开始
        lock.acquire()
        timer = threading.Timer(10, TimeOutHandler, kwargs={"msg": msg})
        message[timestamp] = [set(), timer]
        timer.start()
        lock.release()
        # 线程安全保护结束
        ret = requests.post(url, json=msg)
        return ret

    return NewFunction


def ReplyCollecter(msg):
    global message, lock
    lock.acquire()
    timestamp = msg["timestamp"]
    sender = msg["c_addr"]
    senderSet = message[timestamp][0]
    senderSet.add(sender)
    from consensus.PbftProcess import pbftCore
    if len(senderSet) >= 2 * pbftCore.f + 1:
        message[timestamp][1].cancel()
        del message[timestamp]
        print("get 2*f+1 reply:", timestamp)
    lock.release()
