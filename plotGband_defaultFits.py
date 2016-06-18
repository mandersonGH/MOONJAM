# extract data from fits file
# read file
# type $ ipython {this file path} {.fits or .gz file path}

from astropy.io import fits
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import direcFuncs
import dataCorrection as dC
import plotHexagon


def plotGband_defaultFits(filename, LOGinput):
    # typeStr will indicate to do normal or log plots
    typeStr = ''
    typeMod = '('
    if LOGinput == 1:
        typeStr = '_LOG'
        typeMod = 'Lg('

    # open file
    temp = fits.open(filename)

    # temp.info()

    # temp[1] is EMLINE_GFLUX
    # temp[11] is EMLINE_EW
    iAr = [1, 11]
    # for ii in range(0, 2):
    #     i = iAr[ii]
    # print(temp[i].name)
    # print(temp[1].header.keys)

    # setup new directory for figure-saving
    nFP = direcFuncs.setupNewDir(filename, 'GBand', typeStr)
    fileLs = '-'.join((((filename.split('/')
                         [-1]).split('.fits')[0]).split('-'))[1:3])

    # correct GBand names to include bracket for forbidden transitions
    GBandNames = []
    for j in range(0, 11):
        GBandNames.append(temp[iAr[1]].header[31 + j])
    GBandNames = reformatGBandNames(GBandNames)

    # cycle through 11 chosen wavelengths
    for j in range(0, 11):
        # print(temp[i].name.split("_")[-1] +
        #       ": " + temp[i].header[31 + j])

        newFileName = fileLs + '_' + GBandNames[j] + typeStr

        plt.figure(figsize=(15.5, 5.5))

        for ii in range(0, 2):
            i = iAr[ii]

            # pick out data slice
            sliceMat = temp[i].data[j]

            ############ data Correction #############

            # dC.printDataInfo(sliceMat)

            sliceMat = dC.eliminateNegatives(sliceMat)

            sliceMat = dC.flagOutsideZeros(sliceMat)

            sliceMat = dC.flagHighValues(sliceMat, 300.0)

            sliceMat = dC.flagOutlierValues(sliceMat)

            # dC.checkFreqHisto(sliceMat, temp[i].name + " " + GBandNames[j])

            if typeStr is '_LOG':
                # if LOG then log the data
                sliceMat[sliceMat < .05] = np.NaN
                sliceMat = np.log10(sliceMat)

            sliceMat = dC.whiteFlaggedVals(sliceMat)

            ########### limits on colorbar ############

            # set upper colormap value
            # vmax = np.nanmean(sliceMat) + 1 * np.nanstd(sliceMat)

            # set lower colormap value
            if typeStr is '':
                vmin = 0
            else:
                vmin = np.nanmin(sliceMat) + 1 * np.nanstd(sliceMat)

            ######## get plot ready #########
            axes = plt.subplot(1, 2, ii + 1)
            plt.suptitle(((filename.split(
                '/')[-1]).split('.fits')[0]) + " " + typeMod + GBandNames[j] + ")", fontsize=17)
            axes.set_title(
                typeMod + temp[i].name + ')', fontsize=12)

            ######### axis business ############

            # # to be done once axis labels are found
            # axis1_lbl = temp[i].header[17]
            # axis2_lbl = temp[i].header[18]
            # plt.xlabel(axis1_lbl)
            # plt.ylabel(axis2_lbl)

            axis1_n = temp[i].header[3]
            axis2_n = temp[i].header[4]
            refPnt = [temp[i].header[9], temp[i].header[10]]
            axis1 = np.linspace(0, axis1_n, axis1_n + 1) - refPnt[0]
            axis2 = np.linspace(0, axis2_n, axis2_n + 1) - refPnt[1]

            dx = 1
            dy = 1
            xmin = min(axis1)
            xmax = max(axis1)
            ymin = min(axis2)
            ymax = max(axis2)

            x2, y2 = np.meshgrid(np.arange(
                xmin, xmax + dx, dx) - dx / 2., np.arange(ymin, ymax + dy, dy) - dy / 2.)

            plt.axis([x2.min() - 1, x2.max() + 1, y2.min() - 1, y2.max() + 1])

            ########### hexagon border ##############

            # plotHexagon.plotHexagon([(0, 0)], 70000, axes)

            ############## plotting and colormap ############
            # cmap1 = plt.cm.viridis
            cmap1 = plt.cm.plasma
            cmap1.set_bad(alpha=0.0)
            # cmap.set_over()
            # cmap.set_under('0.75', 1)

            # plt.pcolormesh(x2, y2, sliceMat, cmap=cmap1)
            plt.pcolormesh(x2, y2, sliceMat, cmap=cmap1, vmin=vmin)
            # plt.pcolormesh(x2, y2, sliceMat, cmap=cmap1, vmin=vmin, vmax=vmax)

            cbar = plt.colorbar()
            cbar.set_label(temp[i].header[42])

            ############ cross hairs lines ###############

            plt.plot([x2.min(), x2.max()], [0, 0], 'k')
            plt.plot([0, 0], [y2.min(), y2.max()], 'k')

            ########## saving plot to new folder #############
            plt.savefig(nFP + newFileName +
                        '.png', bbox_inches='tight', dpi=100)
        # plt.close()
    # plt.show()
    plt.close('all')


def reformatGBandNames(GBandNames):
    for i in range(0, len(GBandNames)):
        tempVec = GBandNames[i].split('-')
        if GBandNames[i].startswith("H"):
            GBandNames[i] = tempVec[0] + "____" + tempVec[-1]
        else:
            if len(tempVec[0]) == 2:
                underscore2Add = '__'
            elif len(tempVec[0]) == 3:
                underscore2Add = '_'
            else:
                underscore2Add = ''
            GBandNames[i] = '[' + tempVec[0] + ']' + \
                underscore2Add + tempVec[-1]

    return GBandNames
