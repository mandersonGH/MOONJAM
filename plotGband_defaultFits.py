# extract data from fits file
# read file
# type $ ipython {this file path} {.fits or .gz file path}

from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import direcFuncs


def plotGband_defaultFits(filename, LOGinput):
    # typeStr will indicate to do normal or log plots
    typeStr = ''
    typeMod = '('
    if LOGinput == 1:
        typeStr = '_LOG'
        typeMod = 'Lg('

    # open file
    temp = fits.open(filename)

    # initialize bMat_master
    bMat_master = [[], []]
    pixUnit = ["", ""]

    # temp.info()

    # temp[1] is EMLINE_GFLUX
    # temp[11] is EMLINE_EW
    iAr = [1, 11]
    for ii in range(0, 2):
        i = iAr[ii]

        # print(temp[i].name)
        # print(temp[i].header.keys)

        # axis1_n = temp[i].header[3]
        # axis2_n = temp[i].header[4]
        # refPnt = [temp[i].header[9], temp[i].header[10]]
        pixUnit[ii] = temp[i].header[42]

        # axis1_lbl = temp[i].header[19]
        # axis2_lbl = temp[i].header[20]

        # axis1 = np.linspace(0, axis1_n, axis1_n+1) - refPnt[0]
        # axis2 = np.linspace(0, axis2_n, axis2_n+1) - refPnt[1]

        # bMat's will have:
        #     0 for outside values
        #     1 for good values
        #     0.5 for outliers
        bMat_master[ii] = boundaryMatrix(temp[i].data)

    # setup new directory for figure-saving
    nFP = direcFuncs.setupNewDir(filename, 'GBand', typeStr)
    GBandNames = []
    for j in range(0, 11):
        GBandNames.append(temp[i].header[31 + j])
    GBandNames = reformatGBandNames(GBandNames)
    fileLs = '-'.join((((filename.split('/')
                         [-1]).split('.fits')[0]).split('-'))[1:3])

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

            # printSliceInfo(sliceMat)

            # gray out outliers within hexagon
            bMat = grayOutBadVals(sliceMat, bMat_master[ii])

            # no negative values should be present
            sliceMat[sliceMat < 0] = 0

            if typeStr is not '_':
                # if LOG
                sliceMat[sliceMat == 0] = .00000000000000001
                sliceMat = np.log10(sliceMat)
                sliceMat[sliceMat < -
                         5] = np.min(sliceMat[sliceMat > -5])

            # make outside values invalid for colormap purposes
            sliceMat = whiteOutBndryVals(sliceMat, bMat)

            # choose how many standard deviations from mean should be
            # the top and, if LOG, the bottom of the colormap
            devs = 1

            # set upper colormap value
            vmax = np.mean(sliceMat[bMat != 0.5]) + \
                devs * np.std(sliceMat[bMat != 0.5])

            # set lower colormap value
            if typeStr is '':
                vmin = 0
            else:
                vmin = np.min(sliceMat[bMat != 0.5]) + \
                    2 * np.std(sliceMat[bMat != 0.5])

            # flag outliers(will result in grey)
            sliceMat[bMat == 0.5] = -9999

            # plot

            plt.subplot(1, 2, ii + 1)

            # plt.pcolormesh(sliceMat, cmap=cmap)
            cmap1 = plt.cm.jet
            cmap1.set_bad(alpha=0.0)
            # cmap.set_over()
            # cmap.set_under('0.75', 1)

            plt.pcolormesh(sliceMat, cmap=cmap1, vmin=vmin, vmax=vmax)

            plt.colorbar()
            axes = plt.gca()
            axes.set_xlim([0, sliceMat.shape[0]])
            axes.set_ylim([0, sliceMat.shape[1]])

            # freqHisto(sliceMat[bMat != 0.5])
            plt.suptitle(((filename.split(
                '/')[-1]).split('.fits')[0]) + " " + typeMod + GBandNames[j] + ")", fontsize=17)
            axes.set_title(
                typeMod + temp[i].name + ') ' + pixUnit[ii], fontsize=12)

            # saving plot to new folder
            plt.savefig(nFP + newFileName +
                        '.png', bbox_inches='tight', dpi=100)
            plt.close()
    # plt.show()
    # plt.close('all')


def boundaryMatrix(dataCube):
    tempBndryMat = np.zeros(dataCube[0].shape)
    maxSum = 0
    for lam in range(dataCube.shape[0]):
        for i in range(0, dataCube[lam].shape[0]):
            flag = False
            for j in range(0, dataCube[lam].shape[1]):
                if flag is True:
                    break
                if dataCube[lam, i, j] != 0:
                    for jj in range(dataCube[lam].shape[1] - 1, j, -1):
                        if dataCube[lam, i, jj] != 0:
                            flag = True
                            tempBndryMat[i, j:jj] = 1
                            break
        if np.sum(tempBndryMat) > maxSum:
            maxSum = np.sum(tempBndryMat)
            bndryMat = np.array(tempBndryMat)
    return bndryMat


def grayOutBadVals(sliceMat, bMat):
    tempBMat = np.array(bMat)
    tempBMat[abs(sliceMat) >= 500.0] = 0.5

    # sliceMatNaN = np.array(sliceMat)
    # sliceMatNaN[bMat == 0] = np.NaN
    # sliceMatNaN[abs(sliceMat) >= 1000.0] = np.NaN

    # devs = 15

    # tempBMat[sliceMat < np.nanmean(sliceMatNaN) - devs *
    #          np.nanstd(sliceMatNaN)] = 0.5
    # tempBMat[sliceMat > np.nanmean(sliceMatNaN) + devs *
    #          np.nanstd(sliceMatNaN)] = 0.5

    # print("   min/max [" + str(np.nanmin(sliceMatNaN)) +
    #       ", " + str(np.nanmax(sliceMatNaN)) + "]")
    # print("   avg " + str(np.nanmean(sliceMatNaN)))
    # print("   std " + str(np.nanstd(sliceMatNaN)))

    # l = sliceMat[bMat == 0.5]
    # l = l[~np.equal(l, -9999.0)]

    # print(sorted(l))
    return tempBMat


def whiteOutBndryVals(sliceMat, bMat):
    sliceMat[bMat == 0] = np.NaN
    sliceMat = np.ma.masked_invalid(sliceMat)

    return sliceMat


def freqHisto(main):

    plt.figure()
    plt.hist(main[~np.isnan(main)])


def printSliceInfo(sliceMat):
    print("   min/max [" + str(np.nanmin(sliceMat)) +
          ", " + str(np.nanmax(sliceMat)) + "]")
    print("   avg " + str(np.nanmean(sliceMat)))
    print("   std " + str(np.nanstd(sliceMat)))


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
# plotGband_defaultFits(fin, 2)
# plt.show()
