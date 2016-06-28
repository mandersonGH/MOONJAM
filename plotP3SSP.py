import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from sys import argv
from matplotlib import rc
import dataCorrection as dC
import plottingTools as pT
import direcFuncs as dF
import string


def plotP3SSP(filename):
    temp = fits.open(filename)
    nFP = dF.setupNewDir(filename, 'PIPE3D_SSP', "")
    plate_IFU, SPAXD_vec = pT.pullGeneralInfo(temp[0].header, filename)

    x2, y2 = pT.createAxis(plate_IFU, temp, 0, 'PIPE3D_SSP')
    dataCube = temp[0].data

    typeDict = {}
    unitDict = {}
    descDict = {}
    fileDict = {}
    for j in range(0, len(temp[0].header.keys())):
        tempStr = temp[0].header.keys()[j].split("_")
        if tempStr[0] == "TYPE":
            typeDict[int(tempStr[1])] = temp[0].header[j]
        elif tempStr[0] == "DESC":
            descDict[int(tempStr[1])] = string.capwords(temp[0].header[j])
        elif tempStr[0] == "UNITS":
            unitDict[int(tempStr[1])] = temp[0].header[j]
        elif tempStr[0] == "FILE":
            fileDict[int(tempStr[1])] = temp[0].header[j]

    for i in range(0, dataCube.shape[0]):

        sliceMat = dC.flagOutsideZeros(dataCube[i])
        sliceMat = dC.flagHighValues(sliceMat, 10000)
        sliceMat = dC.flagOutlierValues(sliceMat, 10)
        v_max = dC.pickVMAX(sliceMat, 3)
        v_min = dC.pickVMIN(sliceMat, 3)
        sliceMat = dC.maskInvalidFlaggedVals(sliceMat)

        cmap1 = plt.cm.afmhot_r
        cmap1.set_bad('0.75')

        plt.figure()
        plt.pcolormesh(x2, y2, sliceMat, cmap=cmap1, vmin=v_min, vmax=v_max)
        plt.axis([x2.min() - 1, x2.max() + 1, y2.min() - 1, y2.max() + 1])
        plt.xlabel("arcsec")
        plt.ylabel("arcsec")
        cbar = plt.colorbar(cmap=cmap1)
        cbar.set_label(typeDict[i] + " :: " + unitDict[i])
        plt.title(descDict[i])
        # plt.plot([x2.min(), x2.max()], [0, 0], 'k')
        # plt.plot([0, 0], [y2.min(), y2.max()], 'k')

        ########### plateIFU annotiation ##############
        plt.annotate("Plate-IFU: " + plate_IFU, xy=(x2.min() +
                                                 len(x2) * 0.01, y2.min() + len(y2) * 0.01), size=10)

        plt.savefig(nFP + plate_IFU + "_" +
                    descDict[i] + '.png', bbox_inches='tight', dpi=100)
    # plt.show()
