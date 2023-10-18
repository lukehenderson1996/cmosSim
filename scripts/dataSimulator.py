'''dataSimulator.py: Simulates process variation data across 5 parameters'''

# Author: Luke Henderson
__version__ = '2.0'

import numpy as np
import pickle

import config as cfg
import debugTools as dt
import colors as cl

def genCornerRon(sigma):
    return \
    {'epox': -0.5*sigma,
     'tox': 0.5*sigma,
     'w': -5*sigma,
     'l': 5*sigma,
     'na': -10*sigma}
    
def genCornerVth(sigma):
    return \
    {'epox': 0.5*sigma,
     'tox': -0.5*sigma,
     'w': 0*sigma,
     'l': 0*sigma,
     'na': -10*sigma}

def genCornerCgate(sigma):
    return \
    {'epox': 0.5*sigma,
     'tox': -0.5*sigma,
     'w': 5*sigma,
     'l': 5*sigma,
     'na': 0*sigma}

def genGaussian(sigma, count=1):
    return np.random.normal(loc=0, scale=sigma, size=count)

def genGaussianSingle(sigma):
    return np.random.normal(loc=0, scale=sigma, size=1)[0]

def genWafer(trCount=1):
    epoxWaferOffset = genGaussianSingle(0.5)
    toxWaferOffset  = genGaussianSingle(0.5)
    geomWaferOffset = genGaussianSingle(5)
    wWaferOffset = geomWaferOffset + genGaussianSingle(0.2)
    lWaferOffset = geomWaferOffset + genGaussianSingle(0.2)
    naWaferOffset  = genGaussianSingle(10)
    ret = []
    for i in range(trCount):
        ret.append({'epox': epoxWaferOffset + genGaussianSingle(0.05),
                    'tox': toxWaferOffset + genGaussianSingle(0.05),
                    'w': wWaferOffset + genGaussianSingle(2),
                    'l': lWaferOffset + genGaussianSingle(2),
                    'na': naWaferOffset + genGaussianSingle(3)})
    return ret

#usage: ds.noVar.copy()
noVar = \
    {'epox': 0,
     'tox': 0,
     'w': 0,
     'l': 0,
     'na': 0}
procVar1s = \
    {'epox': 0.5,
     'tox': 0.5,
     'w': 5,
     'l': 5,
     'na': 10}


class WaferConsumer:
    '''Wafer Consumer class'''

    def __init__(self, path=None):
        '''Wafer Consumer\n
        Args:
            path [str]: path of wafer pickle file
        Notes:
            self.waferIter [list of int]: the iterator for used transistor for each wafer\n
            self.waferNum [int]: wafer currently being used for testing/consuming'''
        with open(path, 'rb') as f:
            self.waferArr = pickle.load(f)
        self.waferIter = [0]*len(self.waferArr)
        self.waferNum = 0

    def consume(self, num):
        '''Consume x number of wafers. \n
        Args:
            num [int]: how many wafers to consume
        Return:
            [list of dict (procVar type)]: subarray of X wafers deterministically given in order'''
        # cl.blue(f'consuming from wafer #{waferNum}, returning {num} trs')
        # cl.yellow(f'this wafers iter is currenly {self.waferIter[waferNum]}')
        ret = []
        for trNum in range(num):
            # try:
            ret.append(self.waferArr[self.waferNum][self.waferIter[self.waferNum]+trNum])
            # except:
            #     dt.info(self.waferNum, 'self.waferNum')
            #     dt.info(trNum, 'trNum')
            #     dt.info(self.waferIter[self.waferNum]+trNum, 'self.waferIter[self.waferNum]+trNum')
            #     exit()
            
        self.waferIter[self.waferNum] += num
        # cl.purple(f'this wafers iter increased   {self.waferIter[waferNum]}')
        return ret
        

class DummyWaferConsumer:
    '''Dummy Wafer Consumer class'''

    def __init__(self):
        '''Dummy Wafer Consumer'''

    def consume(self, num):
        '''Consume x number of wafers. \n
        Args:
            num [int]: how many wafers to consume
        Return:
            None'''
        return None