'''
Created on Sep 8, 2017

@author: Mande
'''
import numpy as np
import GalaxyObject.fitsExtraction as fE
import dataCorrection as dC
import plotFuncs as pF

def plotEmLines(EADir, galaxy, plotType, emLineInd, emLineFancy, nFP, dataInd, dataCube, errCube, maskCube):
    
    units = '$' + galaxy.myHDU[dataInd].header['BUNIT'] + '$'
    hex, gal = fE.getCenters(galaxy.myHDU, galaxy.PLATEIFU, dataInd)
    # cycle through 11 chosen wavelengths
    for j in emLineInd.keys():
        # print(lineType + ": " + j)

        newFileName = galaxy.PLATEIFU + '_' + plotType + \
            '_' + j

        plotTitle = galaxy.PLATEIFU + ' :: ' + plotType + ' :: ' + emLineFancy[j]

        dataMat = dataCube[emLineInd[j]]
        errMat = errCube[emLineInd[j]]
        maskMat = maskCube[emLineInd[j]]
        ############ data Correction #############

        # dC.printDataInfo(dataMat)

        if np.nanmin(dataMat[maskMat == 0]) < 0:
            vmin = 0
        else:
            vmin = np.nanmin(dataMat[maskMat == 0])

        devs = 3

        vmax = dC.pickVMAX(dataMat[maskMat == 0], devs)

        if vmax > 10:
            vmax = 10
            
#         maxx = 0
#         for y in range(dataMat.shape[0]):
#             for x in range(dataMat.shape[1]):
#                 if maskMat[x, y] == 0 and dataMat[x, y] > maxx:
#                     tempDist = hF.calculateDistance(x, y, gal[0], gal[1]) / Re
#                     if tempDist < 3.6:
#                         maxx = dataMat[x, y]
#                         maxInds = [x, y]
#                     
#         
#         
#         print(j + ": " + str(round( hF.calculateDistance(maxInds[0], maxInds[1], gal[0], gal[1])/ Re, 2)) )

        # set lower colormap value
        # if typeStr is '':
        #     vmin = 0
        # else:
        #     vmin = dC.pickVMIN(sliceMat, 1)

        pF.plotQuadPlot(EADir,
                        galaxy,
                        nFP,
                        dataInd,
                        dataMat,
                        errMat,
                        maskMat,
                        units,
                        newFileName,
                        plotTitle,
                        vmax=vmax,
                        vmin=vmin)
