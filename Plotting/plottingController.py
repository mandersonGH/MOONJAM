'''
Created on Sep 8, 2017

@author: Mande
'''
from Plotting.DAP.plotDAP import plotter_DAP
from Plotting.PIPE3D.plotPIPE3D import plotter_PIPE3D

class plottingController(object):
    
    dictMPL4files = eval(open("../resources/dictMPL4files.txt").read())
    dictMPL5files = eval(open("../resources/dictMPL5files.txt").read())
    dictPIPE3Dfiles = eval(open("../resources/dictPIPE3Dfiles.txt").read())


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
                
            
        
            
        