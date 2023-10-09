'''dataSimulator.py: Simulates process variation data across 5 parameters'''

# Author: Luke Henderson
__version__ = '1.0'

import numpy as np

import config as cfg

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

