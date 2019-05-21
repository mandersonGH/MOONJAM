import numpy as np
from astropy.io import fits

from resources import EA_data
import Utilities.helperFuncs as hF
import Utilities.mathFuncs as mF
from GalaxyObject.fitsExtraction import *


def axisEndpoints(plate_IFU, Re, hex_at_Cen):
    if plate_IFU not in EA_data.dictMajMinAxis:
        return None
    endPoints = EA_data.dictMajMinAxis[plate_IFU]

    majX = [(float(endPoints[0][i][0] - hex_at_Cen[0]) / Re) for i in range(2)]
    majY = [(float(endPoints[0][i][1] - hex_at_Cen[1]) / Re) for i in range(2)]
    minX = [(float(endPoints[1][i][0] - hex_at_Cen[0]) / Re) for i in range(2)]
    minY = [(float(endPoints[1][i][1] - hex_at_Cen[1]) / Re) for i in range(2)]

    return majX, majY, minX, minY


def getTicks(gal_at_Cen, hex_at_Cen, extentVec, Re, center='GAL'):

    if center == 'GAL':
        hexGalShift = [float(gal_at_Cen[i] - hex_at_Cen[i]) /
                       Re for i in range(0, 2)]
    elif center == 'HEX':
        hexGalShift = [0, 0]

    xmin = np.round(extentVec[0] + hexGalShift[0])
    xmax = np.round(extentVec[1] + hexGalShift[0])
    ymin = np.round(extentVec[2] + hexGalShift[1])
    ymax = np.round(extentVec[3] + hexGalShift[1])

    xticks = [-2, 0, 2]
    yticks = [-2, 0, 2]

    highLim = [5, 10]
    for lim in highLim:
        if xmin < -lim:
            xticks = np.append(-lim, xticks)
        if xmax > lim:
            xticks = np.append(xticks, lim)
        if ymin < -lim:
            yticks = np.append(-lim, yticks)
        if ymax > lim:
            yticks = np.append(yticks, lim)

    return xticks, yticks


def low_high_Inds(distances, Re, ReMax):
    Flag = True
    lowInd = 0
    highInd = 0
    for i in range(len(distances)):
        if distances[i] / Re > -ReMax and Flag:
            lowInd = i
            Flag = False
        elif distances[i] / Re > ReMax:
            highInd = i
            break

    if highInd == 0:
        highInd = i

    return lowInd, highInd


def createExtentVec(plate_IFU, hdu, dataInd, Re, center='GAL'):
    NAXIS_vec = getNAXIS(hdu, dataInd)
    extentVec = [0, NAXIS_vec[0], 0, NAXIS_vec[1]]

    hex_at_Cen, gal_at_Cen = getCenters(hdu, plate_IFU, dataInd)

    if center == 'GAL':
        extentVec[0] -= gal_at_Cen[0]
        extentVec[1] -= gal_at_Cen[0]
        extentVec[2] -= gal_at_Cen[1]
        extentVec[3] -= gal_at_Cen[1]
    elif center == 'HEX':
        extentVec[0] -= hex_at_Cen[0]
        extentVec[1] -= hex_at_Cen[0]
        extentVec[2] -= hex_at_Cen[1]
        extentVec[3] -= hex_at_Cen[1]

    extentVec = [float(v) / Re for v in extentVec]

    return extentVec


def createDistanceMatrix(hdu, Re, dataInd):

    NAXIS_vec = getNAXIS(hdu, dataInd)

    if "CRPIX1" in hdu[dataInd].header.keys():
        refPnt = [hdu[dataInd].header["CRPIX1"], hdu[dataInd].header["CRPIX2"]]
    else:
        refPnt = [0, 0]

    SPAXD_vec = getSPAXD_vec(hdu)

    disMat = np.zeros(NAXIS_vec)

    x2 = refPnt[0]
    y2 = refPnt[1]

    for i in range(0, NAXIS_vec[0]):
        for j in range(0, NAXIS_vec[1]):
            disMat[i, j] = mF.calculateDistance(0, 0, (x2 - i), (y2 - j))
            disMat[i, j] = disMat[i, j] / Re

    return disMat


def getSPAXD_vec(hdu):
    if "SPAXDX" in hdu[0].header.keys():
        SPAXD_vec = [hdu[0].header['SPAXDX'], hdu[0].header['SPAXDY']]
    else:
        SPAXD_vec = [0.5, 0.5]

    return SPAXD_vec


def visualImageCropping(plate_IFU, shape):
    IFU = plate_IFU.split("-")[1]
    fiberNo = int(IFU[:IFU.find('0')])
    cropSize = EA_data.dictScaling[fiberNo]
    scaleVec = [0, 0, 0, 0]
    for i in range(len(shape)):
        scaleVec[i * 2] = cropSize
        scaleVec[i * 2 + 1] = shape[i] - cropSize
    return scaleVec


def centerVec(vec):
    meanShift = [np.mean(vec[:2]), np.mean(vec[2:])]
    vec[0] -= meanShift[0]
    vec[1] -= meanShift[0]
    vec[2] -= meanShift[1]
    vec[3] -= meanShift[1]
    return vec


def axisSkewGal(axes, gal_at_Cen, hex_at_Cen, Re, extentVec):
    hexGalShift = hF.calcHexGalShift(hex_at_Cen, gal_at_Cen, Re)
    # print(hexGalShift)
    badXlim = axes.get_xlim()
    badYlim = axes.get_ylim()
    if badXlim == (0.0, 1.0):
        badXlim = extentVec[:2]
    if badYlim == (0.0, 1.0):
        badYlim = extentVec[2:]

    x1 = badXlim[0] + hexGalShift[0]
    x2 = badXlim[1] + hexGalShift[0]
    y1 = badYlim[0] + hexGalShift[1]
    y2 = badYlim[1] + hexGalShift[1]
    return x1, x2, y1, y2


def major_minor_axis(plate_IFU, whichAxis, hex_at_Cen, gal_at_Cen, center='GAL'):
    # print(center)
    if center == 'GAL':
        refPnt = gal_at_Cen
    elif center == 'HEX':
        refPnt = hex_at_Cen

    axisCoord, m, b = getAxisLineProperties(
        plate_IFU, whichAxis, center, gal_at_Cen, hex_at_Cen)

    ## whether x or y has more values in the range ####
    if abs(m) <= 1:
        var_step = 0
    else:
        var_step = 1

    firstValue = axisCoord[0][var_step]
    lastValue = axisCoord[1][var_step]
    stepSize = 1 + np.abs(firstValue - lastValue)

    indexes = []
    for i in np.linspace(firstValue, lastValue, stepSize):
        if i == refPnt[var_step]:
            indexes.append([int(refPnt[0]), int(refPnt[1])])
        else:
            temp = [0, 0]
            temp[var_step] = int(i)
            if var_step == 0:
                temp[1] = int(round(i * m + b, 0))
            elif var_step == 1:
                temp[0] = int(round(float(i - b) / m, 0))
        indexes.append(temp)

    distances = []

    sign = -1
    for i in indexes:
        dist = sign * \
            np.abs(mF.calculateDistance(refPnt[0], refPnt[1], i[0], i[1]))

        # print(str(i) + " " + str(refPnt) + " " + str(dist))

        if dist == 0:
            sign = 1
        distances.append(dist)

    return distances, indexes


def getAxisLineProperties(plate_IFU, whichAxis, center, gal_at_Cen, hex_at_Cen):

    if whichAxis == 'major':
        ind = 0
    elif whichAxis == 'minor':
        ind = 1

    axisCoord = EA_data.dictMajMinAxis[plate_IFU][ind]
    # print("hey")
    # print(axisCoord)
    axisCoord2 = [[[0, 0], [0, 0]], [[0, 0], [0, 0]]]

    if center == 'GAL':
        for i in range(2):
            for j in range(2):
                axisCoord2[i][j] = axisCoord[i][
                    j] + gal_at_Cen[j] - hex_at_Cen[j]
    else:
        axisCoord2 = axisCoord
    # print(axisCoord2)

    m, b = mF.createLineEquation(axisCoord2)

    return axisCoord2, m, b
