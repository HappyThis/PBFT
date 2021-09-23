from flask import Blueprint

from api.Elect import Elect, StopElect
from api.Pledge import Pledge, StopPledge

test = Blueprint("test", __name__)


@test.route('/elect', methods=["GET"])
def TestElect():
    ret = Elect(value=100, url="http://127.0.0.1:5000/recvNodesMessage")
    return ret.text


@test.route('/stopElect', methods=["POST"])
def TestStopElect():
    ret = StopElect(url="http://127.0.0.1:5000/recvNodesMessage")
    return ret.text


@test.route('/pledge', methods=["GET"])
def TestPledge():
    ret = Pledge(value=100, url="http://127.0.0.1:5000/recvNodesMessage")
    return ret.text


@test.route('/stopPledge', methods=["GET"])
def TestStopPledge():
    ret = StopPledge(url="http://127.0.0.1:5000/recvNodesMessage")
    return ret.text
