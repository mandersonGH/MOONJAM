from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import direcFuncs
import dataCorrection as dC
import plottingTools as pT


def plotD4000(filename):
    # open file
    temp = fits.open(filename)

    # setup new directory for figure-saving
    nFP = direcFuncs.setupNewDir(filename, 'D4000', "")
    # setup title for figure and saving
    mainTitle = (filename.split('/')[-1]).split('.fits')[0]
    newFileName = '-'.join(mainTitle.split('-')[1:3])

    # temp.info()

    fiberNo = int((str(temp[0].header[55]))[
                  :(str(temp[0].header[55])).find('0')])

    # extract dataCube and wavelength vector
    dataCube = temp[1].data
    waveVec = temp[4].data

    # from (~70, ~4000, ~70) to (~70, ~70, ~4000)
    dataCube = np.rollaxis(dataCube, 0, 3)

    # create empty ratio matrix of correct shape
    ratioMat = np.zeros([dataCube.shape[0], dataCube.shape[1]])

    # pick wavelength ranges to measure D4000 ratio
    indVec = findInds(waveVec)
    botStart = indVec[0]
    botEnd = indVec[1]
    topStart = indVec[2]
    topEnd = indVec[3]

    # cycle through spaxels and find ratio
    for i in range(0, dataCube.shape[0]):
        for j in range(0, dataCube.shape[1]):
            topMean = np.mean(dataCube[i, j, topStart:topEnd])
            botMean = np.mean(dataCube[i, j, botStart:botEnd])
            ratioMat[i, j] = topMean / botMean
    ######### axis business ############

    x2, y2 = pT.createAxis(fiberNo, temp[1].header, 'LOGCUBE')

    ########### plotting three different figures ############

    for i in range(0, 3):

        plt.figure()

        # plotHexagon.plotHexagon([(0, 0)], 105000, axes)

        ratioMat4Plot = np.array(ratioMat)

        if i == 2:
            ratioMat4Plot = dC.whiteFlaggedVals(ratioMat4Plot)
            cmapD = colors.ListedColormap(['red', 'blue'])
            bounds = [0.5, 1.6, 3]
            norm = colors.BoundaryNorm(bounds, cmapD.N)
            plt.pcolormesh(x2, y2, ratioMat4Plot, cmap=cmapD, norm=norm)
        else:
            cmapD = plt.cm.plasma
            cmapD.set_bad(alpha=0.0)
            if i == 0:
                vmin = 0.5
                vmax = 3
                ratioMat4Plot = dC.whiteFlaggedVals(ratioMat4Plot)

            elif i == 1:
                vmin = 0.75
                vmax = 1.6
                ratioMatSF = dC.flagHighValues(ratioMat4Plot, 1.6)
                ratioMat4Plot = dC.whiteFlaggedVals(ratioMatSF)

            plt.pcolormesh(x2, y2, ratioMat4Plot, cmap=cmapD,
                           vmin=vmin, vmax=vmax)

        plt.colorbar()

        plt.axis([x2.min(), x2.max(), y2.min(), y2.max()])
        plt.xlabel("arcsec")
        plt.ylabel("arcsec")

        ############ cross hairs lines ###############

        plt.plot([x2.min(), x2.max()], [0, 0], 'k')
        plt.plot([0, 0], [y2.min(), y2.max()], 'k')

        plt.suptitle(mainTitle + '_D4000', fontsize=17)

        plt.savefig(nFP + newFileName +
                    '_D4000_' + str(i) + '.png', bbox_inches='tight', dpi=100)

    # plt.show()
    plt.close('all')


def findInds(waveVec):

    botStart = np.argmin(abs(waveVec - 3750))
    botEnd = np.argmin(abs(waveVec - 3950))
    topStart = np.argmin(abs(waveVec - 4050))
    topEnd = np.argmin(abs(waveVec - 4250))

    return [botStart, botEnd, topStart, topEnd]
