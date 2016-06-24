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
    index = pT.findIndex(waveVec, 4101.75)
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

    cmapD = plt.cm.plasma

    plt.pcolormesh(x2, y2, sliceMat, cmap=cmapD)

    cbar = plt.colorbar()
    cbar.set_label(temp[1].header[19])

    plt.axis([x2.min(), x2.max(), y2.min(), y2.max()])
    plt.xlabel("arcsec")
    plt.ylabel("arcsec")

    ############ cross hairs lines ###############

    plt.plot([x2.min(), x2.max()], [0, 0], 'k')
    plt.plot([0, 0], [y2.min(), y2.max()], 'k')

    plt.suptitle(mainTitle + '_HDA', fontsize=17)

    plt.savefig(nFP + newFileName +
                '_HDA_' + '.png', bbox_inches='tight', dpi=100)

    # plt.show()
    plt.close('all')
