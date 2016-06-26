from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import direcFuncs
import dataCorrection as dC
import plottingTools as pT


def plotHDA(filename):
    # open file
    temp = fits.open(filename)

    # setup new directory for figure-saving
    nFP = direcFuncs.setupNewDir(filename, 'HDA', "")
    # setup title for figure and saving
    mainTitle = (filename.split('/')[-1]).split('.fits')[0]
    newFileName = '-'.join(mainTitle.split('-')[1:3])

    # temp.info()
    # for j in [0, 1]:
    #     print("")
    #     for i in range(0, len(temp[j].header.keys())):
    #         print(str(temp[j].header.keys()[i]) + " -- " + str(temp[j].header[i]))

    fiberNo = int((str(temp[0].header[55]))[
                  :(str(temp[0].header[55])).find('0')])

    # extract dataCube and wavelength vector
    dataCube = temp[1].data
    waveVec = temp[4].data

    # from (~70, ~4000, ~70) to (~70, ~70, ~4000)
    # dataCube = np.rollaxis(dataCube, 0, 3)

    # create empty ratio matrix of correct shape

    # pick wavelength ranges to measure D4000 ratio
    wavelength = 4101.75
    index = pT.findIndex(waveVec, wavelength)
    # print(index)
    # print(waveVec[index-3:index+3])
    # print(dataCube[index].shape)

    sliceMat = dataCube[index]

    sliceMat = dC.flagOutsideZeros(sliceMat)

    # sliceMat = dC.zeroOutNegatives(sliceMat)

    sliceMat = dC.maskInvalidFlaggedVals(sliceMat)

    ######### axis business ############

    x2, y2 = pT.createAxis(fiberNo, temp[1].header, 'LOGCUBE')

    ########### plotting three different figures ############

    plt.figure()
    axes = plt.subplot(1, 1, 1)

    cmapD = plt.cm.plasma
    cmapD.set_bad('0.75')

    plt.pcolormesh(x2, y2, sliceMat, cmap=cmapD)

    cbar = plt.colorbar()
    cbar.set_label(temp[1].header[19])

    plt.axis([x2.min() - 1, x2.max() + 1, y2.min() - 1, y2.max() + 1])
    plt.xlabel("arcsec")
    plt.ylabel("arcsec")

    ############ cross hairs lines ###############

    plt.plot([x2.min(), x2.max()], [0, 0], 'k')
    plt.plot([0, 0], [y2.min(), y2.max()], 'k')

    # additionalTitleComponents = "${\\lambda}$" + str(wavelength)

    # plt.suptitle("H${\\delta}_A$", fontsize=17)
    # axes.set_title("H${\\delta}_A$", fontsize=17)
    plt.title("H${\\delta}_A$", fontsize=17)

    plt.annotate("Plate-IFU: " + "-".join(mainTitle.split('-')
                                          [1:3]), xy=(x2.min() + len(x2) * 0.01, y2.min() + len(y2) * 0.01), size=10)

    plt.savefig(nFP + newFileName +
                '_HDA_' + '.png', bbox_inches='tight', dpi=100)

    # plt.show()
    plt.close('all')
