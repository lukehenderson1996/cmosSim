'''procSim.py: Simulated x86 processor based on transistor models'''

# Author: Luke Henderson
__version__ = '0.1'

import os
import numpy as np
import math

import config as cfg
import colors as cl
import debugTools as dt
import utils as ut
import logger as lg
# import plot
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

#generate transistors and set system variables
procVar = ds.genCornerRon(3) #ds.noVar.copy()
tr1 = tr.FET('n', procVar)
tr2 = tr.FET('n', procVar)
vdd = 2.7
freq = 1e9 #operating frequency [GHz]
clkCyc = 1/freq #cycle time of clock

#map transistors
#tr1
tr1.vgate = 0.0
tr1.cld = tr2.cgate*20
tr1.dConf = 'vdd'
tr1.sConf = 'ld'
tr1.voutConf = 's'
tr1.vout = 0.0
tr1.validateModel()
#tr2
tr2.vgate = tr1.vout
tr2.cld = 0.0
tr2.dConf = 'vdd'
tr2.sConf = 'ld'
tr2.voutConf = 's'
tr2.vout = 0.0
tr2.validateModel()


#-------------------------------------------------------------main loop-------------------------------------------------------------

#test stimulus
#instantaneous increase of tr1 vgate
cl.blue('First charge')
tr1.vgate = vdd
cutoffTime = 3*11.1875e-15
#charge up Cload, assuming it started at 0V
deltaVpercentage = 1-math.exp(-cutoffTime/(tr1.rds(tr1.vgate)*tr1.cld))
print(f'deltaV percentage is {deltaVpercentage}')
#charges next transistor to lesser vgate
tr1.vout = vdd * deltaVpercentage
print(f'tr1.vout = {tr1.vout}')
tr2.vgate = tr1.vout
print(f'tr2.vgate after charge = {tr2.vgate}')

i = 1
while True:
    i += 1
    cl.blue(f'Charge #{i}')
    tr1.vgate = tr2.vgate
    #charge up Cload, assuming it started at 0V
    tr1.vout = 0
    tr2.vgate = 0
    deltaVpercentage = 1-math.exp(-cutoffTime/(tr1.rds(tr1.vgate)*tr1.cld))
    print(f'deltaV percentage is {deltaVpercentage}')
    #charges next transistor to lesser vgate
    tr1.vout = vdd * deltaVpercentage
    print(f'tr1.vout = {tr1.vout}')
    tr2.vgate = tr1.vout
    print(f'tr2.vgate after charge = {tr2.vgate}\n')
    ut.pause()



