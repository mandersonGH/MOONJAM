'''
Created on Sep 8, 2017

@author: Mande
'''

from PlottingDrivers.DAP.plotReSpectra import plotReSpectra


def LOGCUBE_Plots(EADir, galaxy, plotType, DAPtype):
    galaxy.setCenterType('HEX')
    dataInd = 1
    dataCube = galaxy.myHDU[dataInd].data
    errCube = galaxy.myHDU[2].data
    maskCube = galaxy.myHDU[3].data
    waveVec = galaxy.myHDU[4].data

    if plotType == 'respectra':
        plotReSpectra(EADir, galaxy, DAPtype, plotType,
                      dataInd, dataCube, waveVec)
