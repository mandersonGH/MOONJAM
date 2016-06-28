from astropy.io import fits
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import direcFuncs
import dataCorrection as dC
import plottingTools as pT


def plotGband(filename, LOGinput):
    # typeStr will indicate to do normal or log plots
    typeStr = ''
    if LOGinput == 1:
        typeStr = '_LOG'

    # open file
    hdu = fits.open(filename)

    plate_IFU, SPAXD_vec = pT.pullGeneralInfo(hdu[0].header, filename)

    # temp.info()

    # temp[1] is EMLINE_GFLUX
    # temp[11] is EMLINE_EW
    iAr = [1, 11]
    # for ii in range(0, 2):
    #     i = iAr[ii]
    # temp.info()
    # print(temp[1].header.keys)

    # setup new directory for figure-saving
    nFP = direcFuncs.setupNewDir(filename, 'GBand', typeStr)

    # correct GBand names to include bracket for forbidden transitions
    GBandNames = []
    for j in range(0, 11):
        GBandNames.append(hdu[iAr[1]].header[31 + j])
    tempVec = reformatGBandNames(GBandNames)
    GBandNames = tempVec[0]
    GBandFancyNames = tempVec[1]

    # print(GBandNames)
    # print(GBandFancyNames)
    # cycle through 11 chosen wavelengths
    for j in range(0, 11):
        # print(temp[i].name.split("_")[-1] +
        #       ": " + temp[i].header[31 + j])

        newFileName = plate_IFU + '_' + GBandNames[j] + typeStr

        plt.figure(figsize=(15.5, 5.5))

        for ii in range(0, 2):
            i = iAr[ii]

            # pick out data slice
            sliceMat = hdu[i].data[j]

            ############ data Correction #############

            # dC.printDataInfo(sliceMat)

            sliceMat = dC.flagOutsideZeros(sliceMat)

            sliceMat = dC.zeroOutNegatives(sliceMat)

            sliceMat = dC.flagHighValues(sliceMat, 300.0)

            sliceMat = dC.flagOutlierValues(sliceMat, 10)

            # dC.checkFreqHisto(sliceMat, temp[i].name + " " + GBandNames[j])

            if LOGinput == 1:
                # if LOG then log the data
                sliceMat[sliceMat < .05] = np.NaN
                sliceMat = np.log10(sliceMat)

            ########### limits on colorbar ############

            # set upper colormap value
            # vmax = np.nanmean(sliceMat) + 1 * np.nanstd(sliceMat)

            # set lower colormap value
            if typeStr is '':
                vmin = 0
            else:
                vmin = dC.pickVMIN(sliceMat, 1)

            sliceMat = dC.maskInvalidFlaggedVals(sliceMat)

            ########  #########
            axes = plt.subplot(1, 2, ii + 1)

            ##### Plot titles ########

            plt.suptitle(GBandFancyNames[j], fontsize=17)

            if LOGinput == 0:
                axes.set_title(GBandFancyNames[
                               j] + " " + hdu[i].name.split("_")[1], fontsize=12)
            elif LOGinput == 1:
                axes.set_title(
                    "log (" + GBandFancyNames[j] + " " + hdu[i].name.split("_")[1] + ")", fontsize=12)

            ######### axis business ############

            plt.xlabel("arcsec")
            plt.ylabel("arcsec")

            x2, y2 = pT.createAxis(plate_IFU, hdu, i, 'default')

            plt.axis([x2.min() - 1, x2.max() + 1, y2.min() - 1, y2.max() + 1])

            ########### hexagon border ##############

            # plotHexagon.plotHexagon([(0, 0)], 70000, axes)

            ############## plotting and colormap ############
            # cmap1 = plt.cm.viridis
            cmap1 = plt.cm.plasma
            cmap1.set_bad('0.75')
            # cmap.set_over()
            # cmap.set_under('0.75', 1)

            # plt.pcolormesh(x2, y2, sliceMat, cmap=cmap1)
            plt.pcolormesh(x2, y2, sliceMat, cmap=cmap1, vmin=vmin)
            # plt.pcolormesh(x2, y2, sliceMat, cmap=cmap1, vmin=vmin, vmax=vmax)

            cbar = plt.colorbar()
            cbar.set_label(hdu[i].header[42])

            ############ cross hairs lines ###############

            plt.plot([x2.min(), x2.max()], [0, 0], 'k')
            plt.plot([0, 0], [y2.min(), y2.max()], 'k')

            ########### plateIFU annotiation ##############
            plt.annotate("Plate-IFU: " + plate_IFU, xy=(x2.min() +
                                                     len(x2) * 0.01, y2.min() + len(y2) * 0.01), size=10)

            ########## saving plot to new folder #############
            plt.savefig(nFP + newFileName +
                        '.png', bbox_inches='tight', dpi=100)
        # plt.close()
    # plt.show()
    plt.close('all')


def reformatGBandNames(GBandNames):
    GBandFancyNames = [""] * len(GBandNames)
    greekLet = ""
    for i in range(0, len(GBandNames)):
        tempVec = GBandNames[i].split('-')
        if GBandNames[i].startswith("H"):
            GBandNames[i] = tempVec[0] + "____" + tempVec[-1]
            if GBandNames[i][1] == 'a':
                greekLet = '${\\alpha}$'
            elif GBandNames[i][1] == 'b':
                greekLet = '${\\beta}$'
            elif GBandNames[i][1] == 'c':
                greekLet = '${\\gamma}$'
            elif GBandNames[i][1] == 'd':
                greekLet = '${\\delta}$'
            GBandFancyNames[i] = "H" + greekLet + \
                " " + "${\\lambda}$" + tempVec[-1]
        else:
            if len(tempVec[0]) == 2:
                underscore2Add = '__'
            elif len(tempVec[0]) == 3:
                underscore2Add = '_'
            else:
                underscore2Add = ''
            GBandNames[i] = '[' + tempVec[0] + ']' + \
                underscore2Add + tempVec[-1]
            GBandFancyNames[i] = '[' + tempVec[0] + '] ' + \
                '${\\lambda}$' + tempVec[-1]

    return [GBandNames, GBandFancyNames]
