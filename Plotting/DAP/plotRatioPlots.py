'''
Created on Sep 8, 2017

@author: Mande
'''

import numpy as np
from EmissionLine.EmissionLineSlice import EmissionLineSlice
np.seterr(divide='ignore', invalid='ignore')

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mclr

import plottingTools as pT
import plotFuncs as pF
import helperFuncs as hF
import drawOnPlots as dOP


def plotRatioPlots(EADir, galaxy, plotType, emLineInd, emLineFancy, nFP):
    dataInd = 1
    units = 'Some units'

    xValues, yValues, disValues, labelMat, mask, labels, counts = extractData(
        galaxy.myHDU, plotType, galaxy.Re, emLineInd, dataInd)

    slice = EmissionLineSlice()
    slice.setData(labelMat)
    slice.setMask(mask)

#     print(counts)
#     if plotType == "BPT":
#         labelVec = ['SF', 'Sy', 'Inter']
#     elif plotType == 'WHAN':
#         labelVec = ['SF', 'AGN', 'old stars']
#     print(plate_IFU)
#     for i in range(len(labelVec)):
#         print(labelVec[i] + ":  " + str(round(counts[i + 1] / counts[0] * 100, 2)) + '%')

    hex_at_Cen, gal_at_Cen = pT.getCenters(
        galaxy.myHDU, galaxy.PLATEIFU, dataInd)

    vmax = np.amax(labelMat)
    vmin = np.amin(labelMat)
    if vmin == 0:
        vmin = 1
    aspectRatio = 29.0 / 8
    height = 8
    fig = plt.figure(figsize=(height * aspectRatio, height))
    # plt.suptitle(plotType + ' Analysis :: ' + plate_IFU, fontsize=17)

    axes1 = plt.subplot(1, 3, 1)
    pF.opticalImage(EADir, galaxy, dataInd, axes1)

    axes2 = plt.subplot(1, 3, 2)
    ratioAxes(plotType, emLineFancy, xValues,
              yValues, disValues, labels, axes2)

    axes3 = plt.subplot(1, 3, 3)
    pF.spatiallyResolvedPlot(galaxy, plotType, plotType, dataInd,
                             slice, hex_at_Cen, gal_at_Cen, vmax, vmin, axes3)
    dOP.addReCircles(axes3)
    fig.tight_layout()
    # plt.show()
    # print(jello)
    plt.savefig(nFP + galaxy.PLATEIFU + '_' +
                plotType + '.png', bbox_inches='tight')
    # print(jello)
    plt.close()


def extractData(hdu, plotType, Re, emLineInd, dataInd):
    DAPtype = 'mpl5'
    if str(hdu[0].header['VERSDRP2']) == 'v1_5_0':
        DAPtype = 'mpl4'
    xTopArray, yTopArray, xBotArray, yBotArray = getAllIndices(hdu, plotType)

    dMat = pT.createDistanceMatrix(hdu, Re, 'EMLINE_GFLUX')

    xData = calculate_AxisMats(
        hdu, emLineInd, xTopArray[0], xBotArray[0], xTopArray[1], xBotArray[1], 'data')
    xMask = calculate_AxisMats(
        hdu, emLineInd, xTopArray[0], xBotArray[0], xTopArray[3], xBotArray[3], 'mask')

    yData = calculate_AxisMats(
        hdu, emLineInd, yTopArray[0], yBotArray[0], yTopArray[1], yBotArray[1], 'data')
    yMask = calculate_AxisMats(
        hdu, emLineInd, yTopArray[0], yBotArray[0], yTopArray[3], yBotArray[3], 'mask')

    # xMask = xMask / 1000
    # yMask = yMask / 1000

    if DAPtype == 'mpl4':
        mask = xMask + yMask
    else:
        mask = np.zeros(xMask.shape)
        mask[xMask < 0] = 1
        mask[yMask < 0] = 1

    # mask[mask < 0] = 1
    # yMask[yMask < 0] = 200
    # xMask[xMask < 0] = 200
    # yMask[yMask > 27] = 200
    # xMask[xMask > 27] = 200

    # plt.figure()
    # axes1 = plt.subplot(1, 3, 1)
    # plt.imshow(xMask)
    # plt.colorbar()
    # axes2 = plt.subplot(1, 3, 2)
    # plt.imshow(yMask)
    # plt.colorbar()
    # axes3 = plt.subplot(1, 3, 3)
    # plt.imshow(mask)
    # plt.colorbar()
    # plt.show()
    # print(jello)

    mask[np.isnan(xData)] = 1
    mask[np.isnan(yData)] = 1

    if plotType.startswith('BPT') or plotType == 'WHAN':
        xData = np.log10(xData)
        yData = np.log10(yData)

    xValues, yValues, disValues, labelMat, counts = processRatioData(
        plotType, xData, yData, dMat, mask)
    # mask[labelMat == 2] = 1
    # mask[labelMat == 3] = 1
    mask[labelMat == 0] = 1

    labels = [xTopArray[0], yTopArray[0], xBotArray[0], yBotArray[0]]

    return xValues, yValues, disValues, labelMat, mask, labels, counts


def getAllIndices(hdu, plotType):
    DAPtype = 'mpl5'
    if str(hdu[0].header['VERSDRP2']) == 'v1_5_0':
        DAPtype = 'mpl4'

    if plotType == 'WHAN':
        xTop = 'NII-6549'
        xTopDataInd = 'EMLINE_GFLUX'
        xTopErrInd = 'EMLINE_GFLUX_IVAR'
        xTopMaskInd = hdu['EMLINE_GFLUX'].header['QUALDATA']

        xBot = 'Ha-6564'
        xBotDataInd = 'EMLINE_GFLUX'
        xBotErrInd = 'EMLINE_GFLUX_IVAR'
        xBotMaskInd = hdu['EMLINE_GFLUX'].header['QUALDATA']

        yTop = 'Ha-6564'
        yTopDataInd = 'EMLINE_SEW'
        yTopErrInd = 'EMLINE_SEW_IVAR'
        yTopMaskInd = 'EMLINE_SEW_MASK'
        if DAPtype == 'mpl4':
            yTopDataInd = 'EMLINE_EW'
            yTopErrInd = 'EMLINE_EW_IVAR'
            yTopMaskInd = 'EMLINE_EW_MASK'

        yBot = None
        yBotDataInd = None
        yBotErrInd = None
        yBotMaskInd = None

    elif plotType.startswith('BPT'):

        if plotType == 'BPT' or plotType.endswith('[NII]'):
            xTop = 'NII-6549'
            xTopDataInd = 'EMLINE_GFLUX'
            xTopErrInd = 'EMLINE_GFLUX_IVAR'
            xTopMaskInd = hdu['EMLINE_GFLUX'].header['QUALDATA']

        elif plotType.endswith('[SII]'):
            #### Not available in MPL4 #######
            xTop = 'SII-6718'
            xTopDataInd = 'EMLINE_GFLUX'
            xTopErrInd = 'EMLINE_GFLUX_IVAR'
            xTopMaskInd = hdu['EMLINE_GFLUX'].header['QUALDATA']

        xBot = 'Ha-6564'
        xBotDataInd = 'EMLINE_GFLUX'
        xBotErrInd = 'EMLINE_GFLUX_IVAR'
        xBotMaskInd = hdu['EMLINE_GFLUX'].header['QUALDATA']

        yTop = 'OIII-5008'
        yTopDataInd = 'EMLINE_GFLUX'
        yTopErrInd = 'EMLINE_GFLUX_IVAR'
        yTopMaskInd = hdu['EMLINE_GFLUX'].header['QUALDATA']

        yBot = 'Hb-4862'
        yBotDataInd = 'EMLINE_GFLUX'
        yBotErrInd = 'EMLINE_GFLUX_IVAR'
        yBotMaskInd = hdu['EMLINE_GFLUX'].header['QUALDATA']

    xTopArray = [xTop, xTopDataInd, xTopErrInd, xTopMaskInd]
    xBotArray = [xBot, xBotDataInd, xBotErrInd, xBotMaskInd]
    yTopArray = [yTop, yTopDataInd, yTopErrInd, yTopMaskInd]
    yBotArray = [yBot, yBotDataInd, yBotErrInd, yBotMaskInd]

    return xTopArray, yTopArray, xBotArray, yBotArray


def calculate_AxisMats(hdu, emLineInd, Top, Bot, TopMatInd, BotMatInd, Mat_type):
    TopMat = hdu[TopMatInd].data[emLineInd[Top]]

    if Bot is not None:
        BotMat = hdu[BotMatInd].data[emLineInd[Bot]]

        if Mat_type == 'data':
            Mat = np.divide(TopMat, BotMat)
        elif Mat_type == 'mask':
            Mat = TopMat + BotMat
    else:
        Mat = TopMat
    return Mat


def processRatioData(plotType, xMat, yMat, dMat, mask):
    x = []
    y = []
    d = []
    labelMat = np.zeros(xMat.shape)

    counts = np.zeros(4)

    for i in range(xMat.shape[0]):
        for j in range(xMat.shape[1]):
            if mask[i, j] == 0 and ~np.isnan(xMat[i, j]) and ~np.isnan(yMat[i, j]):
                if dMat[i, j] <= 4:
                    x.append(xMat[i, j])
                    y.append(yMat[i, j])
                    d.append(dMat[i, j])
                if plotType.startswith('BPT'):
                    lowerLineYval = (0.61 / (xMat[i, j] - 0.05) + 1.3)
                    upperLineYval = (0.61 / (xMat[i, j] - 0.47) + 1.19)
                    if yMat[i, j] < lowerLineYval and xMat[i, j] < 0.05:
                        # print((xMat[i, j], yMat[i, j], lowerLineYval))
                        labelMat[i, j] = 1
                    elif yMat[i, j] > upperLineYval:
                        labelMat[i, j] = 2
                    else:
                        labelMat[i, j] = 3
                elif plotType == 'WHAN':
                    if yMat[i, j] < .5:
                        # Old Stars
                        labelMat[i, j] = 3
                    elif xMat[i, j] < -.4:
                        labelMat[i, j] = 1
                    else:
                        labelMat[i, j] = 2
                if isinstance(labelMat[i, j], int):
                    counts[labelMat[i, j]] += 1
                counts[0] += 1

    return x, y, d, labelMat, counts


def ratioAxes(plotType, emLineFancy, x, y, d, labels, axes):
    cmap = mclr.ListedColormap(['olive', 'tomato', 'darkturquoise', 'purple'])
    plt.scatter(x, y, c=d, s=20, lw=0.25, cmap=cmap, vmin=0, vmax=4)
    cbar = plt.colorbar()
    cbar.set_label("$R/R_e$", fontsize=pF.fontsize, fontweight='bold')
    dip = .01
    cbar.set_ticks([1 - dip, 2 - dip, 3 - dip, 4])
    cbar.set_ticklabels(['1', '2', '3', '4'])
    cbar.ax.tick_params(labelsize=pF.fontsize - 5)

    xmin, xmax = axes.get_xlim()
    ymin, ymax = axes.get_ylim()

    if plotType.startswith('BPT'):
        limits = [-1.5, 1.0, -1.5, 2.0]
    elif plotType == 'WHAN':
        limits = [-1.5, 1.0, -1, 3]

    xmin, xmax, ymin, ymax = hF.ensureWideEnoughAxisRange(
        limits, [xmin, xmax, ymin, ymax], strict=True)

    if plotType.startswith('BPT'):
        # for demarkations
        x1 = []
        x2 = []
        y1 = []
        y2 = []
        c = np.linspace(xmin, 2, 100)

        for i in c:
            if(i < 0.05):
                x1.append(i)
                y1.append(0.61 / (i - 0.05) + 1.3)
            if(-1.2805 < i and i < .47):
                x2.append(i)
                y2.append(0.61 / (i - 0.47) + 1.19)
    elif plotType == 'WHAN':
        if ymax < 1:
            ymax = 1
        if ymin > 0:
            ymin = 0
        if xmax < 0:
            xmax = 1
        if xmin > -1:
            xmin = -1

        # demarkations
        x1 = [xmin, xmax]
        y1 = [.5, .5]
        x2 = [-.4, -.4]
        y2 = [.5, ymax]

    plt.title(plotType + " Diagram",
              fontsize=pF.fontsize + 5, fontweight='bold')
    xTopLbl = labels[0]
    yTopLbl = labels[1]
    xBotLbl = labels[2]
    yBotLbl = labels[3]

    if xBotLbl is None:
        xDivideByStr = ''
    else:
        xDivideByStr = '/' + emLineFancy[xBotLbl]

    if yBotLbl is None:
        yDivideByStr = ''
    else:
        yDivideByStr = '/' + emLineFancy[yBotLbl]

    plt.xlabel("log " + emLineFancy[xTopLbl] +
               xDivideByStr, fontsize=pF.fontsize)
    plt.ylabel("log " + emLineFancy[yTopLbl] +
               yDivideByStr, fontsize=pF.fontsize)

    annotationSize = 27

    if plotType.startswith('BPT'):
        axes.annotate('SF', xy=(0.1, 0.1), xytext=(0.1, 0.1), textcoords='axes fraction',
                      color='cornflowerblue', fontsize=annotationSize, weight='bold')
        axes.annotate('Sy', xy=(0.1, 0.85), xytext=(0.1, 0.85), textcoords='axes fraction',
                      color='orange', fontsize=annotationSize, weight='bold')

        y_lastAnno = ymin + (ymax - ymin) * 0.1
        x_lastAnno = x1[hF.findIndex(y1, y_lastAnno)] + 0.05
        axes.annotate('Inter', xy=(x_lastAnno, y_lastAnno),
                      color='yellowgreen', fontsize=annotationSize, weight='bold')
    elif plotType == 'WHAN':
        axes.annotate('SF', xy=(0.1, 0.9), xytext=(0.1, 0.9), textcoords='axes fraction',
                      color='cornflowerblue', fontsize=annotationSize, weight='bold')
        axes.annotate('AGN', xy=(0.75, 0.9), xytext=(0.75, 0.9), textcoords='axes fraction',
                      color='orange', fontsize=annotationSize, weight='bold')
        axes.annotate('old stars', xy=(0.05, 0.05), xytext=(0.05, 0.05), textcoords='axes fraction',
                      color='yellowgreen', fontsize=annotationSize, weight='bold')

    plt.plot(x1, y1, 'k', lw=2.5)
    plt.plot(x2, y2, '--k', lw=2.5)
    plt.xticks(fontsize=pF.fontsize)
    plt.yticks(fontsize=pF.fontsize)
    axes.set_xlim([xmin, xmax])
    axes.set_ylim([ymin, ymax])
