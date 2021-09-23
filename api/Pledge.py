from api.Collecter import SendCollecterDecorator


@SendCollecterDecorator
def Pledge(value, url, timestamp, addr, endpoint):
    pledge = {"address": addr,
              "signature": None,
              "timestamp": timestamp,
              "arg": {
                  "func": "pledge",
                  "loopid": 0,
                  "endpoint": endpoint,
                  "value": value
              }}
    return pledge


@SendCollecterDecorator
def StopPledge(url, timestamp, addr, endpoint):
    stopPledge = {"address": addr,
                  "signature": None,
                  "timestamp": timestamp,
                  "arg": {
                      "func": "stopPledge",
                      "loopid": 0,
                      "endpoint": endpoint
                  }}
    return stopPledge
