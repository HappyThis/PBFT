from flask import request

from app import app, pbftCore


# 接收pre-prepare
@app.route('/prePrepare', methods=["POST"])
def RecvPreprepareMsg():
    msg = request.json
    msg["type"] = "prePrepare"
    pbftCore.AddMessage(msg)
    return "True"


# 接收commit确认
@app.route('/commit', methods=["POST"])
def RecvCommitMsg():
    msg = request.json
    msg["type"] = "commit"
    pbftCore.AddMessage(msg)
    return "True"


# 接收prepare确认
@app.route('/prepare', methods=["POST"])
def RecvPrepareMsg():
    msg = request.json
    msg["type"] = "prepare"
    pbftCore.AddMessage(msg)
    return "True"


# 接收ViewChange确认
@app.route('/viewChange', methods=["POST"])
def RecvViewChangeMsg():
    msg = request.json
    msg["type"] = "viewChange"
    pbftCore.AddMessage(msg)
    return "True"


# 接收checkpoint确认
@app.route('/checkPoint', methods=["POST"])
def RecvCheckPointMsg():
    msg = request.json
    msg["type"] = "checkPoint"
    pbftCore.AddMessage(msg)
    return "True"


# 接收NewView
@app.route('/newView', methods=["POST"])
def RecvNewViewMsg():
    msg = request.json
    msg["type"] = "newView"
    pbftCore.AddMessage(msg)
    return "True"
