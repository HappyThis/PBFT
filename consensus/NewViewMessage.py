import json


class NewViewMessage:

    def __init__(self, newView, v, o, signature, addr):
        self.new_view = newView
        self.v = v
        self.o = o
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
