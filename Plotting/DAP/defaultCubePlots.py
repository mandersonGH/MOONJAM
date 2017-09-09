'''
Created on Sep 8, 2017

@author: Mande
'''
import direcFuncs as dF
import numpy as np

from Plotting.DAP.plotEmLines import plotEmLines
from Plotting.DAP.plotRatioPlots import plotRatioPlots


def defaultCubePlots(EADir, galaxy, plotType, DAPtype):

    plotType = formatPlotType(plotType, DAPtype)
    emLineInd, emLineFancy = initializeEmLineDict(galaxy.myHDU, plotType)
    ratioPlots = eval(open("../resources/typesOfRatioPlots.txt").read())
    typesOfBPT = extractTypesOfBPT(DAPtype)

    if plotType in ratioPlots:
        nFP = dF.assure_path_exists(
            EADir + '/' + DAPtype + '/PLOTS/DAP/' + galaxy.PLATEIFU + '/Ratio Plots/')
        if plotType == 'BPT':
            for typeOfBPT in typesOfBPT:
                plotRatioPlots(EADir, galaxy, plotType +
                               typeOfBPT, emLineInd, emLineFancy, nFP)
        else:
            plotRatioPlots(EADir, galaxy, plotType,
                           emLineInd, emLineFancy, nFP)
    else:
        # non ratio plot
        nFP = dF.assure_path_exists(
            EADir + '/' + DAPtype + '/PLOTS/DAP/' + galaxy.PLATEIFU + '/' + plotType + '/')
        dataInd, errInd, maskInd = getHduIndices(plotType)
        galaxy.extractDataCubes(dataInd, errInd, maskInd)
        correctErrorCube(galaxy, plotType)
        plotEmLines(EADir, galaxy, plotType, emLineInd,
                    emLineFancy, nFP, dataInd)


def formatPlotType(plotType, DAPtype):
    if '_' in plotType:
        plotType = plotType[plotType.index('_') + 1:]
    plotType = plotType.upper()
    if DAPtype == 'MPL-5' and plotType == 'EW':
        plotType = 'SEW'
    return plotType


def extractTypesOfBPT(DAPtype):
    if DAPtype == 'MPL-4':
        typesOfBPT = ['']
    elif DAPtype == 'MPL-5':
        typesOfBPT = ['[NII]', '[SII]']
    return typesOfBPT


def correctErrorCube(galaxy, plotType):
    adjustmentScale = 1
    if plotType == 'GFLUX':
        adjustmentScale = 64
    galaxy.myErrorCube = np.sqrt(
        np.divide(1, (galaxy.myErrorCube * adjustmentScale)))


def getHduIndices(plotType):
    # if plotType == 'GFLUX':
    #     dataInd = 1
    #     errInd = 2
    #     maskInd = 3
    # elif plotType == 'EW':
    #     dataInd = 11
    #     errInd = 12
    #     maskInd = 13
    dataInd = 'EMLINE_' + plotType
    maskInd = 'EMLINE_' + plotType + '_MASK'
    errInd = 'EMLINE_' + plotType + '_IVAR'
    return dataInd, errInd, maskInd


def initializeEmLineDict(hdu, plotType):
    if plotType == 'WHAN' or plotType.startswith('BPT'):
        plotType = 'GFLUX'
    # Build a dictionary with the emission line names to ease selection
    emLineInd = {}
    emLineFancy = {}
    for k, v in hdu['EMLINE_' + plotType].header.items():
        if k[0] == 'C':
            try:
                i = int(k[1:]) - 1
            except ValueError:
                continue
            vVec = v.split("-")
            newV = vVec[0] + '-' + vVec[-1]

            emLineInd[newV] = i
            emLineFancy[newV] = reformatEmLineNames(v)

    return emLineInd, emLineFancy


def reformatEmLineNames(EmLineName):
    greekLet = ""
    tempVec = EmLineName.split('-')
    if EmLineName.startswith("H"):
        EmLineName = tempVec[0] + "_" + tempVec[-1]
        if EmLineName[1] == 'a':
            greekLet = '${\\alpha}$'
        elif EmLineName[1] == 'b':
            greekLet = '${\\beta}$'
        elif EmLineName[1] == 'c' or EmLineName[1:4] == 'gam':
            greekLet = '${\\gamma}$'
        elif EmLineName[1] == 'd' or EmLineName[1:4] == 'del':
            greekLet = '${\\delta}$'
        elif EmLineName[1:4] == 'eps':
            greekLet = '${\\epsilon}$'
        EmLineFancyName = "H" + greekLet + \
            " " + "${\\lambda}$" + tempVec[-1]
    else:
        EmLineFancyName = '[' + tempVec[0] + '] ' + \
            '${\\lambda}$' + tempVec[-1]

    return EmLineFancyName
