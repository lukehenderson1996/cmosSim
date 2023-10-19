'''cmosSim.py: Simulated cmos circuitry based on transistor models'''

# Author: Luke Henderson
__version__ = '2.0'

import os
import numpy as np
import math
import pickle
import time

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
modV = {cfg:  '1.0',
        cl:   '0.8',
        lg:   '1.3',
        plot: '1.2',
        ds:   '2.0',
        tr:   '1.0',
        gate: '1.1',
        ts:   '1.3'}
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
# print('Generating...')
# wafer = ds.genWafer(100000)
# waferArr = []
# for i in range(1_000_000):
#     waferArr.append(ds.genWafer(100))

# # with open('pickle\\10k lots 100 tr.pkl', 'rb') as f:
# #     waferArr = pickle.load(f)

# # print(np.max(wafer))
# # print(np.min(wafer))
# # dt.info(wafer, 'wafer')
# # for item in wafer:
# #     for key, value in item.items():
# #         if key=='na':
# #             print(f'na = {value}')

# print('Saving...')
# with open('pickle\\1M lots 100 tr.pkl', 'wb') as f:
#     pickle.dump(waferArr, f)

# print('Plotting...')
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


# #swept validation
# cl.blue(f'Start Inverter Sweep')
# vddList = np.arange(0.1, 3.1, 0.1)
# freqList = np.logspace(np.log10(4e9), np.log10(100e12), num=10)
# logCols = ['Vdd [V]']
# for freq in freqList:
#     logCols.append('{:.1e}'.format(freq))
# invLog = lg.LOGGER(logCols=logCols)

# for vdd in vddList:
#     freqResList = []
#     for freq in freqList:
#         #set system variables
#         # vdd = 1.8
#         cl.blue(f'Vdd = {vdd}')
#         # freq = 1e12 
#         cl.blue(f'Freq = {freq}')
#         tb = ts.TestBench(vdd=vdd, freq=freq)
#         dm = ts.DutManager(tb)
#         #map logic gates
#         inv = gate.INV(vdd)
#         inv.cld = 4*inv.cin
#         #setup dut manager
#         dm.dut = inv
#         dm.input = inv
#         dm.output = inv
#         #begin test
#         tb.setStim('0101000110011011011100100',
#             expRes='1010111001100100100011011')
#         for i in range(tb.ptrnLen):
#             dm.step(i)
#         #check results
#         res = tb.checkRes()
#         if res:
#             freqResList.append(round(tb.avgPwr*1e3, 3)) #'{:.3e}'.format(tb.avgPwr*1e6)
#         else:
#             freqResList.append(False)
#     invLog.simpLog([round(vdd, 2)] + freqResList)






# ######################################Full Adder Full Validation#####################################
# def valFullAdder(vdd, freq, quiet=False, wc=ds.DummyWaferConsumer()):
#     # cl.blue(f'Validate Full Adder \n')
#     #set system variables
#     # vdd = 1.8
#     # freq = 4e9 
#     tb = ts.TestBench(vdd=vdd, freq=freq)
#     dm = ts.MultiDutManager(tb)

#     #map logic gates
#     invNor = gate.INV(vdd, procVarArr=wc.consume(2))
#     invNor.cld = 0
#     nor = gate.NOR(vdd, procVarArr=wc.consume(4))
#     nor.cld = invNor.cin
#     invNand1 = gate.INV(vdd, procVarArr=wc.consume(2))
#     invNand1.cld = nor.cinA
#     nand1 = gate.NAND(vdd, procVarArr=wc.consume(4))
#     nand1.cld = invNand1.cin
#     invNand2 = gate.INV(vdd, procVarArr=wc.consume(4))
#     invNand2.cld = nor.cinB
#     nand2 = gate.NAND(vdd, procVarArr=wc.consume(4))
#     nand2.cld = invNand2.cin
#     xor2 = gate.XOR(vdd, procVarArr=wc.consume(12))
#     xor2.cld = 0
#     xor1 = gate.XOR(vdd, procVarArr=wc.consume(12))
#     xor1.cld = xor2.cinA + nand1.cinB
#     #setup dut manager
#     dm.dut = [xor1, nand2, xor2, nand1, invNand1, invNand2, nor, invNor]
#     dm.input = {'a':[[xor1, 'inA'],[nand2, 'inB']], 
#                 'b':[[xor1, 'inB'],[nand2, 'inA']], 
#                 'cin':[[xor2, 'inB'],[nand1, 'inA']]}
#     dm.output = {'s':xor2, 'cout':invNor}

#     #begin test
#     #print run details
#     # print('                  A + B + Cin   →  Cout Sum')
#     #      Running step # 0: 1 + 1 + 1     →     1 1

#     #set simple test pattern
#     stimPtrnA = '000011110'
#     stimPtrnB = '001100110'
#     stimPtrnC = '010101010'
#     resPtrnS  = '011010010'
#     resPrtnC  = '000101110'

#     # #set exhaustive test pattern
#     # stimPtrnA = ''
#     # stimPtrnB = ''
#     # stimPtrnC = ''
#     # for start in range(8):
#     #     for finish in range(8):
#     #         startBin = format(start, '03b')
#     #         finishBin = format(finish, '03b')
#     #         stimPtrnA += startBin[0]
#     #         stimPtrnB += startBin[1]
#     #         stimPtrnC += startBin[2]
#     #         stimPtrnA += finishBin[0]
#     #         stimPtrnB += finishBin[1]
#     #         stimPtrnC += finishBin[2]
#     # stimPtrnA += '0'
#     # stimPtrnB += '0'
#     # stimPtrnC += '0'
#     # # print(len(stimPtrnA))
#     # # print(f'a: {stimPtrnA}')
#     # # print(f'b: {stimPtrnB}')
#     # # print(f'c: {stimPtrnC}')
#     # resPtrnS = ''
#     # resPrtnC = ''
#     # for i in range(len(stimPtrnA)):
#     #     inputIntA = int(stimPtrnA[i])
#     #     inputIntB = int(stimPtrnB[i])
#     #     inputIntC = int(stimPtrnC[i])
#     #     sum = format(inputIntA+inputIntB+inputIntC, '02b')
#     #     resPtrnS += sum[1]
#     #     resPrtnC += sum[0]
#     # # print(f'S: {resPtrnS}')
#     # # print(f'C: {resPrtnC}')

#     #load stim pattern into simulation
#     tb.setMultiStim({'a':stimPtrnA, 'b':stimPtrnB, 'cin':stimPtrnC}, 
#             expRes={'s':resPtrnS, 'cout':resPrtnC})

#     #step simulation over time for each pattern
#     for i in range(tb.ptrnLen):
#         dm.step(i, quiet)

#     # cl.blue('\nAnalyzing results \n')
#     return tb.checkRes(), tb


# #validate one at a time
# # valFullAdder(vdd=1.8, freq=4e9)

# # #swept (over vdd/freq) validation 
# # cl.blue(f'Start Full Adder Sweep')
# # vddList = np.arange(0.1, 3.1, 0.1)
# # freqList = np.logspace(np.log10(4e9), np.log10(100e12), num=10)
# # logCols = ['Vdd [V]']
# # for freq in freqList:
# #     logCols.append('{:.1e}'.format(freq))
# # faLog = lg.LOGGER(logCols=logCols)

# # for vdd in vddList:
# #     freqResList = []
# #     for freq in freqList:
# #         cl.blue(f'Vdd = {vdd}')
# #         cl.blue(f'Freq = {freq}')
# #         res, tb = valFullAdder(vdd, freq, quiet=True)
# #         if res:
# #             freqResList.append(round(tb.avgPwr*1e3, 3)) #'{:.3e}'.format(tb.avgPwr*1e6)
# #         else:
# #             freqResList.append(False)
# #     faLog.simpLog([round(vdd, 2)] + freqResList)



# #swept (over proc var) validation 
# NUM_WAFERS = 10_000
# startTime = time.time()
# wc = ds.WaferConsumer('pickle\\10k lots 100 tr.pkl')
# wc.waferNum = 0
# # for i in range(2):
# #     subArr = wc.consume(2)
# #     dt.info(subArr, 'subArr')

# powerList = []
# propTimeList = []
# vddMinList = []
# cl.blue('Simulation Start')
# pb = ut.printProgress(NUM_WAFERS, 5)

# # #loop over proc var
# # for i in range(NUM_WAFERS):
# #     wc.waferNum = i
# #     res, tb = valFullAdder(vdd=0.74, freq=1, quiet=True, wc=wc) #work at freq<=20G, not sure about >
# #     if res:
# #         powerList.append(tb.avgPwr*1e3)
# #         propTimeList.append(max(tb.propTimeList))
# #     else:
# #         cl.red('Error: fail')
# #         exit()
# #         powerList.append(False)
# #     pb.update(i)

# #loop over Vdd and proc var
# for i in range(NUM_WAFERS):
#     wc.waferNum = i
#     vdd = 0.67 #no devices pass at this vdd
#     waferFail = True
#     while waferFail:
#         vdd += 0.002
#         res, tb = valFullAdder(vdd=vdd, freq=4e9, quiet=True, wc=wc)
#         if res:
#             # #reset and run again with some margin 
#             # wc.waferIter[i]=0 
#             # vdd += 0.01
#             # res, tb = valFullAdder(vdd=vdd, freq=4e9, quiet=True, wc=wc)
#             #save results
#             vddMinList.append(vdd)
#             powerList.append(tb.avgPwr*1e3)
#             propTimeList.append(max(tb.propTimeList))
#             waferFail = False
#         else:
#             #reset wafer
#             wc.waferIter[i]=0      
#     pb.update(i)

# cl.blue('\n\n' + f'Total sim time: {time.time()-startTime}')
# # dt.info(vddMinList, 'vddMinList')
# # dt.info(powerList, 'powerList')
# # dt.info(propTimeList, 'propTimeList')
# print('Saving pickle files...')
# with open('pickle\\FILE NAME HERE - Vdd min tests 10k - vddMinList.pkl', 'wb') as f:
#     pickle.dump(vddMinList, f)
# with open('pickle\\FILE NAME HERE - Vdd min tests 10k - powerList.pkl', 'wb') as f:
#     pickle.dump(powerList, f)
# with open('pickle\\FILE NAME HERE - Vdd min tests 10k - propTimeList.pkl', 'wb') as f:
#     pickle.dump(propTimeList, f)

# print('Plotting...')
# # plotData = ut.listConv(wafer)
# # plotDataArr = []
# # multiLabels = []
# # for wafer, i in zip(waferArr, range(len(waferArr))):
# #     plotDataArr.append(ut.listConv(wafer)['na'])
# #     multiLabels.append('Lot #' + str(i+1))
# plotter = plot.PLOTTER()
# plotter.binPlot(x=vddMinList, title='Binned Plot of Minimum Passing Vdd', xlabel='Time (s)', ylabel='Count')
# plotter.binPlot(x=powerList, title='Binned Plot of Average Power', xlabel='Power (mW)', ylabel='Count')
# plotter.binPlot(x=propTimeList, title='Binned Plot of Propagation Time', xlabel='Time (s)', ylabel='Count', xLogPlot=True)
# # plotter.binPlot(multiX=plotDataArr, multiLabels=multiLabels, title='Doping Concentration Variation of Randomly Generated Transistors', xlabel='Variation (%)', ylabel='Count')















######################################Yield Analysis#####################################
with open('pickle\\Vdd min + 0.01 tests 10k - vddMinList.pkl', 'rb') as f:
    vddMinList = pickle.load(f)
with open('pickle\\Vdd min + 0.01 tests 10k - powerList.pkl', 'rb') as f:
    powerList = pickle.load(f)
with open('pickle\\Vdd min + 0.01 tests 10k - propTimeList.pkl', 'rb') as f:
    propTimeList = pickle.load(f)

popIdxs = []
for i in range(len(propTimeList)):
    if propTimeList[i] > 30e-12:
        popIdxs.append(i)
for i in reversed(popIdxs):
    vddMinList.pop(i)
    powerList.pop(i)
    propTimeList.pop(i)

assert len(vddMinList)==len(powerList) and len(powerList)==len(propTimeList)
cl.yellow(f'Yield = {len(propTimeList)/100}%')
cl.purple('Vdd min')
print('\t' + f'Min = {min(vddMinList)}')
print('\t' + f'Avg = {np.mean(vddMinList)}')
print('\t' + f'Max = {max(vddMinList)}')
cl.purple('Avg Pwr')
print('\t' + f'Min = {min(powerList)}')
print('\t' + f'Avg = {np.mean(powerList)}')
print('\t' + f'Max = {max(powerList)}')
cl.purple('Prop time')
print('\t' + f'Min = {min(propTimeList)}')
print('\t' + f'Avg = {np.mean(propTimeList)}')
print('\t' + f'Max = {max(propTimeList)}')

print('Plotting...')
plotter = plot.PLOTTER()
plotter.binPlot(x=vddMinList, title='Binned Plot of Minimum Passing Vdd', xlabel='Time (s)', ylabel='Count')
plotter.binPlot(x=powerList, title='Binned Plot of Average Power', xlabel='Power (mW)', ylabel='Count')
plotter.binPlot(x=propTimeList, title='Binned Plot of Propagation Time', xlabel='Time (s)', ylabel='Count', xLogPlot=True)


