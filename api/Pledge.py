import requests

from api.Collecter import SendCollecterDecorator
from api.MsgCreater import PledgeCreater, StopPledgeCreater


@SendCollecterDecorator
def Pledge(value, url):
    msg = PledgeCreater(value)
    ret = requests.post(url, json=msg)
    return ret.text, msg


@SendCollecterDecorator
def StopPledge(url):
    msg = StopPledgeCreater()
    ret = requests.post(url, json=msg)
    return ret.text, msg
