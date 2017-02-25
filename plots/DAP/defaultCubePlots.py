import numpy as np

from plotRatioPlots import plotRatioPlots
from plotEmLines import plotEmLines
import direcFuncs as dF


def defaultCubePlots(EADir, DAPtype, hdu, plotType, plate_IFU, Re, center):

    if '_' in plotType:
        plotType = plotType[plotType.index('_') + 1:]

    plotType = plotType.upper()
    if DAPtype == 'MPL-5' and plotType == 'EW':
        plotType = 'SEW'
    emLineInd, emLineFancy = initializeEmLineDict(hdu, plotType)

    ratioPlots = ['WHAN', 'BPT']
    if DAPtype == 'MPL-4':
        typesOfBPT = ['']
    elif DAPtype == 'MPL-5':
        typesOfBPT = ['[NII]', '[SII]']

    if plotType in ratioPlots:
        nFP = dF.assure_path_exists(EADir + '/' + DAPtype + '/PLOTS/DAP/' + plate_IFU + '/Ratio Plots/')
        if plotType == 'BPT':
            for typeOfBPT in typesOfBPT:
                plotRatioPlots(EADir, hdu, plotType + typeOfBPT, plate_IFU, Re, center, emLineInd, emLineFancy, nFP)
        else:
            plotRatioPlots(EADir, hdu, plotType, plate_IFU, Re, center, emLineInd, emLineFancy, nFP)
    else:
        nFP = dF.assure_path_exists(EADir + '/' + DAPtype + '/PLOTS/DAP/' + plate_IFU + '/' + plotType + '/')


        dataInd, errInd, maskInd = getHduIndices(hdu, plotType)

        dataCube = hdu[dataInd].data
        if plotType == 'GFLUX':
            errCube = np.sqrt(np.divide(1, (hdu[errInd].data * 64)))
        else:
            errCube = np.sqrt(np.divide(1, hdu[errInd].data))
        maskCube = hdu[maskInd].data

        plotEmLines(EADir, hdu, plotType, plate_IFU, Re, center, emLineInd, emLineFancy, nFP, dataInd, dataCube, errCube, maskCube)
        
    


def getHduIndices(hdu, plotType):
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
            newV = vVec[0] + '-' +  vVec[-1]

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
