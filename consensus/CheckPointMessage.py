import json

import requests


class CheckPointMessage:
    def __init__(self, nonce, view, h, signature, addr):
        self.nonce = nonce
        self.h = h
        self.view = view
        self.signature = signature
        self.addr = addr

    # 多播
    def Broadcast(self, endpoints):
        data = self.__dict__
        for ep in endpoints:
            api = ep + "bpftNetwork/checkPoint"
            ret = requests.post(api, json=data)
            print("sent checkPoint to ", ep)
        return True

    # 检查是否正确
    def Check(self):
        return True

    # 等待回收该信息
    def WaitRecv(self):
        return True

    # 签名
    def GetSignature(self):
        return 0
