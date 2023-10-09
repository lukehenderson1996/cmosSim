'''gate.py generates logic gates'''

# Author: Luke Henderson
__version__ = '1.0'

import math

import colors as cl
import debugTools as dt
import dataSimulator as ds
import transistor as tr

TAUS_PER_OPERATION = 5
noVar = ds.noVar.copy()

class INV:
    '''INV class'''

    def __init__(self, vdd, vin=0, vout=0, procVarArr=None):
        '''Inverter gate\n
        Args:
            procVarArr [List of procVar dicts]: given in order [nmos, pmos]\n
            vdd [float]: Vdd upon initialization\n
            vin [float]: Vin upon initialization\n
            Vout [float]: Vout upon initialization'''
        #simulation variables, to be loaded in during mapping
        self.vin = vin #voltage at gate [float]
        self.cld = None #load capacitance [F] (gate capacitance of next transistor(s))
        self.vout = vout #output voltage [V]
        self.vdd = vdd #rail voltage [V]
        #simulation calcuated variables
        self.ssVfinal = None #steady state final output voltage (theoretical, not reached)
        self.ssCurr = None #steady-state current
        self.ssPwr = None #steady-state power
        self.voutFinal = None #actual final output voltage
        self.tau = None #timing constant
        self.stepTime = None #time [s] to complete last operation
        self.stepChg = None #charge [A-s, or coulombs] transferred during last operation
        self.stepEnergy = None #energy [W-s, or joules] consumed during last operation
        #generate transistors
        if procVarArr:
            self.nTr = tr.FET('n', procVarArr[0])
            self.pTr = tr.FET('p', procVarArr[1])
        else:
            self.nTr = tr.FET('n', noVar)
            self.pTr = tr.FET('p', noVar)
        self.cin = self.nTr.cgate + self.pTr.cgate
        #map transistors
        #nTr
        self.nTr.inGate = True
        self.nTr.validateModel()
        #pTr
        self.pTr.inGate = True
        self.pTr.vrail = self.vdd
        self.pTr.validateModel()

    def validateModel(self):
        '''Validates whether model is set up correctly'''
        #simulation variables
        assert self.vin>=0
        assert self.cld>=0
        assert self.vout>=0
        assert self.vdd>0

    def step(self):
        '''Step the model forward one time chunk'''
        self.validateModel()
        #calculate steady state parameters
        nRds = self.nTr.rds(self.vin)
        pRds = self.pTr.rds(self.vin)
        sumRds = nRds + pRds
        self.ssCurr = self.vdd/sumRds #steady-state current
        self.ssPwr = self.vdd**2/sumRds #steady-state power
        self.ssVfinal = self.vdd*(nRds/sumRds) #steady state final output voltage (theoretical, not reached)
        #calculate transient parameters
        self.tau = self.cld*min(nRds, pRds)
        self.stepTime = self.tau*TAUS_PER_OPERATION
        deltaVpercentage = 1-math.exp(-TAUS_PER_OPERATION)
        deltaV = (self.ssVfinal-self.vout) * deltaVpercentage 
        self.voutFinal = self.vout + deltaV #actual final output voltage
        self.stepChg = self.cld * deltaV
        self.stepEnergy = (1/2)*self.cld*(deltaV**2)
        # print(f'pRds is {pRds}')
        # print(f'nRds is {nRds}')
        # print(f'sumRds is {sumRds}')
        # print(f'self.ssCurr is {self.ssCurr}')
        # print(f'self.ssPwr is {self.ssPwr}')
        # print(f'self.stepChg is {self.stepChg}')
        # print(f'self.stepEnergy is {self.stepEnergy}')
        
        #prepare for next step
        self.vout = self.voutFinal
        
class NAND:
    '''NAND class'''

    def __init__(self, vdd, vinA=0, vinB=0, vout=0, procVarArr=None):
        '''NAND gate \n
        Args:
            procVarArr [List of procVar dicts]: given in order [nmos A, nmos B, pmos A, pmos B]\n
            vdd [float]: Vdd upon initialization\n
            vinA [float]: Vin A upon initialization\n
            vinB [float]: Vin B upon initialization\n
            Vout [float]: Vout upon initialization'''
        #simulation variables, to be loaded in during mapping
        self.vinA = vinA #voltage A at gate [float]
        self.vinB = vinB #voltage B at gate [float]
        self.cld = None #load capacitance [F] (gate capacitance of next transistor(s))
        self.vout = vout #output voltage [V]
        self.vdd = vdd #rail voltage [V]
        #simulation calcuated variables
        self.ssVfinal = None #steady state final output voltage (theoretical, not reached)
        self.ssCurr = None #steady-state current
        self.ssPwr = None #steady-state power
        self.voutFinal = None #actual final output voltage
        self.tau = None #timing constant
        self.stepTime = None #time [s] to complete last operation
        self.stepChg = None #charge [A-s, or coulombs] transferred during last operation
        self.stepEnergy = None #energy [W-s, or joules] consumed during last operation
        #generate transistors
        if procVarArr:
            self.nTrA = tr.FET('n', procVarArr[0])
            self.nTrB = tr.FET('n', procVarArr[1])
            self.pTrA = tr.FET('p', procVarArr[2])
            self.pTrB = tr.FET('p', procVarArr[3])
        else:
            self.nTrA = tr.FET('n', noVar)
            self.nTrB = tr.FET('n', noVar)
            self.pTrA = tr.FET('p', noVar)
            self.pTrB = tr.FET('p', noVar)
        self.cinA = self.nTrA.cgate + self.pTrA.cgate
        self.cinB = self.nTrB.cgate + self.pTrB.cgate
        #map transistors
        #nTr
        self.nTrA.inGate = True
        self.nTrA.validateModel()
        self.nTrB.inGate = True
        self.nTrB.validateModel()
        #pTr
        self.pTrA.inGate = True
        self.pTrA.vrail = self.vdd
        self.pTrA.validateModel()
        self.pTrB.inGate = True
        self.pTrB.vrail = self.vdd
        self.pTrB.validateModel()

    def validateModel(self):
        '''Validates whether model is set up correctly'''
        #simulation variables
        assert self.vinA>=0
        assert self.vinB>=0
        assert self.cld>=0
        assert self.vout>=0
        assert self.vdd>0

    def step(self):
        '''Step the model forward one time chunk'''
        self.validateModel()
        #calculate steady state parameters
        nRdsA = self.nTrA.rds(self.vinA)
        nRdsB = self.nTrB.rds(self.vinB)
        pRdsA = self.pTrA.rds(self.vinA)
        pRdsB = self.pTrB.rds(self.vinB)
        nRds = nRdsA + nRdsB
        pRds = pRdsA*pRdsB/(pRdsA+pRdsB)
        sumRds = nRds + pRds
        self.ssCurr = self.vdd/sumRds #steady-state current
        self.ssPwr = self.vdd**2/sumRds #steady-state power
        self.ssVfinal = self.vdd*(nRds/sumRds) #steady state final output voltage (theoretical, not reached)
        #calculate transient parameters
        self.tau = self.cld*min(nRds, pRds)
        self.stepTime = self.tau*TAUS_PER_OPERATION
        deltaVpercentage = 1-math.exp(-TAUS_PER_OPERATION)
        deltaV = (self.ssVfinal-self.vout) * deltaVpercentage 
        self.voutFinal = self.vout + deltaV #actual final output voltage
        self.stepChg = self.cld * deltaV
        self.stepEnergy = (1/2)*self.cld*(deltaV**2)
        # print(f'pRds is {pRds}')
        # print(f'nRds is {nRds}')
        # print(f'sumRds is {sumRds}')
        # print(f'self.ssCurr is {self.ssCurr}')
        # print(f'self.ssPwr is {self.ssPwr}')
        # print(f'self.stepChg is {self.stepChg}')
        # print(f'self.stepEnergy is {self.stepEnergy}')

        #prepare for next step
        self.vout = self.voutFinal

class NOR:
    '''NOR class'''

    def __init__(self, vdd, vinA=0, vinB=0, vout=0, procVarArr=None):
        '''NOR gate \n
        Args:
            procVarArr [List of procVar dicts]: given in order [nmos A, nmos B, pmos A, pmos B]\n
            vdd [float]: Vdd upon initialization\n
            vinA [float]: Vin A upon initialization\n
            vinB [float]: Vin B upon initialization\n
            Vout [float]: Vout upon initialization'''
        #simulation variables, to be loaded in during mapping
        self.vinA = vinA #voltage A at gate [float]
        self.vinB = vinB #voltage B at gate [float]
        self.cld = None #load capacitance [F] (gate capacitance of next transistor(s))
        self.vout = vout #output voltage [V]
        self.vdd = vdd #rail voltage [V]
        #simulation calcuated variables
        self.ssVfinal = None #steady state final output voltage (theoretical, not reached)
        self.ssCurr = None #steady-state current
        self.ssPwr = None #steady-state power
        self.voutFinal = None #actual final output voltage
        self.tau = None #timing constant
        self.stepTime = None #time [s] to complete last operation
        self.stepChg = None #charge [A-s, or coulombs] transferred during last operation
        self.stepEnergy = None #energy [W-s, or joules] consumed during last operation
        #generate transistors
        if procVarArr:
            self.nTrA = tr.FET('n', procVarArr[0])
            self.nTrB = tr.FET('n', procVarArr[1])
            self.pTrA = tr.FET('p', procVarArr[2])
            self.pTrB = tr.FET('p', procVarArr[3])
        else:
            self.nTrA = tr.FET('n', noVar)
            self.nTrB = tr.FET('n', noVar)
            self.pTrA = tr.FET('p', noVar)
            self.pTrB = tr.FET('p', noVar)
        self.cinA = self.nTrA.cgate + self.pTrA.cgate
        self.cinB = self.nTrB.cgate + self.pTrB.cgate
        #map transistors
        #nTr
        self.nTrA.inGate = True
        self.nTrA.validateModel()
        self.nTrB.inGate = True
        self.nTrB.validateModel()
        #pTr
        self.pTrA.inGate = True
        self.pTrA.vrail = self.vdd
        self.pTrA.validateModel()
        self.pTrB.inGate = True
        self.pTrB.vrail = self.vdd
        self.pTrB.validateModel()

    def validateModel(self):
        '''Validates whether model is set up correctly'''
        #simulation variables
        assert self.vinA>=0
        assert self.vinB>=0
        assert self.cld>=0
        assert self.vout>=0
        assert self.vdd>0

    def step(self):
        '''Step the model forward one time chunk'''
        self.validateModel()
        #calculate steady state parameters
        nRdsA = self.nTrA.rds(self.vinA)
        nRdsB = self.nTrB.rds(self.vinB)
        pRdsA = self.pTrA.rds(self.vinA)
        pRdsB = self.pTrB.rds(self.vinB)
        nRds = nRdsA*nRdsB/(nRdsA+nRdsB)
        pRds = pRdsA + pRdsB
        sumRds = nRds + pRds
        self.ssCurr = self.vdd/sumRds #steady-state current
        self.ssPwr = self.vdd**2/sumRds #steady-state power
        self.ssVfinal = self.vdd*(nRds/sumRds) #steady state final output voltage (theoretical, not reached)
        #calculate transient parameters
        self.tau = self.cld*min(nRds, pRds)
        self.stepTime = self.tau*TAUS_PER_OPERATION
        deltaVpercentage = 1-math.exp(-TAUS_PER_OPERATION)
        deltaV = (self.ssVfinal-self.vout) * deltaVpercentage 
        self.voutFinal = self.vout + deltaV #actual final output voltage
        self.stepChg = self.cld * deltaV
        self.stepEnergy = (1/2)*self.cld*(deltaV**2)
        # print(f'pRds is {pRds}')
        # print(f'nRds is {nRds}')
        # print(f'sumRds is {sumRds}')
        # print(f'self.ssCurr is {self.ssCurr}')
        # print(f'self.ssPwr is {self.ssPwr}')
        # print(f'self.stepChg is {self.stepChg}')
        # print(f'self.stepEnergy is {self.stepEnergy}')

        #prepare for next step
        self.vout = self.voutFinal

class XOR:
    '''XOR class'''

    def __init__(self, vdd, vinA=0, vinB=0, vout=0, procVarArr=None):
        '''XOR gate \n
        Args:
            procVarArr [List of procVar dicts, N=8]: given in order 
                [nmos abAB, pmos abAB, invA-np, invB-np]
                    (for abAB the capitals are compliment)
            vdd [float]: Vdd upon initialization\n
            vinA [float]: Vin A upon initialization\n
            vinB [float]: Vin B upon initialization\n
            Vout [float]: Vout upon initialization'''
        #simulation variables, to be loaded in during mapping
        self.vinA = vinA #voltage A at gate [float]
        self.vinB = vinB #voltage B at gate [float]
        self.cld = None #load capacitance [F] (gate capacitance of next transistor(s))
        self.vout = vout #output voltage [V]
        self.vdd = vdd #rail voltage [V]
        #simulation calcuated variables
        self.ssVfinal = None #steady state final output voltage (theoretical, not reached)
        self.ssCurr = None #steady-state current
        self.ssPwr = None #steady-state power
        self.voutFinal = None #actual final output voltage
        self.tau = None #timing constant
        self.stepTime = None #time [s] to complete last operation
        self.stepChg = None #charge [A-s, or coulombs] transferred during last operation
        self.stepEnergy = None #energy [W-s, or joules] consumed during last operation
        #generate transistors
        if procVarArr:
            self.nTra = tr.FET('n', procVarArr[0])
            self.nTrb = tr.FET('n', procVarArr[1])
            self.nTrA = tr.FET('n', procVarArr[2])
            self.nTrB = tr.FET('n', procVarArr[3])

            self.pTra = tr.FET('p', procVarArr[4])
            self.pTrb = tr.FET('p', procVarArr[5])
            self.pTrA = tr.FET('p', procVarArr[6])
            self.pTrB = tr.FET('p', procVarArr[7])

            self.invA = INV(vdd=self.vdd, vout=0, vin=self.vinA, procVarArr=procVarArr[8:10])
            self.invA.cld = self.nTrA.cgate + self.pTrA.cgate
            self.invB = INV(vdd=self.vdd, vout=0, vin=self.vinB, procVarArr=procVarArr[10:12])
            self.invB.cld = self.nTrB.cgate + self.pTrB.cgate
        else:
            self.nTra = tr.FET('n', noVar)
            self.nTrb = tr.FET('n', noVar)
            self.nTrA = tr.FET('n', noVar)
            self.nTrB = tr.FET('n', noVar)

            self.pTra = tr.FET('p', noVar)
            self.pTrb = tr.FET('p', noVar)
            self.pTrA = tr.FET('p', noVar)
            self.pTrB = tr.FET('p', noVar)

            self.invA = INV(vdd=self.vdd, vout=0, vin=self.vinA)
            self.invA.cld = self.nTrA.cgate + self.pTrA.cgate
            self.invB = INV(vdd=self.vdd, vout=0, vin=self.vinB)
            self.invB.cld = self.nTrB.cgate + self.pTrB.cgate
        self.cinA = self.nTrA.cgate + self.pTrA.cgate + self.invA.cin
        self.cinB = self.nTrB.cgate + self.pTrB.cgate + self.invB.cin
        #map transistors
        #nTr
        self.nTra.inGate = True
        self.nTra.validateModel()
        self.nTrA.inGate = True
        self.nTrA.validateModel()
        self.nTrb.inGate = True
        self.nTrb.validateModel()
        self.nTrB.inGate = True
        self.nTrB.validateModel()
        #pTr
        self.pTra.inGate = True
        self.pTra.vrail = self.vdd
        self.pTra.validateModel()
        self.pTrA.inGate = True
        self.pTrA.vrail = self.vdd
        self.pTrA.validateModel()
        self.pTrb.inGate = True
        self.pTrb.vrail = self.vdd
        self.pTrb.validateModel()
        self.pTrB.inGate = True
        self.pTrB.vrail = self.vdd
        self.pTrB.validateModel()

    def validateModel(self):
        '''Validates whether model is set up correctly'''
        #simulation variables
        assert self.vinA>=0
        assert self.vinB>=0
        assert self.cld>=0
        assert self.vout>=0
        assert self.vdd>0

    def chgInputs(self, vinA, vinB):
        self.vinA = vinA
        self.vinB = vinB
        self.invA.vin = vinA
        self.invB.vin = vinB

    def step(self):
        '''Step the model forward one time chunk'''
        self.validateModel()
        #calculate steady state parameters
        self.invA.step()
        self.invB.step()
        self.invA.vout = self.invA.voutFinal
        self.invB.vout = self.invB.voutFinal

        nRdsa = self.nTrA.rds(self.vinA)
        nRdsb = self.nTrB.rds(self.vinB)
        nRdsA = self.nTrA.rds(self.invA.voutFinal)
        nRdsB = self.nTrB.rds(self.invB.voutFinal)
        pRdsa = self.pTrA.rds(self.vinA)
        pRdsb = self.pTrB.rds(self.vinB)
        pRdsA = self.pTrA.rds(self.invA.voutFinal)
        pRdsB = self.pTrB.rds(self.invB.voutFinal)

        nRdsab = nRdsa + nRdsb
        nRdsAB = nRdsA + nRdsB
        nRds = nRdsab*nRdsAB/(nRdsab+nRdsAB)

        pRdsab = pRdsa*pRdsb/(pRdsa+pRdsb)
        pRdsAB = pRdsA*pRdsB/(pRdsA+pRdsB)
        pRds = pRdsab + pRdsAB

        sumRds = nRds + pRds
        self.ssCurr = self.vdd/sumRds + self.invA.ssCurr + self.invB.ssCurr #steady-state current
        self.ssPwr = self.vdd**2/sumRds + self.invA.ssPwr + self.invB.ssPwr #steady-state power
        self.ssVfinal = self.vdd*(nRds/sumRds) #steady state final output voltage (theoretical, not reached)
        #calculate transient parameters
        self.tau = self.cld*min(nRds, pRds)
        self.stepTime = self.tau*TAUS_PER_OPERATION + max(self.invA.stepTime, self.invB.stepTime)
        deltaVpercentage = 1-math.exp(-TAUS_PER_OPERATION)
        deltaV = (self.ssVfinal-self.vout) * deltaVpercentage 
        self.voutFinal = self.vout + deltaV #actual final output voltage
        self.stepChg = self.cld * deltaV + self.invA.stepChg + self.invB.stepChg
        self.stepEnergy = (1/2)*self.cld*(deltaV**2) + self.invA.stepEnergy + self.invB.stepEnergy
        # print(f'pRds is {pRds}')
        # print(f'nRds is {nRds}')
        # print(f'sumRds is {sumRds}')
        # print(f'self.ssCurr is {self.ssCurr}')
        # print(f'self.ssPwr is {self.ssPwr}')
        # print(f'self.stepChg is {self.stepChg}')
        # print(f'self.stepEnergy is {self.stepEnergy}')

        #prepare for next step
        self.vout = self.voutFinal

if __name__ == '__main__':
    import numpy as np
    import dataSimulator as ds
    cl.green('Test Code Start')
    noVar = ds.noVar.copy()
    procVar1s = ds.procVar1s.copy()
    procVar1sRon = ds.genCornerRon(1)
    procVarNeg1sRon = ds.genCornerRon(-1)
    procVar3sRon = ds.genCornerRon(3)
    procVarNeg3sRon = ds.genCornerRon(-3)

    #test inv
    # #0 to 1
    # inv = INV(vdd=1.8, vout=0, vin=0)
    # inv.cld = inv.nTr.cgate*8
    # inv.step()
    # print(f'A: {inv.vin:.2f}\t Out: {inv.voutFinal:.2f}')
    # #1 to 0
    # inv = INV(vdd=1.8, vout=0, vin=1.8)
    # inv.cld = inv.nTr.cgate*8
    # inv.step()
    # print(f'A: {inv.vin:.2f}\t Out: {inv.voutFinal:.2f}')
    #in sequence:
    cl.blue(f'Inverter sequence')
    testPtrn = [0, 1.8, 0, 1.8]
    inv = INV(vdd=1.8, vout=0, vin=0)
    inv.cld = inv.nTr.cgate*8
    print(f'A: {inv.vin:.2f}\t Out: {inv.vout:.2f}')
    for vin in testPtrn:
        inv.vin = vin
        inv.step()
        print(f'A: {inv.vin:.2f}\t Out: {inv.voutFinal:.2f}')
        


    #test NAND
    # nand = NAND(vdd=3.0, vout=0, vinA=1.5, vinB=1.5)
    # nand.cld = nand.nTrA.cgate*8
    # nand.step()
    # print(f'A: {nand.vinA:.2f}\t B: {nand.vinB:.2f}   Out: {nand.voutFinal:.2f}')
    # #00
    # nand = NAND(vdd=1.8, vout=0, vinA=0, vinB=0)
    # nand.cld = nand.nTrA.cgate*8
    # nand.step()
    # print(f'A: {nand.vinA:.2f}\t B: {nand.vinB:.2f}   Out: {nand.voutFinal:.2f}')
    # #01
    # nand = NAND(vdd=1.8, vout=0, vinA=0, vinB=1.8)
    # nand.cld = nand.nTrA.cgate*8
    # nand.step()
    # print(f'A: {nand.vinA:.2f}\t B: {nand.vinB:.2f}   Out: {nand.voutFinal:.2f}')
    # #10
    # nand = NAND(vdd=1.8, vout=0, vinA=1.8, vinB=0)
    # nand.cld = nand.nTrA.cgate*8
    # nand.step()
    # print(f'A: {nand.vinA:.2f}\t B: {nand.vinB:.2f}   Out: {nand.voutFinal:.2f}')
    # #11
    # nand = NAND(vdd=1.8, vout=0, vinA=1.8, vinB=1.8)
    # nand.cld = nand.nTrA.cgate*8
    # nand.step()
    # print(f'A: {nand.vinA:.2f}\t B: {nand.vinB:.2f}   Out: {nand.voutFinal:.2f}')
    #in sequence:
    cl.blue(f'NAND sequence')
    testPtrnA = [0, 1.8, 0, 1.8]
    testPtrnB = [0, 1.8, 0, 1.8]
    nand = NAND(vdd=1.8, vout=0)
    nand.cld = nand.nTrA.cgate*8
    print(f'A: {nand.vinA:.2f}\t B: {nand.vinB:.2f}   Out: {nand.vout:.2f}')
    for i in range(len(testPtrnA)):
        nand.vinA = testPtrnA[i]
        nand.vinB = testPtrnB[i]
        nand.step()
        print(f'A: {nand.vinA:.2f}\t B: {nand.vinB:.2f}   Out: {nand.voutFinal:.2f}')


    # #test NOR
    # # nor = NOR(vdd=3.0, vout=0, vinA=1.5, vinB=1.5)
    # # nor.cld = nor.nTrA.cgate*8
    # # nor.step()
    # # print(f'A: {nor.vinA:.2f}\t B: {nor.vinB:.2f}   Out: {nor.voutFinal:.2f}')
    # #00
    # nor = NOR(vdd=1.8, vout=0, vinA=0, vinB=0)
    # nor.cld = nor.nTrA.cgate*8
    # nor.step()
    # print(f'A: {nor.vinA:.2f}\t B: {nor.vinB:.2f}   Out: {nor.voutFinal:.2f}')
    # #01
    # nor = NOR(vdd=1.8, vout=0, vinA=0, vinB=1.8)
    # nor.cld = nor.nTrA.cgate*8
    # nor.step()
    # print(f'A: {nor.vinA:.2f}\t B: {nor.vinB:.2f}   Out: {nor.voutFinal:.2f}')
    # #10
    # nor = NOR(vdd=1.8, vout=0, vinA=1.8, vinB=0)
    # nor.cld = nor.nTrA.cgate*8
    # nor.step()
    # print(f'A: {nor.vinA:.2f}\t B: {nor.vinB:.2f}   Out: {nor.voutFinal:.2f}')
    # #11
    # nor = NOR(vdd=1.8, vout=0, vinA=1.8, vinB=1.8)
    # nor.cld = nor.nTrA.cgate*8
    # nor.step()
    # print(f'A: {nor.vinA:.2f}\t B: {nor.vinB:.2f}   Out: {nor.voutFinal:.2f}')
    #in sequence:
    cl.blue(f'NOR sequence')
    testPtrnA = [0, 0, 0, 0]
    testPtrnB = [0, 1.8, 0, 1.8]
    nor = NOR(vdd=1.8, vout=0)
    nor.cld = nor.nTrA.cgate*8
    print(f'A: {nor.vinA:.2f}\t B: {nor.vinB:.2f}   Out: {nor.vout:.2f}')
    for i in range(len(testPtrnA)):
        nor.vinA = testPtrnA[i]
        nor.vinB = testPtrnB[i]
        nor.step()
        print(f'A: {nor.vinA:.2f}\t B: {nor.vinB:.2f}   Out: {nor.voutFinal:.2f}')
        

    # #test XOR
    # xor = XOR(vdd=3.0, vout=0, vinA=1.5, vinB=1.5)
    # xor.cld = xor.nTrA.cgate*8
    # xor.step()
    # print(f'A: {xor.vinA:.2f}\t B: {xor.vinB:.2f}   Out: {xor.voutFinal:.2f}')
    # exit()
    # initVout = 0
    # #00
    # xor = XOR(vdd=1.8, vout=initVout, vinA=0, vinB=0)
    # xor.cld = xor.nTrA.cgate*8
    # xor.step()
    # print(f'A: {xor.vinA:.2f}\t B: {xor.vinB:.2f}   Out: {xor.voutFinal:.2f}')
    # #01
    # xor = XOR(vdd=1.8, vout=initVout, vinA=0, vinB=1.8)
    # xor.cld = xor.nTrA.cgate*8
    # xor.step()
    # print(f'A: {xor.vinA:.2f}\t B: {xor.vinB:.2f}   Out: {xor.voutFinal:.2f}')
    # #10
    # xor = XOR(vdd=1.8, vout=initVout, vinA=1.8, vinB=0)
    # xor.cld = xor.nTrA.cgate*8
    # xor.step()
    # print(f'A: {xor.vinA:.2f}\t B: {xor.vinB:.2f}   Out: {xor.voutFinal:.2f}')
    # #11
    # xor = XOR(vdd=1.8, vout=initVout, vinA=1.8, vinB=1.8)
    # xor.cld = xor.nTrA.cgate*8
    # xor.step()
    # print(f'A: {xor.vinA:.2f}\t B: {xor.vinB:.2f}   Out: {xor.voutFinal:.2f}')
    #in sequence:
    cl.blue(f'NOR sequence')
    testPtrnA = [0, 0, 0, 0]
    testPtrnB = [0, 1.8, 0, 1.8]
    xor = XOR(vdd=1.8, vout=0)
    xor.cld = xor.nTrA.cgate*8
    print(f'A: {xor.vinA:.2f}\t B: {xor.vinB:.2f}   Out: {xor.vout:.2f}')
    for i in range(len(testPtrnA)):
        xor.chgInputs(testPtrnA[i], testPtrnB[i])
        xor.step()
        print(f'A: {xor.vinA:.2f}\t B: {xor.vinB:.2f}   Out: {xor.voutFinal:.2f}')
        # print(f'inv B voutFinal: {xor.invB.voutFinal}')
        

        




    




    
    
