from api.Collecter import SendCollecterDecorator


@SendCollecterDecorator
def Pledge(value, url, timestamp, addr, endpoint):
    pledge = {"address": addr,
              "signature": None,
              "timestamp": timestamp,
              "arg": {
                  "func": "pledge",
                  "endpoint": endpoint,
                  "value": value
              }}
    # 签名
    return pledge


@SendCollecterDecorator
def StopPledge(url, timestamp, addr, endpoint):
    stopPledge = {"address": addr,
                  "signature": None,
                  "timestamp": timestamp,
                  "arg": {
                      "func": "stopPledge",
                      "endpoint": endpoint
                  }}
    # 签名
    return stopPledge
