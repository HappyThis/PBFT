import json

import requests


class PrepareMessage:

    def __init__(self, view, nonce, digest, signature, addr):
        self.view = view
        self.nonce = nonce
        self.digest = digest
        self.signature = signature
        self.addr = addr

    # 多播
    def Broadcast(self, endpoints):
        data = self.__dict__
        for ep in endpoints:
            api = ep + "prepare"
            ret = requests.post(api, json=data)
            print("sent prepared to ", ep)
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
