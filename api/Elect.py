import requests

from api.Collecter import SendCollecterDecorator


@SendCollecterDecorator
def Elect(value, url, timestamp, addr, endpoint):
    elect = {"address": addr,
             "signature": None,
             "timestamp": timestamp,
             "arg": {
                 "func": "elect",
                 "loopid": 0,
                 "endpoint": endpoint,
                 "value": value
             }}
    return elect


@SendCollecterDecorator
def StopElect(url, timestamp, addr, endpoint):
    stopElect = {"address": addr,
                 "signature": None,
                 "timestamp": timestamp,
                 "arg": {
                     "func": "stopElect",
                     "loopid": 0,
                     "endpoint": endpoint
                 }}
    return stopElect
