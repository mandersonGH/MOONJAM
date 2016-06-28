from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import direcFuncs
import dataCorrection as dC
import plottingTools as pT


def plotD4000(filename):
    # open file
    hdu = fits.open(filename)

    # setup new directory for figure-saving
    nFP = direcFuncs.setupNewDir(filename, 'D4000', "")
    # setup title for figure and saving
    # temp.info()

    plate_IFU, SPAXD_vec = pT.pullGeneralInfo(hdu[0].header, filename)

    # temp.info()

    # extract dataCube and wavelength vector
    dataCube = hdu[1].data
    waveVec = hdu[4].data

    # from (~70, ~4000, ~70) to (~70, ~70, ~4000)
    dataCube = np.rollaxis(dataCube, 0, 3)

    # create empty ratio matrix of correct shape
    ratioMat = np.zeros([dataCube.shape[0], dataCube.shape[1]])

    # pick wavelength ranges to measure D4000 ratio
    botStart = pT.findIndex(waveVec, 3750)
    botEnd = pT.findIndex(waveVec, 3950)
    topStart = pT.findIndex(waveVec, 4050)
    topEnd = pT.findIndex(waveVec, 4250)

    # cycle through spaxels and find ratio
    for i in range(0, dataCube.shape[0]):
        for j in range(0, dataCube.shape[1]):
            topMean = np.mean(dataCube[i, j, topStart:topEnd])
            botMean = np.mean(dataCube[i, j, botStart:botEnd])
            ratioMat[i, j] = topMean / botMean
    ######### axis business ############

    x2, y2 = pT.createAxis(plate_IFU, hdu, 1, 'LOGCUBE')

    ########### plotting three different figures ############

    for i in range(0, 3):

        plt.figure()

        # plotHexagon.plotHexagon([(0, 0)], 105000, axes)

        ratioMat4Plot = np.array(ratioMat)

        if i == 2:
            ratioMat4Plot = dC.maskInvalidFlaggedVals(ratioMat4Plot)
            cmapD = colors.ListedColormap(['red', 'blue'])
            cmapD.set_bad('0.75')
            bounds = [0.5, 1.6, 3]
            norm = colors.BoundaryNorm(bounds, cmapD.N)
            plt.pcolormesh(x2, y2, ratioMat4Plot, cmap=cmapD, norm=norm)
        else:
            cmapD = plt.cm.plasma
            cmapD.set_bad('0.75')
            if i == 0:
                vmin = 0.5
                vmax = 3
                ratioMat4Plot = dC.maskInvalidFlaggedVals(ratioMat4Plot)

            elif i == 1:
                vmin = 0.75
                vmax = 1.6
                ratioMatSF = dC.flagHighValues(ratioMat4Plot, 1.6)
                ratioMat4Plot = dC.maskInvalidFlaggedVals(ratioMatSF)

            plt.pcolormesh(x2, y2, ratioMat4Plot, cmap=cmapD,
                           vmin=vmin, vmax=vmax)

        plt.colorbar()

        plt.axis([x2.min() - 1, x2.max() + 1, y2.min() - 1, y2.max() + 1])
        plt.xlabel("arcsec")
        plt.ylabel("arcsec")

        ############ cross hairs lines ###############

        plt.plot([x2.min(), x2.max()], [0, 0], 'k')
        plt.plot([0, 0], [y2.min(), y2.max()], 'k')

        # plt.suptitle("$D_n$" + "(4000)", fontsize=17)
        plt.title("$D_n$" + "(4000)", fontsize=17)
        plt.annotate("Plate-IFU: " + plate_IFU, xy=(
            x2.min() + len(x2) * 0.01, y2.min() + len(y2) * 0.01), size=10)

        plt.savefig(nFP + plate_IFU +
                    '_D4000_' + str(i) + '.png', bbox_inches='tight', dpi=100)

    # plt.show()
    plt.close('all')
