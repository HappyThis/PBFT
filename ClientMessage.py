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

    # 返回结果
    # 结果，执行者对结果的签名，执行者链上地址
    def Exec(self, endpoint):
        # 创建进程执行
        api = endpoint + "funcRouter"
        self.arg["addr"] = self.clinet_addr
        ret = requests.post(api, json=self.arg)
        return True
