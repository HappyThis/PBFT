import requests

from api.Collecter import SendCollecterDecorator
from api.MsgCreater import ElectCreater, StopElectCreater


@SendCollecterDecorator
def Elect(value, url):
    msg = ElectCreater(value)
    ret = requests.post(url, json=msg)
    return ret.text, msg


@SendCollecterDecorator
def StopElect(url):
    msg = StopElectCreater()
    ret = requests.post(url, json=msg)
    return ret.text, msg
