'''testSupport.py manages test stimulus and interprets results'''

# Author: Luke Henderson
__version__ = '1.2'

import math
import numpy as np

import config as cfg
import colors as cl
import debugTools as dt
import logger as lg
import plot


class TestBench:
    '''Test bench class'''

    def __init__(self, vdd=None, freq=None):
        '''Test bench and analysis tools\n
        Args:
            vdd [float]: Vdd (Volts) upon initialization \n
            freq [float]: Frequency (Hz) upon initialization 
        Notes:
            resArr [List]: list of results to be populated later \n
            stimList [list of bool]: stimulus bools \n
            stimV [list of float]: stimulus voltages (V) \n
            stimScopeV  [list of float]: stimulus voltages to display on oscope later \n
            stimScopet [list of float]: time lengths of stimScopeV data points \n
            resScopeV  [list of float]: result voltages to display on oscope later \n
            resScopet [list of float]: time lengths of resScopeV data points '''
        self.vdd = vdd
        self.freq = freq
        self.period = 1/freq #seconds
        self.ptrnLen = None
        self.stimPtrn = None
        self.stimList = [] #bool
        self.stimV = []
        self.resArr = []
        self.resVoltArr = []
        self.stimScopeV = []
        self.stimScopet = []
        self.resScopet = []
        self.resScopeV = []
        self.resScopeCurr = []
        self.resScopePwr = []
        self.timingFailure = False
        self.avgCurr = None
        self.avgPwr = None

    def setStim(self, ptrn, expRes=None):
        '''Initialize test stimulus and expected result (optional) \n
        Args: 
            ptrn [str]: string of 1s and 0s to test with \n
            expRes [str]: expected result, string of 1s and 0s '''
        if not isinstance(ptrn, str):
            cl.red('Error: Test pattern must be str')
            exit()
        #setup stimulus variables
        self.stimPtrn = ptrn
        self.ptrnLen = len(self.stimPtrn)
        for char in ptrn:
            if char == '0':
                self.stimList.append(False)
            elif char == '1':
                self.stimList.append(True)
            else:
                cl.red(f'Error: Unexpected character "{char}" in ptrn')
                exit()
        for stim in self.stimList:
            self.stimV.append(self.vdd*stim)
        #prepare stimulus oscope data
        for i in range(self.ptrnLen):
            self.stimScopeV.append(self.stimV[i])
            if self.stimScopet:
                self.stimScopet.append(self.stimScopet[-1] + self.period)
            else:
                self.stimScopet.append(0)
        # dt.info(self.stimScopeV, 'self.stimScopeV')
        # dt.info(self.stimScopet, 'self.stimScopet')


        #setup expected result variables
        if expRes:
            if not isinstance(expRes, str):
                cl.red('Error: expRes must be str')
                exit()
            self.expResList = [] #bool
            for char in expRes:
                if char == '0':
                    self.expResList.append(False)
                elif char == '1':
                    self.expResList.append(True)
                else:
                    cl.red(f'Error: Unexpected character "{char}" in expRes')
                    exit()
        
    def prStep(self, i, vout):
        '''Print step\n
        Args:
            i [int]: iterator
            vout [float]: output voltage (V) for step
        Return:
            res [bool]: true/false result based on vdd/2'''
        
        res = vout > self.vdd/2 #bool
        resChar  = str(int(res))
        print(f'Running step #{i}: {self.stimPtrn[i]} → {resChar}')
        self.resArr.append(res)
        self.resVoltArr.append(vout)
        return res
    
    def saveStep(self, i , vout):
        '''save step\n
        Args:
            i [int]: iterator
            vout [float]: output voltage (V) for step
        Return:
            res [bool]: true/false result based on vdd/2'''
        res = vout > self.vdd/2 #bool
        self.resArr.append(res)
        self.resVoltArr.append(vout)
        return res
        
    def checkRes(self):
        passing = True
        if self.timingFailure:
            passing = False
        if self.resArr != self.expResList:
            passing = False

        #average current/power
        timeWeights = []
        for i in range(len(self.resScopet)-1):
            timeWeights.append(self.resScopet[i+1]-self.resScopet[i])
        sumCurr = 0
        sumPwr  = 0
        for i in range(len(timeWeights)):
            sumCurr += timeWeights[i]*self.resScopeCurr[i]
            sumPwr += timeWeights[i]*self.resScopePwr[i]
        self.avgCurr = sumCurr/sum(timeWeights)
        self.avgPwr = sumPwr/sum(timeWeights)

        if passing:
            cl.purple('PASS')
        else:
            cl.red('FAIL')

        return passing

    def prResTable(self):
        cl.yellow('Step #  In (V)    Out (V)   I O') #7, 10, 10 chars
        for i in range(self.ptrnLen):
            print(f'     {i}  {self.stimV[i]:.3f}     {self.resVoltArr[i]:.3f}     {self.stimPtrn[i]} {int(self.resArr[i])}')

    def resScopeData(self, i, output):
        '''Save the step results to an oscope friendly format \n
        Args:
            output [gate.py class]: output object of DUT \n '''
        #assume two steps, ramp voltage, and steady state
        #begin ramp voltage
        startTime = self.stimScopet[i] #begin ramp voltage at t=0 (relative to step)
        self.resScopet.append(startTime)
        self.resScopeV.append(output.initVout)
        self.resScopeCurr.append(output.stepChg/output.stepTime)
        self.resScopePwr.append(output.stepEnergy/output.stepTime)
        #end ramp voltage, begin steady state
        self.resScopet.append(startTime+output.stepTime)
        self.resScopeV.append(output.voutFinal)
        self.resScopeCurr.append(output.ssCurr)
        self.resScopePwr.append(output.ssPwr)
        #end steady state will tack onto the next one automatically 

        # dt.info(self.resScopet, 'self.resScopet')
        # dt.info(self.resScopeV, 'self.resScopeV')

    def dispScope(self):
        scope = plot.OSCOPE()
        scope.dataList.append({'v': self.stimScopeV, 't': self.stimScopet, 'intp': False})
        scope.dataList.append({'v': self.resScopeV, 't': self.resScopet, 'intp': True})
        scope.dataList.append({'v': self.resScopeCurr, 't': self.resScopet, 'intp': False})
        scope.dataList.append({'v': self.resScopePwr, 't': self.resScopet, 'intp': False})
        scope.plot(multiLabels=['Vin (V)', 'Vout (V)', 'Current (A)', 'Power (W)'], 
                   title='Oscope', xlabel='Time (s)', ylabel='Voltage (V)', trellis=True)
        

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

    def step(self, i, quiet=True):
        self.input.vin = self.tb.stimV[i]
        self.dut.step()

        if self.dut.stepTime >= self.tb.period:
            self.tb.timingFailure = True

        if quiet:
            self.tb.saveStep(i, self.output.voutFinal)
        else:
            self.tb.prStep(i, self.output.voutFinal)
        self.tb.resScopeData(i, self.output)
        

    