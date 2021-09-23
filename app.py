from flask import Flask, request

from api.Collecter import ReplyCollecter
from consensus.Network import bpftNetwork
from consensus.PbftProcess import PBFT, pbftCore
from functions.Elect import Elect, elect_reject, StopElect
from functions.Pledge import Pledge, pledge_reject, StopPledge
from test.TestRouter import test

app = Flask(__name__)
app.register_blueprint(bpftNetwork, url_prefix="/bpftNetwork")
app.register_blueprint(test, url_prefix="/test")
# 如果是委员会节点那么启动
PBFT.start()


# 函数调用路由
@app.route('/funcRouter', methods=["POST"])
def FuncRouter():
    msg = request.json
    func = msg['arg']['func']
    if func == 'elect':
        Elect(msg)
    if func == 'stopElect':
        StopElect(msg)
    if func == 'pledge':
        Pledge(msg)
    if func == 'stopPledge':
        StopPledge(msg)
    return "ok"


# 请求接收点
@app.route('/recvNodesMessage', methods=["POST"])
def RecvNodesMessage():
    msg = request.json
    if elect_reject and msg["arg"]["func"] == "elect":
        return -1
    if pledge_reject and msg["arg"]["func"] == "pledge":
        return -1
    msg["type"] = "client"
    pbftCore.AddMessage(msg)
    return msg["timestamp"]


# 请求回执接收点
@app.route('/recvCommitteesReply', methods=["POST"])
def RecvCommitteesReply():
    msg = request.json
    ReplyCollecter(msg)
    return "ok"


if __name__ == '__main__':
    app.run()
