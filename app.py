from flask import Flask, request

from api.Collecter import ReplyCollecter
from consensus.PbftProcess import PBFT, pbftCore
from functions.Elect import Elect, elect_reject, StopElect
from functions.Pledge import Pledge, pledge_reject, StopPledge

PBFT.start()

app = Flask(__name__)


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
    return True


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
    return True


if __name__ == '__main__':
    app.run()
