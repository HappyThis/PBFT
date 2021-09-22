# 主节点发出的PrePrepare
import requests


class PrePrepareMessage:
    # 视图号,编号,消息摘要,对本信息的签名,签名者,请求消息
    def __init__(self, view, nonce, digest, signature, addr, clientMessage):
        self.view = view
        self.nonce = nonce
        self.digest = digest
        self.signature = signature
        self.addr = addr
        self.client_message = clientMessage

    # 检查是否正确
    def Check(self):
        return True

    # 多播
    def Broadcast(self, endpoints):
        data = self.__dict__
        for ep in endpoints:
            api = ep + "prePrepare"
            ret = requests.post(api, json=data)
            print("sent pre-prepare to ", ep)
        return True

    # 签名
    def GetSignature(self):
        return 0
