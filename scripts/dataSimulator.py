'''dataSimulator.py: Simulates process variation data across 5 parameters'''

# Author: Luke Henderson
__version__ = '0.2'

import config as cfg

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

def genCornerRon(sigma):
    return \
    {'epox': -0.5*sigma,
     'tox': 0.5*sigma,
     'w': -5*sigma,
     'l': 5*sigma,
     'na': -10*sigma}
    
def genCornerVth(sigma):
    pass

def getCornerCgate(sigma):
    pass
