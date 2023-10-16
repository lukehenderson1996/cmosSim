'''procSim.py: Simulated x86 processor based on transistor models'''

# Author: Luke Henderson
__version__ = '1.0'

import os
import numpy as np
import math
import pickle

import config as cfg
import colors as cl
import debugTools as dt
import utils as ut
import logger as lg
import plot
import dataSimulator as ds
import transistor as tr
import gate
import testSupport as ts

cl.green('Program Start')

#----------------------------------------------------------------init----------------------------------------------------------------
#assert correct module versions 
modV = {cfg:  '0.1',
        cl:   '0.8',
        lg:   '1.3',
        plot: '1.1',
        ds:   '1.0',
        tr:   '1.0',
        gate: '1.1',
        ts:   '1.2'}
for module in modV:
    errMsg = f'Expecting version {modV[module]} of "{os.path.basename(module.__file__)}". Imported {module.__version__}'
    assert module.__version__ == modV[module], errMsg


#-------------------------------------------------------------main loop-------------------------------------------------------------


######################################Vth min/max graph over process variation#####################################
# #generate transistors and set system variables
# procVar = ds.genCornerVth(0) #ds.noVar.copy()
# tr1 = tr.FET('n', procVar)
# #test stimulus
# vgsArr = np.linspace(0, 3, 1000)
# rdsArr = np.array([])
# for vgs in vgsArr:
#     rdsArr = np.append(rdsArr, tr1.rds(vgs))

# #-----------------------------------------------------Ron Plus-----------------------------------------------------
# procVar = ds.genCornerVth(3) #ds.noVar.copy()
# tr1 = tr.FET('n', procVar)
# #test stimulus
# rdsArrVthPlus = np.array([])
# for vgs in vgsArr:
#     rdsArrVthPlus = np.append(rdsArrVthPlus, tr1.rds(vgs))

# #-----------------------------------------------------Ron Minus-----------------------------------------------------
# procVar = ds.genCornerVth(-3) #ds.noVar.copy()
# tr1 = tr.FET('n', procVar)
# #test stimulus
# rdsArrVthMinus = np.array([])
# for vgs in vgsArr:
#     rdsArrVthMinus = np.append(rdsArrVthMinus, tr1.rds(vgs))

# plotter = plot.PLOTTER()
# plotter.genericPlot(x=vgsArr, multiY=[rdsArrVthPlus, rdsArr, rdsArrVthMinus], 
#                     multiLabels=['Vth (3σ)', 'Typical', 'Vth (-3σ)'], title='Ron vs Vgs', 
#                     xlabel='Vgs (V)', ylabel='Rds (Ω)')






######################################Randomized transistors#####################################
# # procVarArr = ds.genGaussian(1, 10000)
# with open('pickle\\gaussian10k.pkl', 'rb') as f:
#     procVarArr = pickle.load(f)

# print(np.max(procVarArr))
# print(np.min(procVarArr))
# dt.info(procVarArr, 'procVarArr')

# # with open('pickle\\gaussian10k.pkl', 'wb') as f:
# #     pickle.dump(procVarArr, f)

# plotter = plot.PLOTTER()
# plotter.binPlot(x=procVarArr, kde=False, title='Binned Plot of Randomized Data', xlabel='Variation (σ)', ylabel='Count')






######################################Generate wafer#####################################
# # wafer = ds.genWafer(100000)
# # waferArr = []
# # for i in range(10):
# #     waferArr.append(ds.genWafer(100000))

# with open('pickle\\10 lots 100k tr.pkl', 'rb') as f:
#     waferArr = pickle.load(f)

# # print(np.max(wafer))
# # print(np.min(wafer))
# # dt.info(wafer, 'wafer')
# # for item in wafer:
# #     for key, value in item.items():
# #         if key=='na':
# #             print(f'na = {value}')

# # with open('pickle\\10 lots 100k tr.pkl', 'wb') as f:
# #     pickle.dump(waferArr, f)

# # plotData = ut.listConv(wafer)
# plotDataArr = []
# multiLabels = []
# for wafer, i in zip(waferArr, range(len(waferArr))):
#     plotDataArr.append(ut.listConv(wafer)['na'])
#     multiLabels.append('Lot #' + str(i+1))
# plotter = plot.PLOTTER()
# # plotter.binPlot(x=plotData['w'], kde=True, title='Binned Plot of Randomized Data', xlabel='Variation (σ)', ylabel='Count')
# plotter.binPlot(multiX=plotDataArr, multiLabels=multiLabels, title='Doping Concentration Variation of Randomly Generated Transistors', xlabel='Variation (%)', ylabel='Count')


######################################Full Adder#####################################
# cl.blue(f'Test Full Adder')
# #set system variables
# vdd = 1.8 #0.71

# #map logic gates
# invNor = gate.INV(vdd)
# invNor.cld = 0
# nor = gate.NOR(vdd)
# nor.cld = invNor.cin
# invNand1 = gate.INV(vdd)
# invNand1.cld = nor.cinA
# nand1 = gate.NAND(vdd)
# nand1.cld = invNand1.cin
# invNand2 = gate.INV(vdd)
# invNand2.cld = nor.cinB
# nand2 = gate.NAND(vdd)
# nand2.cld = invNand2.cin
# xor2 = gate.XOR(vdd)
# xor2.cld = 0
# xor1 = gate.XOR(vdd)
# xor1.cld = xor2.cinA + nand1.cinB

# #begin test
# #A, B, and C (carry in)
# testPtrnA = [0, 0,   vdd, vdd, 0  , 0  , vdd, vdd, 0]
# testPtrnB = [0, vdd, 0,   vdd, 0  , vdd, 0  , vdd, 0]
# testPtrnC = [0, 0,   0,   0  , vdd, vdd, vdd, vdd, 0]

# print(f'A+B+C = CS (C=Carry-In, then C=Carry-out, S=Sum)')
# resArr = []
# for i in range(len(testPtrnA)):
#     xor1.chgInputs(testPtrnA[i], testPtrnB[i])
#     nand2.vinA = testPtrnA[i]
#     nand2.vinB = testPtrnB[i]
#     xor1.step()
#     nand2.step()

#     xor2.chgInputs(xor1.voutFinal, testPtrnC[i])
#     nand1.vinA = testPtrnC[i]
#     nand1.vinB = xor1.voutFinal
#     xor2.step()
#     nand1.step()

#     invNand1.vin = nand1.voutFinal
#     invNand2.vin = nand2.voutFinal
#     invNand1.step()
#     invNand2.step()

#     nor.vinA = invNand1.voutFinal
#     nor.vinB = invNand2.voutFinal
#     nor.step()
#     invNor.vin = nor.voutFinal
#     invNor.step()

#     # print(f'A: {testPtrnA[i]:.2f}  B: {testPtrnB[i]:.2f}  C: {testPtrnC[i]:.2f}\t Cout: {invNor.voutFinal:.2f}\t Out S: {xor2.voutFinal:.2f}')
    
#     stimA = str(int(testPtrnA[i] > vdd/2))
#     stimB = str(int(testPtrnB[i] > vdd/2))
#     stimC = str(int(testPtrnC[i] > vdd/2))
#     resS  = str(int(invNor.voutFinal > vdd/2))
#     resC  = str(int(xor2.voutFinal > vdd/2))
#     print(f'{stimA}+{stimB}+{stimC} = {resS}{resC}')
#     resArr.append(f'{resS}{resC}')

# if resArr == ['00', '01', '01', '10', '01', '10', '10', '11', '00']:
#     cl.blue('PASS')
# else:
#     cl.red('FAIL')


######################################Inverter Full Validation#####################################
# cl.blue(f'Validate Inverter')
# #set system variables
# vdd = 1.8 #0.71
# freq = 1e12 
# tb = ts.TestBench(vdd=vdd, freq=freq)
# dm = ts.DutManager(tb)

# #map logic gates
# inv = gate.INV(vdd)
# inv.cld = 4*inv.cin
# #setup dut manager
# dm.dut = inv
# dm.input = inv
# dm.output = inv

# #begin test
# tb.setStim('01', #0101000110011011011100100
#     expRes='10') #1010111001100100100011011

# for i in range(tb.ptrnLen):
#     dm.step(i)

# cl.blue('Analyzing results')
# tb.checkRes()
# # tb.prResTable()
# # tb.dispScope()


#swept validation
cl.blue(f'Start Inverter Sweep')
vddList = np.arange(0.1, 3.1, 0.1)
freqList = np.logspace(np.log10(4e9), np.log10(100e12), num=10)
logCols = ['Vdd [V]']
for freq in freqList:
    logCols.append('{:.1e}'.format(freq))
invLog = lg.LOGGER(logCols=logCols)

for vdd in vddList:
    freqResList = []
    for freq in freqList:
        #set system variables
        # vdd = 1.8
        cl.blue(f'Vdd = {vdd}')
        # freq = 1e12 
        cl.blue(f'Freq = {freq}')
        tb = ts.TestBench(vdd=vdd, freq=freq)
        dm = ts.DutManager(tb)
        #map logic gates
        inv = gate.INV(vdd)
        inv.cld = 4*inv.cin
        #setup dut manager
        dm.dut = inv
        dm.input = inv
        dm.output = inv
        #begin test
        tb.setStim('0101000110011011011100100',
            expRes='1010111001100100100011011')
        for i in range(tb.ptrnLen):
            dm.step(i)
        #check results
        res = tb.checkRes()
        if res:
            freqResList.append(round(tb.avgPwr*1e3, 3)) #'{:.3e}'.format(tb.avgPwr*1e6)
        else:
            freqResList.append(False)
    invLog.simpLog([round(vdd, 2)] + freqResList)






# ######################################Full Adder Full Validation#####################################
# cl.blue(f'Validate Full Adder')
# #set system variables
# vdd = 1.8
# freq = 4e9 
# tb = ts.TestBench(vdd=vdd, freq=freq)
# dm = ts.DutManager(tb)

# #map logic gates
# invNor = gate.INV(vdd)
# invNor.cld = 0
# nor = gate.NOR(vdd)
# nor.cld = invNor.cin
# invNand1 = gate.INV(vdd)
# invNand1.cld = nor.cinA
# nand1 = gate.NAND(vdd)
# nand1.cld = invNand1.cin
# invNand2 = gate.INV(vdd)
# invNand2.cld = nor.cinB
# nand2 = gate.NAND(vdd)
# nand2.cld = invNand2.cin
# xor2 = gate.XOR(vdd)
# xor2.cld = 0
# xor1 = gate.XOR(vdd)
# xor1.cld = xor2.cinA + nand1.cinB
# #OLD MAP
# inv = gate.INV(vdd)
# inv.cld = 4*inv.cin
# #setup dut manager
# dm.dut = inv
# dm.input = inv
# dm.output = inv

# #begin test
# tb.setStim('01', #0101000110011011011100100
#     expRes='10') #1010111001100100100011011

# for i in range(tb.ptrnLen):
#     dm.step(i)

# cl.blue('Analyzing results')
# tb.checkRes()
# # tb.prResTable()
# # tb.dispScope()




# exit()

# #begin test
# #A, B, and C (carry in)
# testPtrnA = [0, 0,   vdd, vdd, 0  , 0  , vdd, vdd, 0]
# testPtrnB = [0, vdd, 0,   vdd, 0  , vdd, 0  , vdd, 0]
# testPtrnC = [0, 0,   0,   0  , vdd, vdd, vdd, vdd, 0]

# print(f'A+B+C = CS (C=Carry-In, then C=Carry-out, S=Sum)')
# resArr = []
# for i in range(len(testPtrnA)):
#     xor1.chgInputs(testPtrnA[i], testPtrnB[i])
#     nand2.vinA = testPtrnA[i]
#     nand2.vinB = testPtrnB[i]
#     xor1.step()
#     nand2.step()

#     xor2.chgInputs(xor1.voutFinal, testPtrnC[i])
#     nand1.vinA = testPtrnC[i]
#     nand1.vinB = xor1.voutFinal
#     xor2.step()
#     nand1.step()

#     invNand1.vin = nand1.voutFinal
#     invNand2.vin = nand2.voutFinal
#     invNand1.step()
#     invNand2.step()

#     nor.vinA = invNand1.voutFinal
#     nor.vinB = invNand2.voutFinal
#     nor.step()
#     invNor.vin = nor.voutFinal
#     invNor.step()

#     # print(f'A: {testPtrnA[i]:.2f}  B: {testPtrnB[i]:.2f}  C: {testPtrnC[i]:.2f}\t Cout: {invNor.voutFinal:.2f}\t Out S: {xor2.voutFinal:.2f}')
    
#     stimA = str(int(testPtrnA[i] > vdd/2))
#     stimB = str(int(testPtrnB[i] > vdd/2))
#     stimC = str(int(testPtrnC[i] > vdd/2))
#     resS  = str(int(invNor.voutFinal > vdd/2))
#     resC  = str(int(xor2.voutFinal > vdd/2))
#     print(f'{stimA}+{stimB}+{stimC} = {resS}{resC}')
#     resArr.append(f'{resS}{resC}')

# if resArr == ['00', '01', '01', '10', '01', '10', '10', '11', '00']:
#     cl.blue('PASS')
# else:
#     cl.red('FAIL')