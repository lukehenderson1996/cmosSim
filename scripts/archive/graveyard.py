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