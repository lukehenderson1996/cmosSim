'''procSim.py: Simulated x86 processor based on transistor models'''

# Author: Luke Henderson
__version__ = '0.1'

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

cl.green('Program Start')

#----------------------------------------------------------------init----------------------------------------------------------------
#assert correct module versions 
modV = {cfg:  '0.1',
        cl:   '0.8',
        lg:   '1.3'} #plot: '0.2'
for module in modV:
    errMsg = f'Expecting version {modV[module]} of "{os.path.basename(module.__file__)}". Imported {module.__version__}'
    assert module.__version__ == modV[module], errMsg


#-------------------------------------------------------------main loop-------------------------------------------------------------




######################################how long of a chain is too long?#####################################
# #generate transistors and set system variables
# procVar = ds.genCornerRon(3) #ds.noVar.copy()
# tr1 = tr.FET('n', procVar)
# tr2 = tr.FET('n', procVar)
# vdd = 1.8
# freq = 1e9 #operating frequency [GHz]
# clkCyc = 1/freq #cycle time of clock

# #map transistors
# #tr1
# tr1.vgate = 0.0
# tr1.cld = tr2.cgate*8 #transistor typically connected to 2-4 other logic gates, or 4-8 other transistors
# tr1.dConf = 'vdd'
# tr1.vrail = vdd
# tr1.sConf = 'ld'
# tr1.voutConf = 's'
# tr1.vout = 0
# tr1.validateModel()
# #tr2
# tr2.vgate = tr1.vout
# tr2.cld = 0.0
# tr2.dConf = 'vdd'
# tr2.vrail = vdd
# tr2.sConf = 'ld'
# tr2.voutConf = 's'
# tr2.vout = 0.0
# tr2.validateModel()

# #test stimulus
# #instantaneous increase of tr1 vgate
# cl.blue('First charge')
# tr1.vgate = vdd
# #charge up Cload, assuming it started at 0V
# tr1.step()
# #charges next transistor to lesser vgate
# tr2.vgate = tr1.vout
# print(f'tr2.vgate after charge = {tr2.vgate}')

# i = 1
# while True:
#     i += 1
#     cl.blue(f'Charge #{i}')
#     tr1.vgate = tr2.vgate
#     #charge up Cload, assuming it started at 0V
#     tr1.vout = 0
#     tr2.vgate = 0
#     deltaVpercentage = 1-math.exp(-cutoffTime/(tr1.rds(tr1.vgate)*tr1.cld))
#     print(f'deltaV percentage is {deltaVpercentage}')
#     #charges next transistor to lesser vgate
#     tr1.vout = vdd * deltaVpercentage
#     print(f'tr1.vout = {tr1.vout}')
#     tr2.vgate = tr1.vout
#     print(f'tr2.vgate after charge = {tr2.vgate}\n')
#     ut.pause()









# ######################################time to switch the next transistors#####################################
# #generate transistors and set system variables
# procVar = ds.genCornerRon(0) #ds.noVar.copy()
# tr1 = tr.FET('n', procVar)
# tr1.ronCoef = tr1.ronCoef/2
# tr2 = tr.FET('n', ds.genCornerCgate(3))
# vdd = 1.8
# #map transistors
# tr1.vgate = 0.0
# tr1.cld = tr2.cgate*8 #transistor typically connected to 2-4 other logic gates, or 4-8 other transistors
# tr1.dConf = 'vdd'
# tr1.vrail = vdd
# tr1.sConf = 'ld'
# tr1.voutConf = 's'
# tr1.vout = 0
# tr1.validateModel()

# #test stimulus
# vddArr = np.linspace(0, 3, 1000)
# switTimeArr = np.array([])
# for vdd in vddArr:
#     tr1.vgate = vdd
#     tr1.step()
#     switTimeArr = np.append(switTimeArr, tr1.stepTime)
#     tr1.vout = 0

# #-----------------------------------------------------Ron Plus-----------------------------------------------------
# procVar = ds.genCornerRon(3) #ds.noVar.copy()
# tr1 = tr.FET('n', procVar)
# tr1.ronCoef = tr1.ronCoef/2
# #map transistors
# tr1.vgate = 0.0
# tr1.cld = tr2.cgate*8 #transistor typically connected to 2-4 other logic gates, or 4-8 other transistors
# tr1.dConf = 'vdd'
# tr1.vrail = vdd
# tr1.sConf = 'ld'
# tr1.voutConf = 's'
# tr1.vout = 0
# tr1.validateModel()
# #test stimulus
# switTimeArrRonPlus = np.array([])
# for vdd in vddArr:
#     tr1.vgate = vdd
#     tr1.step()
#     switTimeArrRonPlus = np.append(switTimeArrRonPlus, tr1.stepTime)
#     tr1.vout = 0

# #-----------------------------------------------------Ron Minus-----------------------------------------------------
# procVar = ds.genCornerRon(-3) #ds.noVar.copy()
# tr1 = tr.FET('n', procVar)
# tr1.ronCoef = tr1.ronCoef/2
# #map transistors
# tr1.vgate = 0.0
# tr1.cld = tr2.cgate*8 #transistor typically connected to 2-4 other logic gates, or 4-8 other transistors
# tr1.dConf = 'vdd'
# tr1.vrail = vdd
# tr1.sConf = 'ld'
# tr1.voutConf = 's'
# tr1.vout = 0
# tr1.validateModel()
# #test stimulus
# switTimeArrRonMinus = np.array([])
# for vdd in vddArr:
#     tr1.vgate = vdd
#     tr1.step()
#     switTimeArrRonMinus = np.append(switTimeArrRonMinus, tr1.stepTime)
#     tr1.vout = 0

# #-----------------------------------------------------Cgate Plus-----------------------------------------------------
# procVar = ds.genCornerCgate(3) #ds.noVar.copy()
# tr1 = tr.FET('n', procVar)
# tr1.ronCoef = tr1.ronCoef/2
# #map transistors
# tr1.vgate = 0.0
# tr1.cld = tr2.cgate*8 #transistor typically connected to 2-4 other logic gates, or 4-8 other transistors
# tr1.dConf = 'vdd'
# tr1.vrail = vdd
# tr1.sConf = 'ld'
# tr1.voutConf = 's'
# tr1.vout = 0
# tr1.validateModel()
# #test stimulus
# switTimeArrCgatePlus = np.array([])
# for vdd in vddArr:
#     tr1.vgate = vdd
#     tr1.step()
#     switTimeArrCgatePlus = np.append(switTimeArrCgatePlus, tr1.stepTime)
#     tr1.vout = 0

# #-----------------------------------------------------Cgate Minus-----------------------------------------------------
# procVar = ds.genCornerCgate(-3) #ds.noVar.copy()
# tr1 = tr.FET('n', procVar)
# tr1.ronCoef = tr1.ronCoef/2
# #map transistors
# tr1.vgate = 0.0
# tr1.cld = tr2.cgate*8 #transistor typically connected to 2-4 other logic gates, or 4-8 other transistors
# tr1.dConf = 'vdd'
# tr1.vrail = vdd
# tr1.sConf = 'ld'
# tr1.voutConf = 's'
# tr1.vout = 0
# tr1.validateModel()
# #test stimulus
# switTimeArrCgateMinus = np.array([])
# for vdd in vddArr:
#     tr1.vgate = vdd
#     tr1.step()
#     switTimeArrCgateMinus = np.append(switTimeArrCgateMinus, tr1.stepTime)
#     tr1.vout = 0

# plotter = plot.PLOTTER()
# plotter.genericPlot(x=vddArr, multiY=[switTimeArrCgatePlus, switTimeArrRonPlus, switTimeArr, switTimeArrRonMinus, switTimeArrCgateMinus], 
#                     multiLabels=['Cgate (3σ)', 'Rds (3σ)', 'Typical', 'Rds (-3σ)', 'Cgate (-3σ)'], title='Vdd vs Switching Time', 
#                     xlabel='Vdd (V)', ylabel='Time to switch (seconds)')










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
# wafer = ds.genWafer(100000)
waferArr = []
for i in range(10):
    waferArr.append(ds.genWafer(100000))

# with open('pickle\\10 lots 100k tr.pkl', 'rb') as f:
#     waferArr = pickle.load(f)

# print(np.max(wafer))
# print(np.min(wafer))
# dt.info(wafer, 'wafer')
# for item in wafer:
#     for key, value in item.items():
#         if key=='na':
#             print(f'na = {value}')

# with open('pickle\\10 lots 100k tr.pkl', 'wb') as f:
#     pickle.dump(waferArr, f)

# plotData = ut.listConv(wafer)
plotDataArr = []
multiLabels = []
for wafer, i in zip(waferArr, range(len(waferArr))):
    plotDataArr.append(ut.listConv(wafer)['na'])
    multiLabels.append('Lot #' + str(i+1))
plotter = plot.PLOTTER()
# plotter.binPlot(x=plotData['w'], kde=True, title='Binned Plot of Randomized Data', xlabel='Variation (σ)', ylabel='Count')
plotter.binPlot(multiX=plotDataArr, multiLabels=multiLabels, title='Doping Concentration Variation of Randomly Generated Transistors', xlabel='Variation (%)', ylabel='Count')



