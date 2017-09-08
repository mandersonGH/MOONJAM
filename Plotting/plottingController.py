'''
Created on Sep 8, 2017

@author: Mande
'''
from Plotting.DAP.plotDAP import plotter_DAP
from Plotting.PIPE3D.plotPIPE3D import plotter_PIPE3D

class plottingController(object):
    
    dictPIPE3Dfiles = {'sfh': 'p_e.rad_SFH_lum_Mass.fits',
                       '_____': 'p_e.Sigma_Mass.fits',
                       'requested': '.cube.fits',
                       'lum_fracs': 'SFH.cube.fits',
                       'stellpops': 'SSP.cube.fits',
                       'flux_elines': '.cube.fits',
                       'indices.cs': '.cube.fits',
                       'elines': 'ELINES.cube.fits'}

    dictMPL4files = {'bpt': 'default.fits',
                     'whan': 'default.fits',
                     'emlines_gflux': 'default.fits',
                     'emlines_ew': 'default.fits',
                     'respectra': 'LOGCUBE.fits'}
    
    dictMPL5files = {'bpt': 'MAPS-SPX-GAU-MILESHC.fits',
                     'whan': 'MAPS-SPX-GAU-MILESHC.fits',
                     'emlines_gflux': 'MAPS-SPX-GAU-MILESHC.fits',
                     'emlines_ew': 'MAPS-SPX-GAU-MILESHC.fits',
                     'respectra': 'LOGCUBE-SPX-GAU-MILESHC.fits'}


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
                plotters.append(plotter_DAP('mpl-4'))
            if 'mpl5' in self.myOpts and plotType in self.dictMPL5files.keys():
                plotters.append(plotter_DAP('mpl-5'))
            self.runPlotters(plotters, plotType)
            
    def runPlotters(self, plotters, plotType):
        for plotter in plotters:
            plotter.plot(self.myEADirectory, self.myGalaxy, plotType)
                
            
        
            
        