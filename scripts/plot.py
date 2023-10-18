'''plot.py: Plots data using seaborn and matplotlib'''

# Author: Luke Henderson
__version__ = '1.2'

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
    "fuchsia",
    "#FF0000", "#FF5E00", "#FFBC00", "#FFEB00", "#C7FF00", "#7CFF00", "#32FF00", "#00FF65", "#00FFCA", "#00C2FF",
    "#0056FF", "#0900FF", "#5600FF", "#A300FF", "#E100FF", "#FF00D4", "#FF008A", "#FF003F", "#FF2A00", "#FF7100",
    "#FFB800", "#FFE000", "#D1FF00", "#86FF00", "#3BFF00", "#00FF4B", "#00FFB0", "#009CFF", "#0030FF", "#2200FF",
    "#7100FF", "#BF00FF", "#FF00EA", "#FF00AF", "#FF0064", "#FF0019", "#FF4500", "#FF9C00", "#FFD300", "#DCFF00",
    "#91FF00", "#45FF00", "#00FF30", "#00FF96", "#0086FF", "#001BFF", "#3B00FF", "#8C00FF", "#DE00FF", "#FF00FF",
    "#FF0075", "#FF003A", "#FF6100", "#FFC700", "#FFF200", "#E6FF00", "#9BFF00", "#50FF00", "#00FF16", "#00FF7D",
    "#0070FF", "#0005FF", "#5300FF", "#A800FF", "#FC00FF", "#FF0015", "#FF0050", "#FF7D00", "#FFD100", "#FFF700",
    "#F0FF00", "#A6FF00", "#5BFF00", "#00FF00", "#00FF64", "#0064FF", "#0000EF", "#6B00FF", "#C400FF", "#F900FF",
    "#FF002A", "#FF0064", "#FF9900", "#FFE600", "#FDFD00", "#FBFF00", "#B0FF00", "#66FF00", "#00FFEB", "#0049FF",
    "#0000A9", "#8300FF", "#D900FF", "#FF00BF", "#FF003F", "#FF5800", "#FFB200", "#FFF400", "#F6FF00", "#9FFF00"]

#version with red as second option
PLOT_COLORS = [
    "g",  # green
    "r",  # red
    "b",  # blue
    "c",  # cyan
    "m",  # magenta
    "y",  # yellow
    "k",  # black
    "#FFA07A",  # light salmon
    "#8A2BE2",  # blue violet
    "lime",
    "teal",
    "navy",
    "fuchsia",
    "#FF0000", "#FF5E00", "#FFBC00", "#FFEB00", "#C7FF00", "#7CFF00", "#32FF00", "#00FF65", "#00FFCA", "#00C2FF",
    "#0056FF", "#0900FF", "#5600FF", "#A300FF", "#E100FF", "#FF00D4", "#FF008A", "#FF003F", "#FF2A00", "#FF7100",
    "#FFB800", "#FFE000", "#D1FF00", "#86FF00", "#3BFF00", "#00FF4B", "#00FFB0", "#009CFF", "#0030FF", "#2200FF",
    "#7100FF", "#BF00FF", "#FF00EA", "#FF00AF", "#FF0064", "#FF0019", "#FF4500", "#FF9C00", "#FFD300", "#DCFF00",
    "#91FF00", "#45FF00", "#00FF30", "#00FF96", "#0086FF", "#001BFF", "#3B00FF", "#8C00FF", "#DE00FF", "#FF00FF",
    "#FF0075", "#FF003A", "#FF6100", "#FFC700", "#FFF200", "#E6FF00", "#9BFF00", "#50FF00", "#00FF16", "#00FF7D",
    "#0070FF", "#0005FF", "#5300FF", "#A800FF", "#FC00FF", "#FF0015", "#FF0050", "#FF7D00", "#FFD100", "#FFF700",
    "#F0FF00", "#A6FF00", "#5BFF00", "#00FF00", "#00FF64", "#0064FF", "#0000EF", "#6B00FF", "#C400FF", "#F900FF",
    "#FF002A", "#FF0064", "#FF9900", "#FFE600", "#FDFD00", "#FBFF00", "#B0FF00", "#66FF00", "#00FFEB", "#0049FF",
    "#0000A9", "#8300FF", "#D900FF", "#FF00BF", "#FF003F", "#FF5800", "#FFB200", "#FFF400", "#F6FF00", "#9FFF00"]

if cfg.plotEn:
    # from seaborn import violinplot as sns_violinplot #this import takes about 1 second
    from seaborn import scatterplot as sns_scatterplot
    from seaborn import lineplot as sns_lineplot
    from seaborn import histplot as sns_histplot
    import matplotlib.pyplot as plt
    from matplotlib import rcParams
    from matplotlib.ticker import EngFormatter
    import matplotlib
    # matplotlib.use('Agg')  # use the Agg backend (NON GUI)

class PLOTTER:
    '''Plotter class'''

    def __init__(self, subFolder=None):
        '''Creates plots\n
        Args:
            subFolder [str, optional]: subfolder to store plots in
                format: 'myfolder' '''
        self.dataList = []
        self.subFolder = subFolder

    def genericPlot(self, x=None, y=None, multiY=None, multiLabels=None, title=None, xlabel=None, ylabel=None):
        '''Plots data\n
        Args:
            x [np.array]: \n
            y [np.array]: '''
 
        # x = np.array([2.1, 2.2, 2.3, 2.4, 2.5])
        # y = np.array([5.0, 5.0, 4.5, 2.5, 1.5])
        
        # plots
        rcParams['figure.figsize'] = 14, 6
        # fig = plt.figure(figsize=(14, 6))
        if multiY:
            assert len(multiY) == len(multiLabels)
            assert len(PLOT_COLORS) >= len(multiY)
            for item, label, color in zip(multiY, multiLabels, PLOT_COLORS ):
                fig2 = sns_lineplot(x=x, y=item, label=label, color=color, zorder=5, linewidth=1.5)
        else:
            fig2 = sns_lineplot(x=x, y=y, zorder=5, linewidth=1.5) #x='Vgs', y='Ron' 

        fig2.grid('True')
        # #log grid stuff
        # fig2.set_yscale('log')
        # plt.gca().xaxis.grid(True, which='major', linewidth=0.8, color='#656565')
        # plt.gca().yaxis.grid(True, which='major', linewidth=0.8, color='#656565')
        # plt.gca().yaxis.grid(True, which='minor', linestyle='--', linewidth=0.5)
        #optional labeling
        if title:
            plt.title(title)
        if xlabel:
            plt.xlabel(xlabel)
        if ylabel:
            plt.ylabel(ylabel)
        #custom xticks
        # plt.xticks(rotation=20)
        # plt.xticks([-6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6])
        #formatting
        # formatter = EngFormatter()
        # plt.gca().yaxis.set_major_formatter(formatter)
        if multiY:
            plt.legend() #ncol=5


        # #optional lines
        # assert not multiY
        # line1 = []
        # line2 = []
        # for item in x:
        #     line1.append(4)
        #     line2.append(8)
        # plt.plot(x, line2, color='r', linestyle='-', zorder=4, label='8 Ω')
        # plt.plot(x, line1, color='r', linestyle='-.', zorder=4, label='4 Ω')
        # plt.legend()


        #plot on screen, blocks main thread
        plt.show()
        figStillOpen = plt.gcf()
        plt.clf()
        plt.close(figStillOpen)

    def binPlot(self, x=None, kde=False, multiX=None, multiLabels=None, title=None, xlabel=None, ylabel=None, xLogPlot=False):
        '''Plots statistically binned data\n
        Args:
            x [np.array]: \n
            y [np.array]: '''
 
        # x = np.array([2.1, 2.2, 2.3, 2.4, 2.5])
        # y = np.array([5.0, 5.0, 4.5, 2.5, 1.5])
        
        # plots
        rcParams['figure.figsize'] = 14, 6

        if multiX:
            assert len(multiX) == len(multiLabels)
            assert len(PLOT_COLORS) >= len(multiX)
            for item, label, color in zip(multiX, multiLabels, PLOT_COLORS ):
                #orig
                # fig2 = sns_histplot(x=item, kde=kde, label=label, color=color)
                #new format
                fig2 = sns_histplot(x=item, label=label, color=color, stat="count", element="step", fill=False)
        else:
            #original
            # fig2 = sns_histplot(x=x, kde=kde) 
            #new format
            fig2 = sns_histplot(x=x, kde=False) #stat="count", element="step", fill=False

            #extra attempts
            # fig2 = sns_histplot(x=x, stat='density', fill=False, kde=kde) #element='line',
            # from seaborn import kdeplot as sns_kdeplot
            # fig2 = sns_kdeplot(data=x, common_norm=True, common_grid=True)

        fig2.set_yscale('log')
        # fig2.grid('True')
        plt.gca().xaxis.grid(True, which='major', linewidth=0.8, color='#656565')
        plt.gca().yaxis.grid(True, which='major', linewidth=0.8, color='#656565')
        plt.gca().yaxis.grid(True, which='minor', linestyle='--', linewidth=0.5)
        if title:
            plt.title(title)
        if xlabel:
            plt.xlabel(xlabel)
        if ylabel:
            plt.ylabel(ylabel)
        # plt.xticks(rotation=20)
        # plt.xticks([-6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6])
        formatter = EngFormatter()
        plt.gca().yaxis.set_major_formatter(formatter)
        if xLogPlot:
            plt.gca().xaxis.set_major_formatter(formatter)
        if multiX:
            plt.legend() #ncol=5

        #plot on screen, blocks main thread
        plt.show()
        figStillOpen = plt.gcf()
        plt.clf()
        plt.close(figStillOpen) 

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
            assert len(PLOT_COLORS) >= len(multiY)
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
        assert len(PLOT_COLORS) >= len(idVgsList)
        for curve, color, vgsLabel in zip(idVgsList, PLOT_COLORS, vgsLabels):
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

    def scopePlot(self, t=None, y=None, multiY=None, multiLabels=None, title=None, xlabel=None, ylabel=None, trellis=False):
        '''Plots voltage/timing data similar to an oscope \n
        Args:
            t [np.array]: \n
            y [np.array]: '''
        
        # plots
        rcParams['figure.figsize'] = 14, 6
        if trellis:
            fig2, axs = plt.subplots(len(multiY), 1, sharex=True)
            fig2.subplots_adjust(hspace=0)
            for ax, yVals, label in zip(axs, multiY, multiLabels):
                ax.plot(t, yVals, label=label, linewidth=1.5)
                ax.grid(True)
                ax.set_ylabel(label, rotation=0)
                ax.yaxis.labelpad = len(label)*5
                formatter = EngFormatter()
                ax.yaxis.set_major_formatter(formatter)
            
            # Set the title and x-label of the entire figure
            if title:
                fig2.suptitle(title)
            axs[-1].xaxis.set_major_formatter(formatter)
            if xlabel:
                axs[-1].set_xlabel(xlabel)
            
            
            # plt.show()
        else:
            if multiY:
                assert len(multiY) == len(multiLabels)
                assert len(PLOT_COLORS) >= len(multiY)
                for item, label, color in zip(multiY, multiLabels, PLOT_COLORS ):
                    fig2 = sns_lineplot(x=t, y=item, label=label, color=color, zorder=5, linewidth=1.5)
            else:
                fig2 = sns_lineplot(x=t, y=y, zorder=5, linewidth=1.5) #x='Vgs', y='Ron' 

            fig2.grid('True')
            # plt.gca().xaxis.grid(True, which='major', linewidth=0.8, color='#656565')
            # plt.gca().yaxis.grid(True, which='major', linewidth=0.8, color='#656565')
            # plt.gca().yaxis.grid(True, which='minor', linestyle='--', linewidth=0.5)
            #optional labeling
            if title:
                plt.title(title)
            if xlabel:
                plt.xlabel(xlabel)
            if ylabel:
                plt.ylabel(ylabel)
            #custom xticks
            # plt.xticks(rotation=20)
            # plt.xticks([-6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6])
            #formatting
            formatter = EngFormatter()
            plt.gca().xaxis.set_major_formatter(formatter)
            if multiY:
                plt.legend() #ncol=5

        # #optional lines
        # assert not multiY
        # line1 = []
        # line2 = []
        # for item in x:
        #     line1.append(4)
        #     line2.append(8)
        # plt.plot(x, line2, color='r', linestyle='-', zorder=4, label='8 Ω')
        # plt.plot(x, line1, color='r', linestyle='-.', zorder=4, label='4 Ω')
        # plt.legend()

        #plot on screen, blocks main thread
        plt.show()
        figStillOpen = plt.gcf()
        plt.clf()
        plt.close(figStillOpen)

    def scopeTrellisPlot(self, t=None, y=None, multiY=None, multiLabels=None, title=None, xlabel=None, ylabel=None):
        """Generates a trellis plot using numpy and matplotlib.
        Args:
        - t [np.array]: Time values
        - multiY [list of np.array]: List of y-values
        - multiLabels [list of str]: Names for the y-values
        - title [str]: Plot title
        """
        num_plots = len(multiY)
        
        # Create subplots
        fig, axs = plt.subplots(num_plots, 1, sharex=True, figsize=(14, 6 * num_plots))
        
        # Ensure axs is a list even if there's only one subplot
        if num_plots == 1:
            axs = [axs]
        
        fig.subplots_adjust(hspace=0)
        
        # Plot each dataset
        for ax, y_vals, label in zip(axs, multiY, multiLabels):
            ax.plot(t, y_vals, label=label, linewidth=1.5, color='r')
            # ax.legend()
            ax.grid(True)
            ax.set_ylabel(label)
            formatter = EngFormatter()
            ax.xaxis.set_major_formatter(formatter)
        
        # Set the title and x-label of the entire figure
        if title:
            fig.suptitle(title)
        axs[-1].set_xlabel('Time')
        
        plt.show()


class OSCOPE:
    '''Oscope class'''

    def __init__(self):
        '''Creates oscilloscope plots over a period of time\n
        Notes:
            dataList [list of dict]: input data (small number of samples where information is changing)
                dict format: {'v': voltage list, t: timing list, 'intp': interpolation bool}
                    whether to use linear interpolation (True) \n
                    or to merely extend the values (False)
            tSamples [numpy array]: time samples (large number of linspace values)
            vSamplesList [list of numpy array]: voltage samples (large number)'''
        self.dataList = []
        self.tSamples = None
        self.vSamplesList = []
        self.plotter = PLOTTER()
    
    def plot(self, multiLabels=None, title=None, xlabel=None, ylabel=None, trellis=False):
        NUM_SAMPLES = 10_000
        if isinstance(self.dataList, list):
            for item in self.dataList:
                if isinstance(item, dict):
                    pass
                else:
                    cl.red('Error: dataList must contain "dict" objects only')
                    dt.info(self.dataList, 'self.dataList')
                    exit()
        else:
            cl.red('Error: dataList must be of type "list"')
            dt.info(self.dataList, 'self.dataList')
            exit()

        #produce tSamples and vSamples list
        for dataDict in self.dataList:
            t = dataDict['t']
            v = dataDict['v']
            intp = dataDict['intp']
            if not self.tSamples is None:
                if t[-1] > self.tSamples[-1]:
                    self.tSamples = np.append(self.tSamples, t[-1])
                assert t[-1] <= self.tSamples[-1]
            else:
                self.tSamples = np.linspace(t[0], (t[-1]-t[0])*1.10, NUM_SAMPLES)
            if intp:
                vSamples = np.interp(self.tSamples, t, v)
            else:
                vSamples = np.zeros_like(self.tSamples)
                tPositions = [np.argmax(self.tSamples >= timeVal) for timeVal in t]
                tPositions.append(len(self.tSamples)) #will be an invalid index, but expecting later code to be [:endInd]
                assert len(t)==len(v) and len(t)+1==len(tPositions)
                #populate voltages
                for i in range(len(tPositions)-1):
                    startInd = tPositions[i]
                    endInd   = tPositions[i+1]
                    vSamples[startInd:endInd] = v[i]
            self.vSamplesList.append(vSamples)
        # dt.info(self.vSamplesList, 'self.vSamplesList')

        

        if len(self.vSamplesList) == 1:
            self.plotter.scopePlot(t=self.tSamples, y=self.vSamplesList[0], title='Oscope', xlabel='Time (s)')
        else:
            for i in range(len(self.vSamplesList)):
                while len(self.vSamplesList[i]) < len(self.tSamples):
                    self.vSamplesList[i] = np.append(self.vSamplesList[i], self.vSamplesList[i][-1])
            self.plotter.scopePlot(t=self.tSamples, multiY=self.vSamplesList, multiLabels=multiLabels, 
                                   title=title, xlabel=xlabel, ylabel=ylabel, trellis=trellis)
        # dt.info(tSamples, 'tPoints')
        # dt.info(tPositions, 'tPositions')
        # for i in range(len(vSamples)):
        #     print(vSamples[i])
        
        