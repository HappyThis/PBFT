from flask import request, Blueprint

from consensus.PbftProcess import pbftCore

bpftNetwork = Blueprint("bpftNetwork", __name__)


# 接收pre-prepare
@bpftNetwork.route('/prePrepare', methods=["POST"])
def RecvPreprepareMsg():
    msg = request.json
    msg["type"] = "prePrepare"
    pbftCore.AddMessage(msg)
    return "True"


# 接收commit确认
@bpftNetwork.route('/commit', methods=["POST"])
def RecvCommitMsg():
    msg = request.json
    msg["type"] = "commit"
    pbftCore.AddMessage(msg)
    return "True"


# 接收prepare确认
@bpftNetwork.route('/prepare', methods=["POST"])
def RecvPrepareMsg():
    msg = request.json
    msg["type"] = "prepare"
    pbftCore.AddMessage(msg)
    return "True"


# 接收ViewChange确认
@bpftNetwork.route('/viewChange', methods=["POST"])
def RecvViewChangeMsg():
    msg = request.json
    msg["type"] = "viewChange"
    pbftCore.AddMessage(msg)
    return "True"


# 接收checkpoint确认
@bpftNetwork.route('/checkPoint', methods=["POST"])
def RecvCheckPointMsg():
    msg = request.json
    msg["type"] = "checkPoint"
    pbftCore.AddMessage(msg)
    return "True"


# 接收NewView
@bpftNetwork.route('/newView', methods=["POST"])
def RecvNewViewMsg():
    msg = request.json
    msg["type"] = "newView"
    pbftCore.AddMessage(msg)
    return "True"
