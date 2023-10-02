'''transistor.py generated transistor models'''

# Author: Luke Henderson
__version__ = '0.1'

import colors as cl
import debugTools as dt


class FET:
    '''FET class'''

    ELECTRON_Q = 1.6e-19 #elementary charge [C]

    def __init__(self, chanType, procVar):
        '''MOSFET model\n
        Args:
            chanType [str]: 'n' or 'p' for nmos or pmos\n
            procVar [dict]: process variation randomization parameters
                'epox': epsilon of oxide [+/- percentage]\n
                'tox': oxide thickness [+/- nm]\n
                'w': transistor width [+/- nm]\n
                'l': transistor length [+/- nm]\n
                'na': 
        Return:
        '''
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
        self.vgate = None #voltage at gate [float]
        self.cld = None #load capacitance (gate capacitance of next transistor(s))
        self.dConf = None #drain configuration, could be 'vdd' (Vdd) or 'ld' (load)
        self.sConf = None #source configuration, could be 'vss' (Vss) or 'ld' (load)
        self.voutConf = None #output voltage configuration, could be 'd' or 's', needs to match d/sConf information 
        self.vout = None #output voltage

    def rds(self, vgs):
        '''Calculate Rds based on Vgs\n
        Args:
            vgs [float]: gate-to-source voltage'''
        # if vgs == self.vth:
        #     cl.red('Error: div by 0')
        #     exit()
        if self.chanType == 'n':
            if vgs > self.vth:
                return min(100e3, 1/(self.ronCoef * (vgs-self.vth)**2))
            else:
                return 100e3 #Roff = 100kOhms
        else: #'p'
            if vgs < self.vth: 
                return min(100e3, 1/(self.ronCoef * (self.vth - vgs)**2)) 
            else:
                return 100e3  # Roff = 100kOhms
        
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
        #note the below comments are out of date and only for reference
        assert isinstance(self.vgate, (int, float)) #voltage at gate
        assert self.cld>=0 #load capacitance (gate capacitance of next transistor(s))
        assert self.dConf=='vdd' or self.dConf=='ld' #drain configuration, could be 'vdd' (Vdd) or 'ld' (load)
        assert self.sConf=='vss' or self.sConf=='ld'#source configuration, could be 'vss' (Vss) or 'ld' (load)
        assert self.voutConf=='d' or self.voutConf=='s' #output voltage configuration, could be 'd' or 's', needs to match d/sConf information 
        assert isinstance(self.vout, (int, float)) #output voltage
            


if __name__ == '__main__':
    import numpy as np
    cl.green('Test Code Start')
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
    procVar1sRon = \
        {'epox': -0.5,
         'tox': 0.5,
         'w': -5,
         'l': 5,
         'na': -10}
    procVarNeg1sRon = \
        {'epox': 0.5,
         'tox': -0.5,
         'w': 5,
         'l': -5,
         'na': 10}
    procVar3sRon = \
        {'epox': -1.5,
         'tox': 1.5,
         'w': -15,
         'l': 15,
         'na': -30}
    procVarNeg3sRon = \
        {'epox': 1.5,
         'tox': -1.5,
         'w': 15,
         'l': -15,
         'na': 30}
    tr = FET('n', noVar)
    tr1s = FET('n', procVar1sRon)
    trNeg1s = FET('n', procVarNeg1sRon)
    tr3s = FET('n', procVar3sRon)
    trNeg3s = FET('n', procVarNeg3sRon)
    # print(f'epox is {tr.epox}')
    # print(f'w is {tr.w}')
    # print(f'l is {tr.l}')
    # print(f'cl is {tr.cl}')
    # print(f'vth is {tr.vth}')
    # print(f'ronCoef is {tr.ronCoef}')

    cl.blue('Ron calculations: ')
    print(f'ronCoef (of tr)      is {tr.ronCoef}')
    print(f'ronCoef (of tr1s)    is {tr1s.ronCoef}')
    print(f'ronCoef (of trNeg1s) is {trNeg1s.ronCoef}')
    print('\n')
    print(f'tr resistance      @ Vgs=1: {tr.rds(1)}')
    print(f'tr1s resistance    @ Vgs=1: {tr1s.rds(1)}')
    print(f'trNeg1s resistance @ Vgs=1: {trNeg1s.rds(1)}')
    print(f'1-sigma difference = {round(tr1s.rds(1)-tr.rds(1),3)} Ω')
    print('\n')
    cl.blue('Vth calculations: ')
    print(f'trNeg3s Vth is {trNeg3s.vth}')
    print(f'tr      Vth is {tr.vth}')
    print(f'tr3s    Vth is {tr3s.vth}')
    print('\n')
    cl.blue('Rds(on) calculations: ')
    print(f'trNeg3s Rds(on) 1.0V is {trNeg3s.rds(1)}')
    print(f'tr      Rds(on) 1.0V is {tr.rds(1)}')
    print(f'tr3s    Rds(on) 1.0V is {tr3s.rds(1)}')
    print('-----------------------------------')
    print(f'trNeg3s Rds(on) 1.5V is {trNeg3s.rds(1.5)}')
    print(f'tr      Rds(on) 1.5V is {tr.rds(1.5)}')
    print(f'tr3s    Rds(on) 1.5V is {tr3s.rds(1.5)}')
    print('-----------------------------------')
    print(f'trNeg3s Rds(on) 2.0V is {trNeg3s.rds(2)}')
    print(f'tr      Rds(on) 2.0V is {tr.rds(2)}')
    print(f'tr3s    Rds(on) 2.0V is {tr3s.rds(2)}')
    print('\n')
    cl.blue('Cgate calculations: ')
    print(f'trNeg3s Cgate is {trNeg3s.cgate*1e15}')
    print(f'tr      Cgate is {tr.cgate*1e15} fF')
    print(f'tr3s    Cgate is {tr3s.cgate*1e15}')
    # exit()


    vgsArr = np.linspace(0, 3, 100)
    ronArr = np.array([])
    for vgs in vgsArr:
        # cl.blue(f'vgs = {vgs}')
        # cl.yellow(f'Rds = {tr.rds(vgs)}')
        ronArr = np.append(ronArr, tr.rds(vgs))
        # print(f'Rds = {1/(tr.ronCoef * (vgs-tr.vth))}')
    ronArr1s = np.array([])
    for vgs in vgsArr:
        ronArr1s = np.append(ronArr1s, tr1s.rds(vgs))
    ronArrNeg1s = np.array([])
    for vgs in vgsArr:
        ronArrNeg1s = np.append(ronArrNeg1s, trNeg1s.rds(vgs))
    ronArr3s = np.array([])
    for vgs in vgsArr:
        ronArr3s = np.append(ronArr3s, tr3s.rds(vgs))
    ronArrNeg3s = np.array([])
    for vgs in vgsArr:
        ronArrNeg3s = np.append(ronArrNeg3s, trNeg3s.rds(vgs))
    multiY = [ronArr3s, ronArr1s, ronArr, ronArrNeg1s, ronArrNeg3s]
    multiLabels = ['Rds (3σ)', 'Rds (1σ)', 'Rds (typ.)', 'Rds (-1σ)', 'Rds (-3σ)']

    import plot
    plotter = plot.PLOTTER()
    # plotter.vgsPlot(x=vgsArr, y=ronArr, dispPlot=True)
    plotter.vgsPlot(x=vgsArr, multiY=multiY, multiLabels=multiLabels, dispPlot=True)

    # vds = np.linspace(0, 10, 11)
    # idVgsList = []
    # for vgs in [3.0, 2.5, 2.0, 1.5, 1.0, 0.5]:
    #     idVgsCurve = []
    #     for xValue in vds:
    #         idVgsCurve.append(xValue/tr.rds(vgs)) #compute y value of curve
    #     idVgsList.append(idVgsCurve)
    # vgsLabels = ['Vgs=3.0V', 'Vgs=2.5V', 'Vgs=2.0V', 'Vgs=1.5V', 'Vgs=1.0V', 'Vgs=0.5V']
    # plotter.idPlot(vds, idVgsList, vgsLabels, dispPlot=True)

    
    
