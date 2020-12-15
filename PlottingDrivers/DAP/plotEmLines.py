'''
Created on Sep 8, 2017

@author: Mande
'''
import numpy as np
import matplotlib.pyplot as plt

import GalaxyObject.fitsExtraction as fE
import dataCorrection as dC
import PlottingTools.plotFuncs as pF
import Utilities.mathFuncs as mF
from EmissionLine import EmissionLineSlice

def plotEmLines(EADir, galaxy, plotType, emLineInd, emLineFancy, nFP, dataInd):

    units = '$' + galaxy.myHDU[dataInd].header['BUNIT'] + '$'
    # galaxy.printInfo()
    hex_at_Cen, gal_at_Cen = fE.getCenters(
        galaxy.myHDU, galaxy.PLATEIFU, dataInd)

    print("plotEmLines("+galaxy.PLATEIFU+")")

    # cycle through 11 chosen wavelengths
    for j in emLineInd.keys():
        # print(plotType + ": " + j)

        slice = EmissionLineSlice.EmissionLineSlice(galaxy, emLineInd[j], j, emLineFancy[j], units)

        ############ data Correction #############

        # dC.printDataInfo(dataMat)

        ############ action #############

        # average = get_average(galaxy, slice)
        # print(galaxy.PLATEIFU, slice.myName, average)

        actuallyPlot(EADir, galaxy, plotType, nFP, dataInd, slice)

def get_average(galaxy, slice):
    masked_data = np.ma.array(slice.myData, mask=slice.myMask)
    # masked_err = np.ma.array(slice.myError, mask=slice.myMask)
    average = np.mean(masked_data)
    return average


def actuallyPlot(EADir, galaxy, plotType, nFP, dataInd, slice):
    newFileName = galaxy.PLATEIFU + '_' + plotType + \
            '_' + slice.myName

    plotTitle = galaxy.PLATEIFU + ' :: ' + \
        plotType + ' :: ' + slice.myFancyName
    vmax, vmin = pickBoundsForColorBar(slice)
#         print(jello)
    # try:
    #     pF.plotQuadPlot(EADir,
    #                     galaxy,
    #                     nFP,
    #                     dataInd,
    #                     slice,
    #                     newFileName,
    #                     plotTitle,
    #                     vmax=vmax,
    #                     vmin=vmin)
    # except Exception as e:
    #     plt.close()
    #     print(e)
    #     pF.plotDuoPlot(EADir,
    #                    galaxy,
    #                    nFP,
    #                    dataInd,
    #                    slice,
    #                    newFileName,
    #                    plotTitle,
    #                    vmax=vmax,
    #                    vmin=vmin)
    pF.plotLonePlot(EADir,
                   galaxy,
                   nFP,
                   dataInd,
                   slice,
                   newFileName,
                   plotTitle,
                   vmax=vmax,
                   vmin=vmin)

def pickBoundsForColorBar(slice):
    try:
        if np.nanmin(slice.myData[slice.myMask == 0]) < 0:
            vmin = 0
        else:
            vmin = np.nanmin(slice.myData[slice.myMask == 0])
    except ValueError:
        vmin = 0
    devs = 3
    vmax = dC.pickVMAX(slice.myData[slice.myMask == 0], devs)
    if vmax > 10:
        vmax = 10
#         maxx = 0
#         for y in range(dataMat.shape[0]):
#             for x in range(dataMat.shape[1]):
#                 if maskMat[x, y] == 0 and dataMat[x, y] > maxx:
#                     tempDist = calculateDistance(x, y, gal[0], gal[1]) / Re
#                     if tempDist < 3.6:
#                         maxx = dataMat[x, y]
#                         maxInds = [x, y]
#
#
#
#         print(j + ": " + str(round( calculateDistance(maxInds[0], maxInds[1], gal[0], gal[1])/ Re, 2)) )
# set lower colormap value
# if typeStr is '':
#     vmin = 0
# else:
#     vmin = dC.pickVMIN(sliceMat, 1)
    return vmax, vmin
