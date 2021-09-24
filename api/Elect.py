import requests

from api.Collecter import SendCollecterDecorator


@SendCollecterDecorator
def Elect(value, url, timestamp, addr, endpoint):
    elect = {"address": addr,
             "signature": None,
             "timestamp": timestamp,
             "arg": {
                 "func": "elect",
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
                     "endpoint": endpoint
                 }}
    return stopElect
