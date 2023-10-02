'''plot.py: Plots data using seaborn and matplotlib'''

# Author: Luke Henderson
__version__ = '0.2'

import math
import time
import numpy as np

import config as cfg
import colors as cl
import utils as ut
import debugTools as dt

PLOT_COLORS = [
    "b",  # blue
    "g",  # green
    "r",  # red
    "c",  # cyan
    "m",  # magenta
    "y",  # yellow
    "k",  # black
    "#FFA07A",  # light salmon
    "#8A2BE2",  # blue violet
    "lime",
    "teal",
    "navy",
    "fuchsia"]

if cfg.plotEn:
    # from seaborn import violinplot as sns_violinplot #this import takes about 1 second
    from seaborn import scatterplot as sns_scatterplot
    from seaborn import lineplot as sns_lineplot
    import matplotlib.pyplot as plt
    from matplotlib import rcParams
    from matplotlib.ticker import EngFormatter
    import matplotlib
    # matplotlib.use('Agg')  # use the Agg backend (NON GUI)

class PLOTTER:
    '''Plotter class'''

    def __init__(self, subFolder=None, livePlotter=False):
        '''Creates violin plots over a period of time\n
        Args:
            subFolder [str, optional]: subfolder to store plots in
                format: 'myfolder' 
            livePlotter [bool, optional]: different save format for live gui plotting'''
        self.pastDataList = []
        self.subFolder = subFolder
        self.livePlotter = livePlotter

    def vgsPlot(self, x=None, y=None, multiY=None, multiLabels=None, dispPlot=False):
        '''Plots Vgs\n
        Args:
            x [np.array]: \n
            y [np.array]: \n
            dispPlot [bool, optional]: 
                True: display plot\n
                False: (NOT IMPLEMENTED) save plot to file'''
 
        # vgs = np.array([2.1, 2.2, 2.3, 2.4, 2.5])
        # ron = np.array([5.0, 5.0, 4.5, 2.5, 1.5])
        
        # plots
        rcParams['figure.figsize'] = 14, 6
        # fig = plt.figure(figsize=(14, 6))
        if multiY:
            assert len(multiY) == len(multiLabels)
            assert len(PLOT_COLORS) > len(multiY)
            for item, label, color in zip(multiY, multiLabels, PLOT_COLORS ):
                fig2 = sns_lineplot(x=x, y=item, label=label, color=color)
        else:
            fig2 = sns_lineplot(x=x, y=y) #x='Vgs', y='Ron' 
        fig2.set_yscale('log')
        fig2.grid('True')
        plt.title('Ron vs Vgs')
        plt.xlabel('Vgs (V)')
        plt.ylabel('Rds(on) (Ω)')
        plt.xticks(rotation=20)
        formatter = EngFormatter()
        plt.gca().yaxis.set_major_formatter(formatter)

        # line1 = []
        # line2 = []
        # for item in x:
        #     line1.append(4)
        #     line2.append(8)
        # plt.plot(x, line2, color='r', linestyle='-.', zorder=0, label='8 Ω')
        # plt.plot(x, line1, color='r', linestyle='-', zorder=0, label='4 Ω')
        plt.legend()


        if dispPlot:
            #plot on screen, blocks main thread
            
            plt.show()

            figStillOpen = plt.gcf()
            plt.clf()
            plt.close(figStillOpen) 
        else:
            pass
            # #plot to file, nonblocking
            # humReadDate, humReadTime, dateObj = ut.humTimeAndObj()
            # # saveDir = ut.pth('', 'rel1')
            # if self.livePlotter:
            #     if zoom==None and self.subFolder==None:
            #         # saveDir += f'/datalogs/plots/live/{plotTime}.png'
            #         saveDir = ut.gpth(f'/datalogs/plots/live/{plotTime}.png', 'rel1')
            #     else:
            #         # saveDir += f'/datalogs/plots/live/{self.subFolder} {plotTime}.png'
            #         saveDir = ut.gpth(f'/datalogs/plots/live/{self.subFolder} {plotTime}.png', 'rel1')
            # elif self.subFolder is None:
            #     # saveDir += f"/datalogs/plots/{humReadDate} {humReadTime.replace(':', '-')} violin_plot.png"
            #     saveDir = ut.gpth(f"/datalogs/plots/{humReadDate} {humReadTime.replace(':', '-')} violin_plot.png", 'rel1')
            # else:
            #     # saveDir += f"/datalogs/plots/{self.subFolder}/{humReadDate} {humReadTime.replace(':', '-')} violin_plot.png"
            #     saveDir = ut.gpth(f"/datalogs/plots/{self.subFolder}/{humReadDate} {humReadTime.replace(':', '-')} violin_plot.png", 'rel1')
            # figSaved = plt.savefig(saveDir)

            # plt.clf()
            # plt.close()
        
    def idPlot(self, vds, idVgsList, vgsLabels, dispPlot=False):
        '''Plots Id vs vds, one curve for each Vgs\n
        Args:
            vds [np.array]: \n
            idVgsList [list of np.array]: start with highest Vgs, then second highest...\n
            vgsLabels [list of str]: must match idVgsList \n
            dispPlot [bool, optional]: 
                True: display plot\n
                False: (NOT IMPLEMENTED) save plot to file'''
        assert len(idVgsList) == len(vgsLabels)
                
        # vds = np.array([0.0, 2.0, 4.0, 6.0, 8.0, 10.0])
        # idVgs1 = np.array([0.1, 0.8, 1.5, 2.0, 2.4, 2.8])
        # idVgs2 = np.array([0.2, 1.6, 3.0, 4.0, 4.8, 5.6])
        # idVgs3 = np.array([0.3, 2.4, 4.5, 6.0, 7.2, 8.4])
        # idVgsList = [idVgs3, idVgs2, idVgs1]
        # vgsLabels = ['Vgs=3V', 'Vgs=2V', 'Vgs=1V']

        #make plots
        rcParams['figure.figsize'] = 14, 6
        # fig = plt.figure(figsize=(14, 6))
        assert len(PLOT_COLORS) > len(idVgsList)
        for curve, color, vgsLabel in zip(idVgsList, self.LOT_COLORS, vgsLabels):
            fig2 = sns_lineplot(x=vds, y=curve, color=color, label=vgsLabel)
        fig2.grid('True')
        plt.title('Comparison of Id vs Vds for Vgs=0.5-3V')
        plt.xlabel('Vds (V)')
        plt.ylabel('Id (A)')
        # plt.xticks(rotation=20)
        # formatter = EngFormatter()
        # plt.gca().yaxis.set_major_formatter(formatter)

        # line1 = []
        # line2 = []
        # for item in x:
        #     line1.append(4)
        #     line2.append(8)
        # plt.plot(x, line2, color='r', linestyle='-.', zorder=0, label='8 Ω')
        # plt.plot(x, line1, color='r', linestyle='-', zorder=0, label='4 Ω')
        # plt.legend()


        if dispPlot:
            #plot on screen, blocks main thread
            
            plt.show()

            figStillOpen = plt.gcf()
            plt.clf()
            plt.close(figStillOpen) 
        else:
            pass
            

    # def violinPlot(self, pricePointList, orderSpeedList, wtmProf, timestamp=None, dispPlot=False, zoom=None):
    #     '''Plots a history of order prices over time\n
    #     Args: 
    #         pricePointList [list of float] \n
    #         orderSpeedList [list of float] \n
    #         wtmProf [float] \n
    #         timestamp [float, optional] \n
    #         dispPlot [bool, optional]: 
    #             True: display plot\n
    #             False: save plot to file
    #         zoom [str, optional]: if '96', will zoom in on ~96% price'''

    #     if timestamp is None:
    #         plotTime = time.time()
    #     else:
    #         plotTime = timestamp
    #     #condition data:
    #     ROUND_CUTOFF = 10 #one place behind the decimal
    #     orderSpeedInts = []
    #     for item in orderSpeedList:
    #         roundedItem = round(item*10**ROUND_CUTOFF)
    #         if roundedItem == 0:
    #             roundedItem = 1
    #         orderSpeedInts.append(roundedItem)

    #     priceViolinList = []
    #     columnStrList = []
    #     newPriceViolinList = []
    #     newColumnStrList = []
    #     HistPriceViolinList = []
    #     HistColumnStrList = []
    #     for i in range(len(pricePointList)):
    #         #set j number of violin lists:
    #         # LENGTH = len(self.pastDataList)
    #         # for j in range(LENGTH):
    #         for dictEl in self.pastDataList:
    #             for k in range(len(dictEl['priceViolinList'])):
    #                 HistPriceViolinList.append(dictEl['priceViolinList'][k])
    #                 minSince = (plotTime-dictEl["time"])/60
    #                 if minSince < 1:
    #                     secSince = minSince*60
    #                     if secSince < 25: 
    #                         timeLabel = f'{round(secSince, 3)} s'
    #                     else:
    #                         timeLabel = f'{round(secSince)} s'
    #                 elif minSince < 25: 
    #                     timeLabel = f'{round(minSince, 2)} m'
    #                 elif minSince < 60: 
    #                     timeLabel = f'{round(minSince)} m'
    #                 else: #longer than 1 hour
    #                     hourSince = minSince/60
    #                     if hourSince < 25:
    #                         timeLabel = f'{round(minSince/60, 2)} h'
    #                     else:
    #                         timeLabel = f'{round(minSince/60)} h'
    #                 HistColumnStrList.append(timeLabel)

    #         #set variables for newest violin plot
    #         loopLength = round(math.log(orderSpeedInts[i], 10))
    #         loopLength = int(loopLength)
    #         if loopLength == 0:
    #             loopLength = 1
    #         for k in range(loopLength):
    #             newPriceViolinList.append(pricePointList[i])
    #             newColumnStrList.append(f'Now')

    #     #save converted data to historical record
    #     self.pastDataList.append({'time': plotTime, 'priceViolinList': newPriceViolinList, 'wtmProf': wtmProf})

    #     #combine new with historical data:
    #     priceViolinList = HistPriceViolinList + newPriceViolinList
    #     columnStrList = HistColumnStrList + newColumnStrList


    #     #make colored violin plots
    #     rcParams['figure.figsize'] = 14, 6
    #     if zoom=='96':
    #         bw = 0.01
    #         inner = 'stick'
    #     else:
    #         bw=0.07
    #         inner = 'box'
    #     # fig = plt.figure(figsize=(14, 6))
    #     fig2 = sns_violinplot(x=columnStrList, y=priceViolinList, inner=inner, gridsize=500, color='#0485d1',
    #                 bw=bw, kernel='gau', scale='width') 
    #                 #x=overLimitViolinList, $"box", "quartile", "point", "stick"
    #                 #bw=0.2, kernel='gau', cut=0
    #                 #make scale area, width, or count, area is more skinny so going with that for now
    #                     #now not using scale since there are so many plots
    #                 #color: https://xkcd.com/color/rgb/
    #     plt.title('Order Speeds Over Time vs Profitability Line')
    #     plt.ylabel('Order Price')
    #     plt.xticks(rotation=20)
    #     if zoom == '96':
    #         # plt.ylim(2.75, 3.0)
    #         plt.ylim(wtmProf*0.95, wtmProf*0.97) #.94 and .985
    #     else:
    #         plt.ylim(YLIM_LOW, YLIM_HIGH) #2.6, 3.8

    #     #draw profitability lines
    #     wtmProfList = []
    #     for dictEl in self.pastDataList:
    #         wtmProfList.append(dictEl['wtmProf'])
    #     assert len(self.pastDataList)==len(wtmProfList), 'Error: plot.py found mismatch in list lengths'
    #     x = range(len(wtmProfList))
    #     if len(wtmProfList) == 1:
    #         #make line appear on first plot
    #         wtmProfList.append(wtmProfList[0])
    #         x = [-1, 1]
    #     profLess2 = []
    #     profLess4 = []
    #     for value in wtmProfList:
    #         profLess2.append(value*0.98)
    #         profLess4.append(value*0.96)
    #     plt.plot(x, wtmProfList, color='r', linestyle='-', zorder=0)
    #     plt.plot(x, profLess2, color='r', linestyle='-.', zorder=0)
    #     plt.plot(x, profLess4, color='r', linestyle='-.', zorder=0)

    #     if dispPlot:
    #         #plot on screen, blocks main thread
            
    #         plt.show()
    #         # saveDir = ut.pth('', 'rel1')
    #         if self.subFolder:
    #             figSaved = plt.savefig(ut.gpth(f"/datalogs/plots/{self.subFolder}/TEST violin_plot.png", 'rel1'))
    #             # figSaved = plt.savefig(saveDir + f"/datalogs/plots/{self.subFolder}/TEST violin_plot.png")
    #         else:
    #             figSaved = plt.savefig(ut.gpth(f"/datalogs/plots/TEST violin_plot.png", 'rel1'))
    #             # figSaved = plt.savefig(saveDir + f"/datalogs/plots/TEST violin_plot.png")
    #         # exit()
    #         # plt.clf() #created a bug
    #         # plt.close(fig)
    #         plt.clf()
    #         plt.close(figSaved)
    #         figStillOpen = plt.gcf()
    #         plt.clf()
    #         plt.close(figStillOpen) 
    #     else:
    #         #plot to file, nonblocking
    #         humReadDate, humReadTime, dateObj = ut.humTimeAndObj()
    #         # saveDir = ut.pth('', 'rel1')
    #         if self.livePlotter:
    #             if zoom==None and self.subFolder==None:
    #                 # saveDir += f'/datalogs/plots/live/{plotTime}.png'
    #                 saveDir = ut.gpth(f'/datalogs/plots/live/{plotTime}.png', 'rel1')
    #             else:
    #                 # saveDir += f'/datalogs/plots/live/{self.subFolder} {plotTime}.png'
    #                 saveDir = ut.gpth(f'/datalogs/plots/live/{self.subFolder} {plotTime}.png', 'rel1')
    #         elif self.subFolder is None:
    #             # saveDir += f"/datalogs/plots/{humReadDate} {humReadTime.replace(':', '-')} violin_plot.png"
    #             saveDir = ut.gpth(f"/datalogs/plots/{humReadDate} {humReadTime.replace(':', '-')} violin_plot.png", 'rel1')
    #         else:
    #             # saveDir += f"/datalogs/plots/{self.subFolder}/{humReadDate} {humReadTime.replace(':', '-')} violin_plot.png"
    #             saveDir = ut.gpth(f"/datalogs/plots/{self.subFolder}/{humReadDate} {humReadTime.replace(':', '-')} violin_plot.png", 'rel1')
    #         figSaved = plt.savefig(saveDir)

    #         plt.clf()
    #         plt.close()

        
    #     #fix historical record length
    #     if zoom == '96':
    #         dispLength = 5
    #     else:
    #         dispLength = 20
    #     while len(self.pastDataList) > dispLength - 1:
    #         self.pastDataList.pop(0)