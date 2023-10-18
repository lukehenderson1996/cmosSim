'''testSupport.py manages test stimulus and interprets results'''

# Author: Luke Henderson
__version__ = '1.3'

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
            resArr [List of bool]: list of results to be populated later \n
                [dict of list of float] for multi mode, str keys
            stimList [list of bool]: stimulus bools \n
            stimList [dict of list of bool]: stimulus bools for Multi DUTs
                str keys
            stimV [list of float]: stimulus voltages (V) \n
            stimV [dict of list of float]: stimulus voltages (V) for Multi DUTs
                str keys
            stimScopeV  [list of float]: stimulus voltages to display on oscope later
                [dict of list of float] for multi mode, str keys
            stimScopet [list of float]: time lengths of stimScopeV data points \n
            resScopeV  [list of float]: result voltages to display on oscope later
                [dict of list of float] for multi mode, str keys
            resScopet [list of float]: time lengths of resScopeV data points \n
            propTimeList [list of float]: list of propagation delays for every transistion in test pattern'''
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
        self.propTimeList = []

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

    def setMultiStim(self, ptrn, expRes=None):
        '''Initialize test stimulus and expected result (optional) \n
        Args: 
            ptrn [dict of str]: string of 1s and 0s to test with \n
                str keys
            expRes [dict str]: expected result, string of 1s and 0s 
                str keys '''
        if not isinstance(ptrn, dict):
            cl.red('Error: Test pattern must be dict')
            exit()
        #setup stimulus variables
        self.stimList = {}
        self.stimV = {}
        self.stimPtrn = ptrn
        ptrnKeys = list(self.stimPtrn.keys())
        self.ptrnLen = len(self.stimPtrn[ptrnKeys[0]])
        for key in ptrnKeys:
            self.stimList[key] = []
            for char in self.stimPtrn[key]:
                if char == '0':
                    self.stimList[key].append(False)
                elif char == '1':
                    self.stimList[key].append(True)
                else:
                    cl.red(f'Error: Unexpected character "{char}" in ptrn')
                    exit()
            # dt.info(self.stimList, 'self.stimList')
            # dt.info(key, 'key')
        for key in ptrnKeys:
            self.stimV[key] = []
            for stim in self.stimList[key]:
                self.stimV[key].append(self.vdd*stim)
        # dt.info(self.stimV, 'self.stimV')
        #prepare stimulus oscope data
        for i in range(self.ptrnLen):
            if self.stimScopet:
                self.stimScopet.append(self.stimScopet[-1] + self.period)
            else:
                self.stimScopet.append(0)
        self.stimScopeV = {}
        for key in ptrnKeys:
            self.stimScopeV[key] = []
            for i in range(self.ptrnLen):
                self.stimScopeV[key].append(self.stimV[key][i])  
        # dt.info(self.stimScopeV, 'self.stimScopeV')
        # dt.info(self.stimScopet, 'self.stimScopet')
        # exit()

        #setup expected result variables
        if expRes:
            if not isinstance(expRes, dict):
                cl.red('Error: expRes must be dict')
                exit()
            expKeys = list(expRes.keys())
            self.expResList = {} #dict of list of bool
            for key in expKeys:
                self.expResList[key] = []
                for char in expRes[key]:
                    if char == '0':
                        self.expResList[key].append(False)
                    elif char == '1':
                        self.expResList[key].append(True)
                    else:
                        cl.red(f'Error: Unexpected character "{char}" in expRes')
                        exit()
        # dt.info(self.expResList, 'self.expResList')
        
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
        '''Save step\n
        Args:
            i [int]: iterator
            vout [float]: output voltage (V) for step
        Return:
            res [bool]: true/false result based on vdd/2'''
        res = vout > self.vdd/2 #bool
        self.resArr.append(res)
        self.resVoltArr.append(vout)
        return res
    
    def prStepMulti(self, i, vout):
        '''MULTI print step\n
        Args:
            i [int]: iterator
            vout [dict of float]: output voltages (V) for step
        Return:
            res [dict of bool]: true/false results based on vdd/2'''
        
        
        
        
        voutKeys = list(vout.keys())
        res = {}
        for key in voutKeys:
            res[key] = vout[key] > self.vdd/2 #bool
            if not key in self.resArr:
                self.resArr[key] = []
            self.resArr[key].append(res[key])
            if not key in self.resVoltArr:
                self.resVoltArr[key] = []
            self.resVoltArr[key].append(vout[key])
        # dt.info(self.resArr, 'self.resArr')
        # dt.info(self.resVoltArr, 'self.resVoltArr')

        resStr = ''
        for key in reversed(voutKeys):
            resChar  = str(int(res[key]))
            # resStr += f'{key}: {resChar}   '
            resStr += f'{resChar} '
        print(f'Running step #{i:2}: {self.stimPtrn["a"][i]} + {self.stimPtrn["b"][i]} + {self.stimPtrn["cin"][i]}     →     {resStr}')
        
        return res
    
    
    def saveStepMulti(self, i , vout):
        '''MULTI save step\n
        Args:
            i [int]: iterator
            vout [dict of float]: output voltages (V) for step
        Return:
            res [dict of bool]: true/false results based on vdd/2'''
        voutKeys = list(vout.keys())
        res = {}
        for key in voutKeys:
            res[key] = vout[key] > self.vdd/2 #bool
            if not key in self.resArr:
                self.resArr[key] = []
            self.resArr[key].append(res[key])
            if not key in self.resVoltArr:
                self.resVoltArr[key] = []
            self.resVoltArr[key].append(vout[key])
        # dt.info(self.resArr, 'self.resArr')
        # dt.info(self.resVoltArr, 'self.resVoltArr')
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
        #print run details
        # print(f'Average current consumption: {round(self.avgCurr*1000, 9)} mA')
        # print(f'Average power   consumption: {round(self.avgPwr*1000, 9)} mW')

        #print run details
        # if passing:
        #     cl.purple('\nPASS')
        # else:
        #     cl.red('\nFAIL')

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

    def resScopeDataMulti(self, i, dut, propTime):
        '''MULTI (only for full adder right now) - Save the step results to an oscope friendly format \n
        Args:
            output [gate.py class]: output object of DUT \n '''
        xor1 = dut[0]
        nand2 = dut[1]
        xor2 = dut[2]
        nand1 = dut[3]
        invNand1 = dut[4]
        invNand2 = dut[5]
        nor = dut[6]
        invNor = dut[7]
        
        #assume two steps, ramp voltage, and steady state
        #begin ramp voltage
        startTime = self.stimScopet[i] #begin ramp voltage at t=0 (relative to step)
        self.resScopet.append(startTime)
        if not isinstance(self.resScopeV, dict):
            self.resScopeV = {'s':[], 'cout':[]}
        self.resScopeV['s'].append(xor2.initVout)
        self.resScopeV['cout'].append(invNor.initVout)
        self.resScopeCurr.append((xor1.stepChg+nand2.stepChg+xor2.stepChg+nand1.stepChg+invNand1.stepChg+invNand2.stepChg+nor.stepChg+invNor.stepChg)/propTime)
        self.resScopePwr.append((xor1.stepEnergy+nand2.stepEnergy+xor2.stepEnergy+nand1.stepEnergy+invNand1.stepEnergy+invNand2.stepEnergy+nor.stepEnergy+invNor.stepEnergy)/propTime)
        #end ramp voltage, begin steady state
        self.resScopet.append(startTime+propTime)
        self.resScopeV['s'].append(xor2.voutFinal)
        self.resScopeV['cout'].append(invNor.voutFinal)
        self.resScopeCurr.append(xor1.ssCurr+nand2.ssCurr+xor2.ssCurr+nand1.ssCurr+invNand1.ssCurr+invNand2.ssCurr+nor.ssCurr+invNor.ssCurr)
        self.resScopePwr.append(xor1.ssPwr+nand2.ssPwr+xor2.ssPwr+nand1.ssPwr+invNand1.ssPwr+invNand2.ssPwr+nor.ssPwr+invNor.ssPwr)
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
        

class MultiDutManager:
    '''Multi DUT manager class'''

    def __init__(self, tb=None, dut=None):
        '''*ONLY WORKS FOR FULL ADDER FOR NOW*\n
        Dut manager steps entire devices\n
        Args:
            tb [TestBench class]: test bench object \n
            dut [list of INV, NAND, NOR or XOR (from gate.py) class]: 
        Notes:
            input [dict of gate.py class]: input gate
                str keys
            output [dict of gate.py class]: output gate
                str keys'''
        self.tb = tb
        self.dut = dut
        self.input = None
        self.output = None
        self.tb.resArr = {}
        self.tb.resVoltArr = {}

    def step(self, i, quiet=True):
        assert isinstance(self.dut, list) and len(self.dut)==8 #only works for a full adder for now
        
        xor1 = self.dut[0]
        nand2 = self.dut[1]
        xor2 = self.dut[2]
        nand1 = self.dut[3]
        invNand1 = self.dut[4]
        invNand2 = self.dut[5]
        nor = self.dut[6]
        invNor = self.dut[7]
        
        xor1.chgInputs(self.tb.stimV['a'][i], self.tb.stimV['b'][i])
        nand2.vinA = self.tb.stimV['a'][i]
        nand2.vinB = self.tb.stimV['b'][i]
        xor1.step()
        nand2.step()

        xor2.chgInputs(xor1.voutFinal, self.tb.stimV['cin'][i])
        nand1.vinA = self.tb.stimV['cin'][i]
        nand1.vinB = xor1.voutFinal
        xor2.step()
        nand1.step()

        invNand1.vin = nand1.voutFinal
        invNand2.vin = nand2.voutFinal
        invNand1.step()
        invNand2.step()

        nor.vinA = invNand1.voutFinal
        nor.vinB = invNand2.voutFinal
        nor.step()
        invNor.vin = nor.voutFinal
        invNor.step()

        sumPropTime1 = xor1.stepTime + xor2.stepTime
        sumPropTime2 = xor1.stepTime + nand1.stepTime + invNand1.stepTime + nor.stepTime + invNor.stepTime
        sumPropTime3 = nand2.stepTime + invNand2.stepTime + nor.stepTime + invNor.stepTime
        maxSumPropTime = max(sumPropTime1, sumPropTime2, sumPropTime3)
        self.tb.propTimeList.append(maxSumPropTime)
        if maxSumPropTime >= self.tb.period:
            self.tb.timingFailure = True

        if quiet:
            self.tb.saveStepMulti(i, {'s':xor2.voutFinal, 'cout':invNor.voutFinal})
        else:
            self.tb.prStepMulti(i, {'s':xor2.voutFinal, 'cout':invNor.voutFinal})
        
        self.tb.resScopeDataMulti(i, self.dut, maxSumPropTime)