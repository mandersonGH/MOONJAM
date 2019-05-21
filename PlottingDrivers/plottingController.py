'''
Created on Sep 8, 2017

@author: Mande
'''
from PlottingDrivers.DAP.plotDAP import plotter_DAP
from PlottingDrivers.PIPE3D.plotPIPE3D import plotter_PIPE3D
import os


class plottingController(object):
    resourceFolder = os.path.join(os.path.abspath(
        os.path.join(__file__, "..", "..")), "resources")

    dictMPL4files = eval(
        open(os.path.join(resourceFolder, "dictMPL4files.txt")).read())
    dictMPL5files = eval(
        open(os.path.join(resourceFolder, "dictMPL5files.txt")).read())
    dictPIPE3Dfiles = eval(
        open(os.path.join(resourceFolder, "dictPIPE3Dfiles.txt")).read())

    def __init__(self, EADirectory, galaxy, plotsToBeCreated, data_versions):
        self.myEADirectory = EADirectory
        self.myGalaxy = galaxy
        self.myPlotsToBeCreated = plotsToBeCreated
        self.data_versions = data_versions

    def run(self):
        for plotType in self.myPlotsToBeCreated:
            plotters = []

            if plotType in self.dictPIPE3Dfiles.keys():
                if 'mpl4' in self.data_versions:
                    plotters.append(plotter_PIPE3D('MPL-4'))
                if 'mpl5' in self.data_versions:
                    plotters.append(plotter_PIPE3D('MPL-5'))
            if 'mpl4' in self.data_versions and plotType in self.dictMPL4files.keys():
                plotters.append(plotter_DAP('MPL-4'))
            if 'mpl5' in self.data_versions and plotType in self.dictMPL5files.keys():
                plotters.append(plotter_DAP('MPL-5'))

            self.runPlotters(plotters, plotType)

    def runPlotters(self, plotters, plotType):
        for plotter in plotters:
            plotter.plot(self.myEADirectory, self.myGalaxy, plotType)
