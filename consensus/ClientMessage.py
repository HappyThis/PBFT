# class客户端请求
import requests


class ClientMessage:
    def __init__(self, signature, clinetAddr, arg, timestamp):
        self.signature = signature
        self.clinet_addr = clinetAddr
        self.arg = arg
        self.timestamp = timestamp,

    # 检查是否正确
    def Check(self):
        return True

    # 生成摘要
    def Digest(self):
        return True
