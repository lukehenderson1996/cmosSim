'''testSupport.py manages test stimulus and interprets results'''

# Author: Luke Henderson
__version__ = '1.0'

import math
import numpy as np

import config as cfg
import colors as cl
import debugTools as dt
import logger as lg


class TestBench:
    '''Test bench class'''

    def __init__(self, vdd=None, freq=None):
        '''Test bench and analysis tools\n
        Args:
            vdd [float]: Vdd (Volts) upon initialization\n
            freq [float]: Frequency (Hz) upon initialization '''
        self.vdd = vdd
        self.freq = freq
        self.period = 1/freq #seconds
        self.stimPtrn = None
        self.stimPtrnBool = None

    def setStim(self, ptrn):
        '''Initialize test stimulus\n
        Args: 
            ptrn [str]: string of 1s and 0s to test with
        Notes:
            stimList [list of bool]: stimulus bools
            stimV [list of float]: stimulus voltages (V)'''
        if not isinstance(ptrn, str):
            cl.red('Error: Test pattern must be str')
            exit()
        self.stimList = [] #bool
        for char in ptrn:
            if char == '0':
                self.stimList.append(False)
            elif char == '1':
                self.stimList.append(True)
            else:
                cl.red(f'Error: Unexpected character "{char}" in ptrn')
                exit()
        
        self.stimV = []
        for stim in self.stimList:
            self.stimV.append(self.vdd*stim)

    def prStep(self, i, vout):
        '''Print step\n
        Args:
            i [int]: iterator
            vout [float]: output voltage (V) for step'''
        
        stim = str(int(self.stimList[i]))
        res  = str(int(vout > self.vdd/2))
        print(f'{stim} → {res}')
        return res

class DutManager:
    '''DUT manager class'''

    def __init__(self, tb=None, dut=None):
        '''Dut manager steps gate objects\n
        Args:
            tb [TestBench class]: test bench object \n
            dut [INV, NAND, NOR or XOR (from gate.py) class]: 
        Notes:
            input [gate.py class]: input gate
            output [gate.py class]: output gate'''
        self.tb = tb
        self.dut = dut
        self.input = None
        self.output = None

    def step(self, i):
        self.input.vin = self.tb.stimV[i]
        self.dut.step()

    