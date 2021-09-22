# 实用拜占庭算法核心
from multiprocessing import get_context
from multiprocessing.queues import Queue
from queue import PriorityQueue

from consensus.CheckPointMessage import CheckPointMessage
from consensus.CommitMessage import CommitMessage
from consensus.Deserialization import ToClientMsg, ToPrepare, ToPrePrepare, ToCommit, ToCheckPoint
from consensus.PrePrepareMessage import PrePrepareMessage
from consensus.PrepareMessage import PrepareMessage


class PbftCore:
    def __init__(self):
        # 请求消息队列
        self.queue = Queue(ctx=get_context())
        # nonce
        self.nonce = 0
        # 委员会
        self.committees = ["0xaaaaaaaaaa"]
        self.endpoints = ["http://127.0.0.1:5000/"]
        self.f = (len(self.committees) - 1) / 3
        # view
        self.view = 0
        # 水线
        self.L = 200
        self.h = 0
        self.H = 0 + self.L
        self.currentExe = 0
        self.addr = "0xaaaaaaaaaa"
        self.selfEndPoint = self.endpoints[self.committees.index(self.addr)]
        self.checkPointLoop = 50
        # 消息存储列表
        self.P = []
        self.Q = []
        # 等待执行的请求队列
        self.waitexe = PriorityQueue()
        # 请求存储点
        self.clientMsgStatus = {}
        # 回收存储点
        self.checkPointMsgStatus = {}
        # 视图更改存储点
        self.viewChangeMsgStatus = {}
        # 原始消息存储点
        self.clientReq = {}

    def IsPrimary(self):
        return self.addr == self.committees[self.view % len(self.committees)]

    def RunPbft(self):
        while True:
            msg = self.queue.get()
            if msg["type"] == "client":
                self.ClientHandler(msg)
            if msg["type"] == "prePrepare":
                self.PrePrepareHandler(msg)
            if msg["type"] == "prepare":
                self.PrepareHandler(msg)
            if msg["type"] == "commit":
                self.CommitHandler(msg)
            if msg["type"] == "viewChange":
                self.ViewChangeHandler(msg)
            if msg["type"] == "checkPoint":
                self.CheckPointHandler(msg)
            if msg["type"] == "newView":
                self.NewViewHandler(msg)

    def ClientHandler(self, jsonClientMessage):

        clientMessage = ToClientMsg(jsonClientMessage)

        # 如果检查没有通过那么什么也不做
        if clientMessage.Check() is not True:
            print("check break down")
            return False

        # 分配结束之后构造pre-prepare消息
        prePrepare = PrePrepareMessage(view=self.view,
                                       nonce=self.nonce,
                                       digest=clientMessage.Digest(),
                                       signature=None,
                                       addr=self.addr,
                                       clientMessage=jsonClientMessage)
        prePrepare.signature = prePrepare.GetSignature()
        # 向全体委员会广播
        prePrepare.Broadcast(self.endpoints)
        # nonce自增
        self.nonce += 1
        return True

    def PrePrepareHandler(self, jsonPrePrepareMessage):

        prePrepare = ToPrePrepare(jsonPrePrepareMessage)
        # 从消息收到，计时器随即启动

        # 数学检查
        if prePrepare.Check() is not True:
            print("check break down")
            return False
        # PBFT规则检查

        self.clientReq[(prePrepare.nonce, prePrepare.view)] = prePrepare

        # 检查通过后即向全网广播prepare信息
        # 首先构造一个prepare
        prepare = PrepareMessage(
            view=prePrepare.view,
            nonce=prePrepare.nonce,
            digest=prePrepare.digest,
            signature=None,
            addr=prePrepare.addr
        )
        prepare.signature = prepare.GetSignature()
        # 广播
        prepare.Broadcast(self.endpoints)
        # 消息存档后结束处理流程
        self.Q.append(prePrepare)

        return True

    def PrepareHandler(self, jsonPrepareMessage):
        prepare = ToPrepare(jsonPrepareMessage)
        # 数学检查
        if prepare.Check() is not True:
            print("check break down")
            return False
        # PBFT规则检查...

        if (prepare.nonce, prepare.view, "prepared") not in self.clientMsgStatus.keys():
            self.clientMsgStatus[(prepare.nonce, prepare.view, "prepared")] = {}

        preparedDict = self.clientMsgStatus[(prepare.nonce, prepare.view, "prepared")]

        preparedDict[prepare.addr] = prepare

        if len(preparedDict) < self.f * 2 + 1:
            return True

        # 存档

        self.P.append(prepare)

        # 生成commit消息

        commitMessage = CommitMessage(view=prepare.view,
                                      nonce=prepare.nonce,
                                      digest=prepare.digest,
                                      signature=None,
                                      addr=self.addr)
        commitMessage.signature = commitMessage.GetSignature()

        commitMessage.Broadcast(self.endpoints)

        return True

    def CommitHandler(self, jsonCommitMessage):

        commitMessage = ToCommit(jsonCommitMessage)
        # 数学检查
        if commitMessage.Check() is not True:
            print("check break down")
            return False
        # PBFT规则检查...

        if (commitMessage.nonce, commitMessage.view, "committed") not in self.clientMsgStatus.keys():
            self.clientMsgStatus[(commitMessage.nonce, commitMessage.view, "committed")] = {}

        committedDict = self.clientMsgStatus[(commitMessage.nonce, commitMessage.view, "committed")]

        committedDict[commitMessage.addr] = commitMessage

        if len(committedDict) < self.f * 2 + 1:
            return True

        # 进入执行队列

        clientMsg = self.clientReq[(commitMessage.nonce, commitMessage.view)]

        self.waitexe.put((clientMsg.nonce, clientMsg.view, clientMsg))

        maybeExec = self.waitexe.get()

        if self.currentExe == maybeExec[0]:
            maybeExec[2].Exec(self.selfEndPoint, self.addr)
            self.currentExe += 1
        else:
            print("except nonce is ", self.currentExe, " but min nonce is ", maybeExec[0])

        # 是否应该发起CheckPoint

        if self.currentExe % self.checkPointLoop == 0:
            print("发起checkPoint")
            checkPointMessage = CheckPointMessage(nonce=self.currentExe - 1,
                                                  view=self.view,
                                                  h=self.h,
                                                  signature=None,
                                                  addr=self.addr)
            checkPointMessage.signature = checkPointMessage.GetSignature()
            checkPointMessage.Broadcast(self.endpoints)

        return True

    def CheckPointHandler(self, jsonCheckPointMessage):
        checkPointMessage = ToCheckPoint(jsonCheckPointMessage)
        # 数学检查
        if checkPointMessage.Check() is not True:
            print("check break down")
            return False
        # PBFT规则检查...

        if (checkPointMessage.nonce, checkPointMessage.view) not in self.checkPointMsgStatus.keys():
            self.checkPointMsgStatus[(checkPointMessage.nonce, checkPointMessage.view)] = {}

        checkPointDict = self.checkPointMsgStatus[(checkPointMessage.nonce, checkPointMessage.view)]

        checkPointDict[checkPointMessage.addr] = checkPointMessage

        if len(checkPointDict) < self.f * 2 + 1:
            return True

        # 当接收了2f+1个检查点

        # 1.提高水线h 2.清除系统内所有在水线h之前的所有数据

        self.h = max(checkPointMessage.nonce, self.h)
        self.H = self.h + self.L
        print("h=", self.h)
        self.currentExe = max(self.currentExe, self.h)

        self.ClearDataBeforeWaterLine()

        return True

    def NewViewHandler(self, msg):
        return True

    def ViewChangeHandler(self, msg):
        return True

    def AddMessage(self, clientJson):
        self.queue.put(clientJson)

    def ClearDataBeforeWaterLine(self):
        # PQ队列
        self.P = [msg for msg in self.P if msg.nonce >= self.h and msg.view == self.view]
        self.Q = [msg for msg in self.Q if msg.nonce >= self.h and msg.view == self.view]
        # 没有执行的请求不再执行
        while not self.waitexe.empty():
            msg = self.waitexe.get()
            if msg.nonce >= self.currentExe and msg.view == self.view:
                break
        # 原始请求
        for key in list(self.clientReq.keys()):
            if key[0] < self.h and key[1] == self.view:
                del self.clientReq[key]
        # 请求存储点
        for key in list(self.clientMsgStatus.keys()):
            if key[0] < self.h and key[1] == self.view:
                del self.clientMsgStatus[key]
        # 回收存储点
        for key in list(self.checkPointMsgStatus.keys()):
            if key[0] < self.h and key[1] == self.view:
                del self.checkPointMsgStatus[key]
        # 视图更改存储点

        return True

    def SendViewChange(self):
        return True
