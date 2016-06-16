from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import os
import sys


def plotD4000_LOGCUBE(filename):
    # open file
    temp = fits.open(filename)

    # setup new directory for figure-saving
    nFP = setupNewDir(filename)
    # setup title for figure and saving
    mainTitle = (filename.split('/')[-1]).split('.fits')[0]
    newFileName = '-'.join(mainTitle.split('-')[1:3])

    # temp.info()

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

    # all NaNs correspond to bad values and will not be shown
    # either outside of hexagon or 0 values
    ratioMat = elimNaNs(ratioMat)

    minVec = [0.5, 1]
    maxVec = [3, 1.6]

    for i in range(0, len(minVec) + 1):

        plt.figure()

        # cmap to white out invalid entries
        cmapD = plt.cm.jet
        cmapD.set_bad(alpha=0.0)

        if i <= len(minVec) - 1:
            # cmapD.set_over('0.75', 1)
            # cmapD.set_under('0.75', 1)
            plt.pcolormesh(ratioMat, cmap=cmapD,
                           vmin=minVec[i], vmax=maxVec[i])

        else:
            cmapD = colors.ListedColormap(['red', 'blue'])
            bounds = [0.5, 1.6, 3]
            norm = colors.BoundaryNorm(bounds, cmapD.N)
            plt.pcolormesh(ratioMat, cmap=cmapD, norm=norm)

        # plot

        # plt.pcolormesh(ratioMat, cmap=cmap,
        #                norm=colors.LogNorm(vmin=np.nanmin(ratioMat),
        #                                    vmax=np.nanmax(ratioMat)))

        # plt.xlabel('x')
        # plt.ylabel('y')
        # plt.grid(True)
        plt.colorbar()
        axes = plt.gca()
        axes.set_xlim([0, dataCube.shape[0]])
        axes.set_ylim([0, dataCube.shape[1]])

        plt.suptitle(mainTitle + '_D4000', fontsize=17)

        plt.savefig(nFP + newFileName +
                    '_D4000_' + str(i) + '.png', bbox_inches='tight', dpi=100)

    # plt.show()
    plt.close('all')


def elimNaNs(dataCube):
    # dataCube[dataCube <= 0] = np.NaN

    # print("   min " + str(np.nanmin(dataCube)))
    # print("   max " + str(np.nanmax(dataCube)))
    dataCube = np.ma.masked_invalid(dataCube)

    return dataCube


def findInds(waveVec):

    botStart = np.argmin(abs(waveVec - 3750))
    botEnd = np.argmin(abs(waveVec - 3950))
    topStart = np.argmin(abs(waveVec - 4050))
    topEnd = np.argmin(abs(waveVec - 4250))

    return [botStart, botEnd, topStart, topEnd]


def setupNewDir(filename):
    # ensures new folder
    # sets up folder path for new files
    # print(filename)
    fileLs = filename.split('/')
    # print(fileLs)
    del fileLs[-1]

    newFldrPath = '/'.join(fileLs) + '/Figures/D4000/'
    # print(newFldrPath)
    assure_path_exists(newFldrPath)

    return newFldrPath


def assure_path_exists(path):
    # from
    # https://justgagan.wordpress.com/2010/09/22/python-create-path-or-directories-if-not-exist/
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)
        print("New directory made {" + dir + "/}")
