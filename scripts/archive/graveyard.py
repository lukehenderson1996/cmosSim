#BUG: produce tSamples and vSamples list
        # for dataDict, intp in zip(self.dataList, self.interpolate):
        #     for v, t in zip(dataDict['v'], dataDict['t']):
        #         # t = self.dataList[0]['t'] #BUG
        #         # v = self.dataList[0]['v'] #BUG
        #         if not self.tSamples is None:
        #             assert t[-1] <= self.tSamples[-1]
        #         else:
        #             self.tSamples = np.linspace(t[0], (t[-1]-t[0])*1.10, 100)
        #         if intp:
        #             cl.red('int')
        #             vSamples = np.interp(self.tSamples, t, v)
        #         else:
        #             cl.red('not int')
        #             vSamples = np.zeros_like(self.tSamples)
        #             tPositions = [np.argmax(self.tSamples >= timeVal) for timeVal in t]
        #             tPositions.append(len(self.tSamples)) #will be an invalid index, but expecting later code to be [:endInd]
        #             assert len(t)==len(v) and len(t)+1==len(tPositions)
        #             #populate voltages
        #             for i in range(len(tPositions)-1):
        #                 startInd = tPositions[i]
        #                 endInd   = tPositions[i+1]
        #                 vSamples[startInd:endInd] = v[i]
        #     self.vSamplesList.append(vSamples)
        #     # dt.info(self.vSamplesList, 'self.vSamplesList')









#DEPRECATED
# import plot
# plotter = plot.PLOTTER()
# plotter.vgsPlot(x=vgArr, y=rdsArr, dispPlot=True)
# plotter.vgsPlot(x=vgArr, multiY=multiY, multiLabels=multiLabels, dispPlot=True)




# #DEPRECATED
# if self.chanType == 'n':
#     if vgs > self.vth: #avoid div by zero
#         return min(self.ROFF, 1/(self.ronCoef * (vgs-self.vth)**2))
#     else:
#         return self.ROFF
# else: #'p'
#     assert vgs <= 0
#     if vgs < self.vth: #avoid div by zero
#         return min(self.ROFF, 1/(self.ronCoef * (self.vth - vgs)**2)) 
#     else:
#         return self.ROFF