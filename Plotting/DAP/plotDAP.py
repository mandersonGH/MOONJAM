'''
Created on Sep 8, 2017

@author: Mande
'''

from Plotting.PlotterABC import PlotterABC
from Plotting.DAP.defaultCubePlots import defaultCubePlots
from Plotting.DAP.LOGCUBE_Plots import LOGCUBE_Plots


class plotter_DAP(PlotterABC):
    
    potentialDefaultCubePlots = ['emlines_gflux', 'emlines_ew', 'whan', 'bpt']


    def __init__(self, mplNum):
        self.DAPtype = mplNum
        
    
    def plot(self, EADir, galaxy, plotType):   
        galaxy.setCenterType('GAL')
        galaxy.pullRe(EADir, self.DAPtype)
        if plotType in self.potentialDefaultCubePlots:
            defaultCubePlots(EADir, galaxy , plotType, self.DAPtype)
        else:
            LOGCUBE_Plots(EADir, galaxy , plotType, self.DAPtype)
