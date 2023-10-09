'''transistor.py generates transistor models'''

# Author: Luke Henderson
__version__ = '1.0'

import math

import colors as cl
import debugTools as dt

class FET:
    '''FET class'''

    ELECTRON_Q = 1.6e-19 #elementary charge [C]
    ROFF = 100e3 #Roff = 100kOhms

    def __init__(self, chanType, procVar):
        '''MOSFET model\n
        Args:
            chanType [str]: 'n' or 'p' for nmos or pmos\n
            procVar [dict]: process variation randomization parameters
                'epox': epsilon of oxide [+/- percentage]\n
                'tox': oxide thickness [+/- nm]\n
                'w': transistor width [+/- nm]\n
                'l': transistor length [+/- nm]\n
                'na': doping concentration [+/- percentage]'''
        if chanType!='n' and chanType!='p':
            cl.red('Error: chanType not valid')
            exit()
        self.chanType = chanType
        self.epox = 1.2396e-10 * (1+procVar['epox']/100) #[F/m]
        self.tox  = 5 + procVar['tox'] #[nm]
        self.w = 240 + procVar['w'] #[nm]
        self.l = 30 + procVar['l'] #[nm]
        self.cgate = self.epox * self.w*1e-9 * self.l*1e-9 / (self.tox*1e-9)  #Cgate, gate capacitance [F]
        self.vth0 = 0.75 #V
        self.na = 9e23 * (1+procVar['na']/100) #doping concentration
        self.xd = 10 #depletion layer width [nm]
        self.cox = self.epox / (self.tox*1e-9) #gate oxide capacitance per unit area
        self.vth = self.vth0 - (self.ELECTRON_Q*self.na * self.xd*1e-9)/self.cox #threshold voltage [V]
        self.un = 0.85 * (1-0.25*(procVar['na']/100)) #mu-n, [m^2/(Volt-seconds)]
        self.ronCoef = self.un * self.cox * (self.w/self.l) #R-on coeficient, on-resistance of transistor [Ohms]
        # self.cgate = self.cox*self.w*1e-9*self.l*1e-9 #Cgate, gate capacitance [F]

        #simulation variables, to be loaded in during mapping
        self.inGate = None #Transistor is stand-alone (False), or part of a logic gate (True) [bool]
        self.vgate = None #voltage at gate [float]
        self.cld = None #load capacitance [F] (gate capacitance of next transistor(s))
        self.dConf = None #drain configuration, could be 'vdd' (Vdd) or 'ld' (load)
        self.sConf = None #source configuration, could be 'vss' (Vss) or 'ld' (load)
        self.voutConf = None #output voltage configuration, could be 'd' or 's', needs to match d/sConf information 
        self.vout = None #output voltage [V]
        self.vrail = None #rail voltage [V]
        #simulation calcuated variables
        self.stepRds = None #stored rds [Ohms] per step, to save time
        self.tau = None #timing constant
        self.stepTime = None #time [s] to complete last operation
        self.stepChg = None #charge [A-s, or coulombs] transferred during last operation
        self.stepEnergy = None #energy [W-s, or joules] consumed during last operation
        
    def validateModel(self):
        '''Validates whether model is set up correctly'''
        assert self.chanType=='n' or self.chanType=='p'
        assert self.epox>0 and self.epox<1 #[F/m]
        assert self.tox>0 #[nm]
        assert self.w>0 #[nm]
        assert self.l>0 #[nm]
        assert self.cgate>=0  #load capacitance [F]
        assert self.vth0>0 #V
        assert self.na>1e10 #doping concentration
        assert self.xd>0 #depletion layer width [nm]
        assert self.cox>=0 #gate oxide capacitance per unit area
        assert self.vth>0 #threshold voltage [V]
        assert self.un>0 #mu-n, [m^2/(Volt-seconds)]
        assert self.ronCoef>0 #R-on coeficient, on-resistance of transistor [Ohms]
        # assert self.cgate>0 #Cgate, gate capacitance [F]

        #simulation variables
        if not self.inGate:
            assert isinstance(self.vgate, (int, float)) and self.vgate>= 0 #voltage at gate
            assert self.cld>=0 #load capacitance
            assert self.dConf=='vdd' or self.dConf=='ld' #drain configuration
            assert self.sConf=='vss' or self.sConf=='ld'#source configuration
            assert self.voutConf=='d' or self.voutConf=='s' #output voltage configuration
            assert isinstance(self.vout, (int, float)) #output voltage
            assert isinstance(self.vrail, (int, float)) and self.vrail>=0 #rail voltage
        if self.chanType == 'p':
            assert isinstance(self.vrail, (int, float)) and self.vrail>=0 #rail voltage 

    def rds(self, vgate):
        '''Calculate Rds based on Vgate\n
        Args:
            vgate [float]: gate voltage, always positive (Vg-Vss)
        Return:
            Rds [float]: drain-to-source resistance (Ohms)'''
        assert vgate >= 0
        # assert eqVgs != self.vth #avoid div by zero
        if self.chanType == 'p':
            assert isinstance(self.vrail, (int, float))
            eqVgs = -1*(vgate - self.vrail) #equation Vgs, which for pmos is in reference to vrail
        else: #'n'
            eqVgs = vgate
        assert eqVgs >= 0

        if eqVgs <= self.vth: #avoid div by zero, and negative case
            return self.ROFF
        return min(self.ROFF, 1/(self.ronCoef * (eqVgs-self.vth)))


    def step(self):
        '''Step the transistor model forward one time chunk\n
        Notes:
            self.vgate is always positive (Vg-Vss)
                however, for pmos the rds() method depends on the current Vs
        Args:
        Return: '''
        TAUS_PER_OPERATION = 3
        self.validateModel()
        self.stepRds = self.rds(self.vgate)
        if self.chanType == 'n':
            if self.dConf=='vdd': #will assume that source is load
                self.tau = self.cld*self.stepRds
                self.stepTime = self.tau*TAUS_PER_OPERATION
                # print(f'self.stepTime={self.stepTime}')
                deltaVpercentage = 1-math.exp(-self.stepTime/(self.tau))
                deltaV = (self.vrail-self.vout) * deltaVpercentage
                self.vout = self.vout + deltaV
                self.stepChg = self.cld * deltaV
                self.stepEnergy = (1/2)*self.cld*(deltaV**2)
                # print(f'avg power during operation = {}')
            else:
                cl.red("drain configuration 'ld' not implemented")
        else: #self.chanType == 'p'
            cl.red('p channel not implemented')
        
            


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

    #nmos
    tr = FET('n', noVar)
    tr1s = FET('n', procVar1sRon)
    trNeg1s = FET('n', procVarNeg1sRon)
    tr3s = FET('n', procVar3sRon)
    trNeg3s = FET('n', procVarNeg3sRon)
    # cl.blue('nmos')
    # print(f'epox is {tr.epox}')
    # print(f'w is {tr.w}')
    # print(f'l is {tr.l}')
    # print(f'cgate is {tr.cgate}')
    # print(f'vth is {tr.vth}')
    # print(f'ronCoef is {tr.ronCoef}')

    #pmos
    vdd = 3.0 
    pTr = FET('p', noVar)
    pTr1s = FET('p', procVar1sRon)
    pTrNeg1s = FET('p', procVarNeg1sRon)
    pTr3s = FET('p', procVar3sRon)
    pTrNeg3s = FET('p', procVarNeg3sRon)
    pTr.vrail = vdd
    pTr1s.vrail = vdd
    pTrNeg1s.vrail = vdd
    pTr3s.vrail = vdd
    pTrNeg3s.vrail = vdd
    # cl.blue('pmos')
    # print(f'epox is {pTr.epox}')
    # print(f'w is {pTr.w}')
    # print(f'l is {pTr.l}')
    # print(f'cgate is {pTr.cgate}')
    # print(f'vth is {pTr.vth}')
    # print(f'ronCoef is {pTr.ronCoef}')

    # #nmos
    # cl.blue('Rds calculations: ')
    # print(f'ronCoef (of tr)      is {tr.ronCoef}')
    # print(f'ronCoef (of tr1s)    is {tr1s.ronCoef}')
    # print(f'ronCoef (of trNeg1s) is {trNeg1s.ronCoef}')
    # print('\n')
    # print(f'tr resistance      @ Vgs=1: {tr.rds(1)}')
    # print(f'tr1s resistance    @ Vgs=1: {tr1s.rds(1)}')
    # print(f'trNeg1s resistance @ Vgs=1: {trNeg1s.rds(1)}')
    # print(f'1-sigma difference = {round(tr1s.rds(1)-tr.rds(1),3)} Ω')
    # print('\n')
    # cl.blue('Rds(on) calculations: ')
    # print(f'trNeg3s Rds(on) 1.0V is {trNeg3s.rds(1)}')
    # print(f'tr      Rds(on) 1.0V is {tr.rds(1)}')
    # print(f'tr3s    Rds(on) 1.0V is {tr3s.rds(1)}')
    # print('-----------------------------------')
    # print(f'trNeg3s Rds(on) 1.5V is {trNeg3s.rds(1.5)}')
    # print(f'tr      Rds(on) 1.5V is {tr.rds(1.5)}')
    # print(f'tr3s    Rds(on) 1.5V is {tr3s.rds(1.5)}')
    # print('-----------------------------------')
    # print(f'trNeg3s Rds(on) 2.0V is {trNeg3s.rds(2)}')
    # print(f'tr      Rds(on) 2.0V is {tr.rds(2)}')
    # print(f'tr3s    Rds(on) 2.0V is {tr3s.rds(2)}')
    # print('\n')
    # cl.blue('Vth calculations: (over worst case Vth)')
    # tr3s = FET('n', ds.genCornerVth(3))
    # trNeg3s = FET('n', ds.genCornerVth(-3))
    # print(f'trNeg3s Vth is {trNeg3s.vth}')
    # print(f'tr      Vth is {tr.vth}')
    # print(f'tr3s    Vth is {tr3s.vth}')
    # cl.blue('Cgate calculations: (over worst case Cgate)')
    # tr3s = FET('n', ds.genCornerCgate(3))
    # trNeg3s = FET('n', ds.genCornerCgate(-3))
    # print(f'trNeg3s Cgate is {trNeg3s.cgate*1e15}\tfF')
    # print(f'tr      Cgate is {tr.cgate*1e15}\tfF')
    # print(f'tr3s    Cgate is {tr3s.cgate*1e15}\tfF')

    # #pmos
    # cl.blue('Rds calculations: ')
    # print(f'ronCoef (of pTr)      is {pTr.ronCoef}')
    # print(f'ronCoef (of pTr1s)    is {pTr1s.ronCoef}')
    # print(f'ronCoef (of pTrNeg1s) is {pTrNeg1s.ronCoef}')
    # print('\n')
    # print(f'pTr resistance      @ Vgs=1: {pTr.rds(1)}')
    # print(f'pTr1s resistance    @ Vgs=1: {pTr1s.rds(1)}')
    # print(f'pTrNeg1s resistance @ Vgs=1: {pTrNeg1s.rds(1)}')
    # print(f'1-sigma difference = {round(pTr1s.rds(1)-pTr.rds(1),3)} Ω')
    # print('\n')
    # cl.blue('Vth calculations: ')
    # print(f'pTrNeg3s Vth is {pTrNeg3s.vth}')
    # print(f'pTr      Vth is {pTr.vth}')
    # print(f'pTr3s    Vth is {pTr3s.vth}')
    # print('\n')
    # cl.blue('Rds(on) calculations: ')
    # print(f'pTrNeg3s Rds(on) 1.0V is {pTrNeg3s.rds(1)}')
    # print(f'pTr      Rds(on) 1.0V is {pTr.rds(1)}')
    # print(f'pTr3s    Rds(on) 1.0V is {pTr3s.rds(1)}')
    # print('-----------------------------------')
    # print(f'pTrNeg3s Rds(on) 1.5V is {pTrNeg3s.rds(1.5)}')
    # print(f'pTr      Rds(on) 1.5V is {pTr.rds(1.5)}')
    # print(f'pTr3s    Rds(on) 1.5V is {pTr3s.rds(1.5)}')
    # print('-----------------------------------')
    # print(f'pTrNeg3s Rds(on) 2.0V is {pTrNeg3s.rds(2)}')
    # print(f'pTr      Rds(on) 2.0V is {pTr.rds(2)}')
    # print(f'pTr3s    Rds(on) 2.0V is {pTr3s.rds(2)}')
    # print('\n')
    # cl.blue('Cgate calculations: ')
    # print(f'pTrNeg3s Cgate is {pTrNeg3s.cgate*1e15}\tfF')
    # print(f'pTr      Cgate is {pTr.cgate*1e15}\tfF')
    # print(f'pTr3s    Cgate is {pTr3s.cgate*1e15}\tfF')

    # #plot nmos rds over Ron proc var
    # vgArr = np.linspace(0, 3, 10000)
    # rdsArr = np.array([])
    # for vg in vgArr:
    #     # cl.blue(f'vg = {vg}')
    #     # cl.yellow(f'Rds = {tr.rds(vg)}')
    #     rdsArr = np.append(rdsArr, tr.rds(vg))
    #     # print(f'Rds(on) (bug if transistor is off) = {1/(tr.ronCoef * (vg-tr.vth))}')
    # ronArr1s = np.array([])
    # for vg in vgArr:
    #     ronArr1s = np.append(ronArr1s, tr1s.rds(vg))
    # ronArrNeg1s = np.array([])
    # for vg in vgArr:
    #     ronArrNeg1s = np.append(ronArrNeg1s, trNeg1s.rds(vg))
    # ronArr3s = np.array([])
    # for vg in vgArr:
    #     ronArr3s = np.append(ronArr3s, tr3s.rds(vg))
    # ronArrNeg3s = np.array([])
    # for vg in vgArr:
    #     ronArrNeg3s = np.append(ronArrNeg3s, trNeg3s.rds(vg))
    # multiY = [ronArr3s, ronArr1s, rdsArr, ronArrNeg1s, ronArrNeg3s]
    # multiLabels = ['Rds (3σ)', 'Rds (1σ)', 'Rds (typ.)', 'Rds (-1σ)', 'Rds (-3σ)']

    # import plot
    # plotter = plot.PLOTTER()
    # # plotter.genericPlot(x=vgArr, y=rdsArr, title='Rds vs Vgs', xlabel='Vgs (V)', ylabel='Rds (Ω)')
    # plotter.genericPlot(x=vgArr, multiY=multiY, multiLabels=multiLabels, title='Rds vs Vgs', xlabel='Vgs (V)', ylabel='Rds (Ω)')


    # #plot nmos rds over Vth proc var
    # tr3s = FET('n', ds.genCornerVth(3))
    # trNeg3s = FET('n', ds.genCornerVth(-3))
    # vgArr = np.linspace(0, 3, 10000)
    # rdsArr = np.array([])
    # for vg in vgArr:
    #     rdsArr = np.append(rdsArr, tr.rds(vg))
    # rdsArr3s = np.array([])
    # for vg in vgArr:
    #     rdsArr3s = np.append(rdsArr3s, tr3s.rds(vg))
    # rdsArrNeg3s = np.array([])
    # for vg in vgArr:
    #     rdsArrNeg3s = np.append(rdsArrNeg3s, trNeg3s.rds(vg))
    # multiY = [rdsArr3s, rdsArr, rdsArrNeg3s]
    # multiLabels = ['Vth (3σ)', 'Typical', 'Vth (-3σ)']

    # import plot
    # plotter = plot.PLOTTER()
    # plotter.genericPlot(x=vgArr, multiY=multiY, multiLabels=multiLabels, title='Rds vs Vgs', xlabel='Vgs (V)', ylabel='Rds (Ω)')


    # #plot pmos rds
    # vsgArr = np.linspace(0, -3, 10000)
    # rdsArr = np.array([])
    # for vsg in vsgArr:
    #     # cl.blue(f'vsg = {vsg}')
    #     vgate = pTr.vrail + vsg
    #     # cl.blue(f'vgate = {vgate}')
    #     # cl.yellow(f'Rds = {pTr.rds(vgate)}')
    #     rdsArr = np.append(rdsArr, pTr.rds(vgate))
    #     # print(f'Rds(on) (bug if transistor is off) = {1/(pTr.ronCoef * (-1*vsg-pTr.vth))}')
    # rdsArr1s = np.array([])
    # for vsg in vsgArr:
    #     vgate = pTr.vrail + vsg
    #     rdsArr1s = np.append(rdsArr1s, pTr1s.rds(vgate))
    # rdsArrNeg1s = np.array([])
    # for vsg in vsgArr:
    #     vgate = pTr.vrail + vsg
    #     rdsArrNeg1s = np.append(rdsArrNeg1s, pTrNeg1s.rds(vgate))
    # rdsArr3s = np.array([])
    # for vsg in vsgArr:
    #     vgate = pTr.vrail + vsg
    #     rdsArr3s = np.append(rdsArr3s, pTr3s.rds(vgate))
    # rdsArrNeg3s = np.array([])
    # for vsg in vsgArr:
    #     vgate = pTr.vrail + vsg
    #     rdsArrNeg3s = np.append(rdsArrNeg3s, pTrNeg3s.rds(vgate))
    # multiY = [rdsArr3s, rdsArr1s, rdsArr, rdsArrNeg1s, rdsArrNeg3s]
    # multiLabels = ['Rds (3σ)', 'Rds (1σ)', 'Rds (typ.)', 'Rds (-1σ)', 'Rds (-3σ)']

    # import plot
    # plotter = plot.PLOTTER()
    # plotter.genericPlot(x=vsgArr, y=rdsArr, title='Rds vs Vsg', xlabel='Vsg (V)', ylabel='Rds (Ω)')


    

    # #nmos Id plot (lack of saturation curves)
    # print(f'tr.rds @1.5V is {tr.rds(1.5)}')
    # vds = np.linspace(0, 10, 11)
    # idVgsList = []
    # for vgs in [3.0, 2.5, 2.0, 1.5, 1.0, 0.5]:
    #     idVgsCurve = []
    #     for xValue in vds:
    #         idVgsCurve.append(xValue/tr.rds(vgs)) #compute y value of curve
    #     idVgsList.append(idVgsCurve)
    # vgsLabels = ['Vgs=3.0V', 'Vgs=2.5V', 'Vgs=2.0V', 'Vgs=1.5V', 'Vgs=1.0V', 'Vgs=0.5V']
    # import plot
    # plotter = plot.PLOTTER()
    # plotter.idPlot(vds, idVgsList, vgsLabels, dispPlot=True)


    # #CMOS logic testing
    # vdd = 3.0#1.8

    # pTr = FET('p', noVar)
    # pTr3s = FET('p', procVar3sRon)
    # pTrNeg3s = FET('p', procVarNeg3sRon)
    # pTr.vrail = vdd
    # pTr3s.vrail = vdd
    # pTrNeg3s.vrail = vdd

    # vgArr = np.linspace(0, vdd, 10000)

    # #nmos
    # nRdsArr = np.array([])
    # for vg in vgArr:
    #     nRdsArr = np.append(nRdsArr, tr.rds(vg))
    # #pmos
    # pRdsArr = np.array([])
    # for vg in vgArr:
    #     pRdsArr = np.append(pRdsArr, pTr.rds(vg))
    # #sum
    # sumRdsArr = np.array([])
    # for i in range(len(vgArr)):
    #     sumRdsArr = np.append(sumRdsArr, nRdsArr[i]+pRdsArr[i])
    # #leakage I
    # leakIdArr = np.array([])
    # for i in range(len(sumRdsArr)):
    #     leakIdArr = np.append(leakIdArr, vdd/sumRdsArr[i])
    # #voltage div
    # voutArr = np.array([])
    # for i in range(len(vgArr)):
    #     voutArr = np.append(voutArr, vdd*(nRdsArr[i]/sumRdsArr[i]))
    
    # #plot R
    # multiY = [nRdsArr, pRdsArr, sumRdsArr]
    # multiLabels = ['NMOS', 'PMOS', 'Sum']
    # import plot
    # plotter = plot.PLOTTER()
    # # plotter.genericPlot(x=vgArr, y=nRdsArr, title='Rds vs Vin', xlabel='Vin (V)', ylabel='Rds (Ω)')
    # # plotter.genericPlot(x=vgArr, multiY=multiY, multiLabels=multiLabels, title='Rds vs Vin', xlabel='Vin (V)', ylabel='Rds (Ω)')
    # #plot Vout
    # plotter.genericPlot(x=vgArr, y=voutArr, title='Vout vs Vin', xlabel='Vin (V)', ylabel='Vout (V)')


    #plot leakage I
    pTr = FET('p', noVar)
    pTr3s = FET('p', procVar3sRon)
    pTrNeg3s = FET('p', procVarNeg3sRon)
    
    vddArr = [3.0, 2.4, 1.8, 1.4, 1.2, 1.1, 1.0, 0.9, 0.8] #[1.0, 1.4, 1.8, 2.4, 3.0]
    vinPercentageArr = np.linspace(0, 100, 10000)
    sumRdsArrArr = []
    leakIdArrArr = []
    voutArrArr = []
    for vdd in vddArr:
        pTr.vrail = vdd
        pTr3s.vrail = vdd
        pTrNeg3s.vrail = vdd

        vgArr = np.array([])
        for perc in vinPercentageArr:
            vgArr = np.append(vgArr, perc/100*vdd)

        #nmos
        nRdsArr = np.array([])
        for vg in vgArr:
            nRdsArr = np.append(nRdsArr, tr.rds(vg))
        #pmos
        pRdsArr = np.array([])
        for vg in vgArr:
            pRdsArr = np.append(pRdsArr, pTr.rds(vg))
        #sum
        sumRdsArr = np.array([])
        for i in range(len(vgArr)):
            sumRdsArr = np.append(sumRdsArr, nRdsArr[i]+pRdsArr[i])
        sumRdsArrArr.append(sumRdsArr)
        #leakage I
        leakIdArr = np.array([])
        for i in range(len(sumRdsArr)):
            leakIdArr = np.append(leakIdArr, vdd/sumRdsArr[i])
        leakIdArrArr.append(leakIdArr)
        #voltage div
        voutArr = np.array([])
        for i in range(len(vgArr)):
            voutArr = np.append(voutArr, vdd*(nRdsArr[i]/sumRdsArr[i]))
        voutArrArr.append(voutArr)
    
    multiLabels = []
    for vdd in vddArr:
        multiLabels.append(f'Vdd = {vdd}')
    import plot
    plotter = plot.PLOTTER()
    # plotter.genericPlot(x=vinPercentageArr, y=leakIdArrArr[4], title='Leakage Current vs Vin/Vdd Percentage', xlabel='Vin/Vdd (%)', ylabel='Current (A)')
    # plotter.genericPlot(x=vinPercentageArr, multiY=leakIdArrArr, multiLabels=multiLabels, title='Leakage Current vs Vin/Vdd Percentage', xlabel='Vin/Vdd (%)', ylabel='Current (A)')
    #plot Vout
    # plotter.genericPlot(x=vgArr, y=voutArr, title='Vout vs Vin', xlabel='Vin (V)', ylabel='Vout (V)')
    plotter.genericPlot(x=vinPercentageArr, multiY=voutArrArr, multiLabels=multiLabels, title='Vout vs Vin', xlabel='Vin/Vdd (%)', ylabel='Vout (V)')






    




    
    
