import json


class ViewChangeMessage:

    def __init__(self, newView, lastStableCheckpoint, c, p, signature, addr):
        self.new_view = newView
        self.last_stable_checkpoint = lastStableCheckpoint
        self.c = c
        self.p = p
        self.signature = signature
        self.addr = addr

    # 多播
    def Broadcast(self, endpoints):
        data = json.dumps(self, default=lambda obj: obj.__dict__)
        print(data)
        return True

    # 检查是否正确
    def Check(self):
        return True

    # 等待回收该信息
    def WaitRecv(self):
        return True
