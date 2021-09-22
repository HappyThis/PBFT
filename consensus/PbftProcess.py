from multiprocessing.dummy import Process

from consensus.PbftCore import PbftCore

pbftCore = PbftCore()


def PBFTCoreProcess():
    global pbftCore
    pbftCore.RunPbft()


PBFT = Process(target=PBFTCoreProcess)
