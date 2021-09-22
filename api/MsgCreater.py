def ElectCreater(value):
    from app import pbftCore
    elect = {"address": "0x801FD03AfBe1c9FCBaE77bDc03C7812Ad9776d60",
             "signature": "xxxxxxxx",
             "timestamp": "5486",
             "arg": {
                 "func": "stopElect",
                 "loopid": 0,
                 "endpoint": pbftCore.selfEndPoint,
                 "value": value
             }}
    return elect


def StopElectCreater():
    from app import pbftCore
    stopElect = {"address": "0x801FD03AfBe1c9FCBaE77bDc03C7812Ad9776d60",
                 "signature": "xxxxxxxx",
                 "timestamp": "5486",
                 "arg": {
                     "func": "stopElect",
                     "loopid": 0,
                     "endpoint": pbftCore.selfEndPoint,
                     "value": 50
                 }}
    return stopElect


def PledgeCreater(value):
    from app import pbftCore
    pledge = {"address": "0x801FD03AfBe1c9FCBaE77bDc03C7812Ad9776d60",
              "signature": "xxxxxxxx",
              "timestamp": "5486",
              "arg": {
                  "func": "stopElect",
                  "loopid": 0,
                  "endpoint": pbftCore.selfEndPoint,
                  "value": value
              }}
    return pledge


def StopPledgeCreater():
    from app import pbftCore
    stopPledge = {"address": "0x801FD03AfBe1c9FCBaE77bDc03C7812Ad9776d60",
                  "signature": "xxxxxxxx",
                  "timestamp": "5486",
                  "arg": {
                      "func": "stopPledge",
                      "loopid": 0,
                      "endpoint": pbftCore.selfEndPoint,
                      "value": 50
                  }}
    return stopPledge
