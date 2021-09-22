import json

from CheckPointMessage import CheckPointMessage
from ClientMessage import ClientMessage
from CommitMessage import CommitMessage
from PrePrepareMessage import PrePrepareMessage
from PrepareMessage import PrepareMessage


def ToClientMsg(msg):
    # 组装消息
    address = msg['address']
    signature = msg['signature']
    timestamp = msg['timestamp']
    arg = msg["arg"]
    clientMessage = ClientMessage(signature=signature,
                                  clinetAddr=address,
                                  timestamp=timestamp,
                                  arg=arg)
    return clientMessage


def ToPrePrepare(msg):
    # 组装消息
    view = msg["view"]
    nonce = msg["nonce"]
    digest = msg["digest"]
    signature = msg["signature"]
    addr = msg["addr"]
    clientMessage = ToClientMsg(msg['client_message'])
    prePrepare = PrePrepareMessage(view=view,
                                   nonce=nonce,
                                   digest=digest,
                                   signature=signature,
                                   addr=addr,
                                   clientMessage=clientMessage)
    return prePrepare


def ToPrepare(msg):
    # 组装消息
    view = msg["view"]
    nonce = msg["nonce"]
    digest = msg["digest"]
    signature = msg["signature"]
    addr = msg["addr"]
    prepare = PrepareMessage(
        view=view,
        nonce=nonce,
        digest=digest,
        signature=signature,
        addr=addr
    )
    return prepare


def ToCommit(msg):
    view = msg["view"]
    nonce = msg["nonce"]
    digest = msg["digest"]
    signature = msg["signature"]
    addr = msg["addr"]
    commitMessage = CommitMessage(view=view,
                                  nonce=nonce,
                                  digest=digest,
                                  signature=signature,
                                  addr=addr)
    return commitMessage


def ToCheckPoint(msg):
    nonce = msg["nonce"]
    h = msg["h"]
    signature = msg["signature"]
    addr = msg["addr"]
    view = msg["view"]
    checkPointMessage = CheckPointMessage(nonce=nonce,
                                          h=h,
                                          view=view,
                                          signature=signature,
                                          addr=addr)
    return checkPointMessage


def ToViewChange(msg):
    return True


def ToNewView(msg):
    return True
