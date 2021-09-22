from multiprocessing.dummy import Process
from flask import Flask, request

from PbftCore import PbftCore
from functions.Elect import Elect, elect_reject, StopElect
from functions.Pledge import Pledge, pledge_reject, StopPledge

elect_list = {}
pledge_list = {}

pbftCore = PbftCore()


def BPFTCoreProcess():
    global pbftCore
    pbftCore.RunPbft()


process = Process(target=BPFTCoreProcess)
process.start()

app = Flask(__name__)


# 普通节点质押金以换取模型
# 非主节点只有转发的权利
@app.route('/pledge', methods=["POST"])
def pledge():
    if pledge_reject is True:
        return "reject"
    msg = request.json
    msg["type"] = "client"
    pbftCore.AddMessage(msg)
    return "ok"


# 普通节点参加选举
# 非主节点只有转发的权利
@app.route('/elect', methods=["POST"])
def elect():
    if elect_reject is True:
        return "reject"
    msg = request.json
    msg["type"] = "client"
    pbftCore.AddMessage(msg)
    return "ok"


# 接收pre-prepare
@app.route('/prePrepare', methods=["POST"])
def RecvPreprepareMsg():
    msg = request.json
    msg["type"] = "prePrepare"
    pbftCore.AddMessage(msg)
    return "ok"


# 接收commit确认
@app.route('/commit', methods=["POST"])
def RecvCommitMsg():
    msg = request.json
    msg["type"] = "commit"
    pbftCore.AddMessage(msg)
    return "ok"


# 接收prepare确认
@app.route('/prepare', methods=["POST"])
def RecvPrepareMsg():
    msg = request.json
    msg["type"] = "prepare"
    pbftCore.AddMessage(msg)
    return "ok"


# 接收ViewChange确认
@app.route('/viewChange', methods=["POST"])
def RecvViewChangeMsg():
    msg = request.json
    msg["type"] = "viewChange"
    pbftCore.AddMessage(msg)
    return "ok"


# 接收checkpoint确认
@app.route('/checkPoint', methods=["POST"])
def RecvCheckPointMsg():
    msg = request.json
    msg["type"] = "checkPoint"
    pbftCore.AddMessage(msg)
    return "ok"


# 接收NewView
@app.route('/newView', methods=["POST"])
def RecvNewViewMsg():
    msg = request.json
    msg["type"] = "newView"
    pbftCore.AddMessage(msg)
    return "ok"


# 函数调用路由
@app.route('/funcRouter', methods=["POST"])
def FuncRouter():
    msg = request.json
    func = msg['func']
    if func == 'elect':
        Elect(msg)
    if func == 'stopElect':
        StopElect(msg)
    if func == 'pledge':
        Pledge(msg)
    if func == 'stopPledge':
        StopPledge(msg)
    return "ok"


# 选举提交时间到，调用停止函数
@app.route('/submitElect', methods=["POST"])
def FuncSubmitElect():
    # 发送一个停止信息
    # 消息的作用就是告诉系统，之后的共识不再接受elect请求
    stopElect = {"address": "0x801FD03AfBe1c9FCBaE77bDc03C7812Ad9776d60",
                 "signature": "xxxxxxxx",
                 "timestamp": "5486",
                 "arg": {
                     "func": "stopElect",
                     "loopid": 0,
                     "endpoint": pbftCore.selfEndPoint,
                     "value": 50
                 }, "type": "client"}
    pbftCore.AddMessage(stopElect)


# 质押提交时间到，调用停止函数
@app.route('/submitPledge', methods=["POST"])
def FuncSubmitPledge():
    # 发送一个停止信息
    # 消息的作用就是告诉系统，之后的共识不再接受elect请求
    stopPledge = {"address": "0x801FD03AfBe1c9FCBaE77bDc03C7812Ad9776d60",
                  "signature": "xxxxxxxx",
                  "timestamp": "5486",
                  "arg": {
                      "func": "stopPledge",
                      "loopid": 0,
                      "endpoint": pbftCore.selfEndPoint,
                      "value": 50
                  }, "type": "client"}
    pbftCore.AddMessage(stopPledge)


if __name__ == '__main__':
    app.run()
