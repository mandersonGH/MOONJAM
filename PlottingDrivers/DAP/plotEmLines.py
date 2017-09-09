'''
Created on Sep 8, 2017

@author: Mande
'''
import numpy as np
import GalaxyObject.fitsExtraction as fE
import dataCorrection as dC
import PlottingTools.plotFuncs as pF
from EmissionLine import EmissionLineSlice


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


def plotEmLines(EADir, galaxy, plotType, emLineInd, emLineFancy, nFP, dataInd):

    units = '$' + galaxy.myHDU[dataInd].header['BUNIT'] + '$'
#     galaxy.myHDU.info()
#     for j in galaxy.myHDU[dataInd].header.keys():
#         print(str(j) + "  ::   " + str(galaxy.myHDU[dataInd].header[j]))
#     #galaxy.printInfo()

    # cycle through 11 chosen wavelengths
    for j in emLineInd.keys():
        # print(lineType + ": " + j)

        newFileName = galaxy.PLATEIFU + '_' + plotType + \
            '_' + j

        plotTitle = galaxy.PLATEIFU + ' :: ' + \
            plotType + ' :: ' + emLineFancy[j]

        slice = EmissionLineSlice.EmissionLineSlice()
        slice.setName(emLineInd[j])
        slice.setFancyName(emLineFancy[j])
        slice.setData(galaxy.myDataCube[emLineInd[j]])
        slice.setError(galaxy.myErrorCube[emLineInd[j]])
        slice.setMask(galaxy.myMaskCube[emLineInd[j]])
        slice.setUnits(units)

        ############ data Correction #############

        # dC.printDataInfo(dataMat)

        vmax, vmin = pickBoundsForColorBar(slice)
#         print(jello)
        pF.plotQuadPlot(EADir,
                        galaxy,
                        nFP,
                        dataInd,
                        slice,
                        newFileName,
                        plotTitle,
                        vmax=vmax,
                        vmin=vmin)
