'''
Created on Sep 8, 2017

@author: Mande
'''

from PlottingDrivers.PlotterABC import PlotterABC
from PlottingDrivers.DAP.defaultCubePlots import defaultCubePlots
from PlottingDrivers.DAP.LOGCUBE_Plots import LOGCUBE_Plots
import sys
import os


class plotter_DAP(PlotterABC):

    resourceFolder = os.path.abspath(
        os.path.join(__file__, "../../..")) + "/resources/"

    potentialDefaultCubePlots = eval(
        open(resourceFolder + "potentialDefaultCubePlots.txt").read())

    def __init__(self, mplNum):
        self.DAPtype = mplNum

    def plot(self, EADir, galaxy, plotType):
        galaxy.setCenterType('GAL')
        galaxy.pullRe(EADir, self.DAPtype)
        if plotType in self.potentialDefaultCubePlots:
            defaultCubePlots(EADir, galaxy, plotType, self.DAPtype)
        else:
            LOGCUBE_Plots(EADir, galaxy, plotType, self.DAPtype)
