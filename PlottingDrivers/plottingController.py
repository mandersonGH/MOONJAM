'''
Created on Sep 8, 2017

@author: Mande
'''
from PlottingDrivers.DAP.plotDAP import plotter_DAP
from PlottingDrivers.PIPE3D.plotPIPE3D import plotter_PIPE3D
import os


class plottingController(object):
    resourceFolder = os.path.abspath(
        os.path.join(__file__, "../..")) + "/resources/"
    dictMPL4files = eval(open(resourceFolder + "dictMPL4files.txt").read())
    dictMPL5files = eval(open(resourceFolder + "dictMPL5files.txt").read())
    dictPIPE3Dfiles = eval(open(resourceFolder + "dictPIPE3Dfiles.txt").read())

    def __init__(self, EADirectory, galaxy, plotsToBeCreated, opts):
        self.myEADirectory = EADirectory
        self.myGalaxy = galaxy
        self.myPlotsToBeCreated = plotsToBeCreated
        self.myOpts = opts

    def run(self):
        for plotType in self.myPlotsToBeCreated:
            plotters = []

            if plotType in self.dictPIPE3Dfiles.keys():
                plotters.append(plotter_PIPE3D())
            if 'mpl4' in self.myOpts and plotType in self.dictMPL4files.keys():
                plotters.append(plotter_DAP('MPL-4'))
            if 'mpl5' in self.myOpts and plotType in self.dictMPL5files.keys():
                plotters.append(plotter_DAP('MPL-5'))

            self.runPlotters(plotters, plotType)

    def runPlotters(self, plotters, plotType):
        for plotter in plotters:
            plotter.plot(self.myEADirectory, self.myGalaxy, plotType)
