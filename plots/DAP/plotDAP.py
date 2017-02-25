import os
import sys

currentDirectory = os.path.dirname(os.path.abspath(__file__))
tempVec = currentDirectory.split('/')
del tempVec[-2:]
pythonDirectoryPathname = '/'.join(tempVec)
sys.path.append(pythonDirectoryPathname)

import direcFuncs as dF
import fitsExtraction as fE

from defaultCubePlots import defaultCubePlots
from LOGCUBE_Plots import LOGCUBE_Plots

potentialDefaultCubePlots = ['emlines_gflux', 'emlines_ew', 'whan', 'bpt']


def plotDAP(EADir, DAPtype, filepath, hdu, plotType):

    filename = dF.getFilename(filepath)    
    
    plate_IFU = fE.pullPLATEIFU(hdu[0].header, filename)
    
    Re = fE.getRe(EADir, DAPtype, plate_IFU)

    center = 'GAL'

    if plotType in potentialDefaultCubePlots:
        defaultCubePlots(EADir, DAPtype, hdu, plotType, plate_IFU, Re, center)
    else:
        LOGCUBE_Plots(EADir, DAPtype, filepath, hdu, plotType, plate_IFU, Re, center)
