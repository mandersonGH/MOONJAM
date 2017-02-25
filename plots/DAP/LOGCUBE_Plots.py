from plotReSpectra import plotReSpectra


def LOGCUBE_Plots(EADir, DAPtype, filepath, hdu, plotType, plate_IFU, Re, center):
    center = 'HEX'

    dataInd = 1
    dataCube = hdu[dataInd].data
    errCube = hdu[2].data
    maskCube = hdu[3].data
    waveVec = hdu[4].data

    if plotType == 'respectra':
        plotReSpectra(EADir, DAPtype, filepath, hdu, plotType, plate_IFU, Re, center, dataInd, dataCube, waveVec)
