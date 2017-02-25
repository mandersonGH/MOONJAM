import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.cm as cm
import matplotlib.colors as mclr

import plottingTools as pT
import fitsExtraction as fE
import dataCorrection as dC
import helperFuncs as hF
import drawOnPlots as dOP

import CALIFAcolourmap as CALIFAcmap

from astropy.io.fits.verify import VerifyError, VerifyWarning

fontsize = 30


def plotQuadPlot(EADir, hdu, plate_IFU, Re, center, nFP, dataInd, dataMat, errMat, maskMat, units, newFileName, plotTitle, vmax=None, vmin=None):
    # print(center)
    simple = 'Yes'
    hex_at_Cen, gal_at_Cen = fE.getCenters(hdu, plate_IFU, dataInd)

    # print("Masking " + str(round(float(sum(sum(maskMat)) * 100) /
    #                              (maskMat.shape[0] * maskMat.shape[1]), 2)) + ' percent of the data matrix; ~40 percent is great data')

    aspectRatio = 17.0 / 13
    height = 19
    fig = plt.figure(figsize=(height * aspectRatio, height))
    fig.subplots_adjust(hspace=0.25)
    # plt.figure()
    plt.suptitle(plotTitle, fontsize=fontsize + 5, fontweight='bold')

    axes1 = plt.subplot(2, 2, 1)
    opticalImage(EADir, hdu, plate_IFU, Re, center, dataInd, axes1)
    # dOP.plotHexagon(axes1, plate_IFU)

    axes2 = plt.subplot(2, 2, 2)
    spatiallyResolvedPlot(hdu, "", newFileName, plate_IFU, Re, center, dataInd, units, 
                          dataMat, maskMat, hex_at_Cen, gal_at_Cen, vmax, vmin, axes2)

    if simple == 'No':
      dOP.addCrossHairs(axes2, plate_IFU, Re, hex_at_Cen)
      dOP.addReCircles(axes2)

      axes3 = plt.subplot(2, 2, 3)
      plotMajMinAxis(plate_IFU, Re, center, dataMat, errMat, maskMat, 
                     units, hex_at_Cen, gal_at_Cen, axes3, 'major')


      axes4 = plt.subplot(2, 2, 4)
      plotMajMinAxis(plate_IFU, Re, center, dataMat, errMat, maskMat, 
                     units, hex_at_Cen, gal_at_Cen, axes4, 'minor')

    # fig.tight_layout()
    plt.show()
    print(jello)
    plt.savefig(nFP + newFileName + '.png')
    # print(jello)
    plt.close()


def spatiallyResolvedPlot(hdu, plotType, newFileName, plate_IFU, Re, center, dataInd, units, dataMat, maskMat, hex_at_Cen, gal_at_Cen, vmax, vmin, axes):

    axes.set_title('Spatially Resolved', fontsize=fontsize + 5, weight='bold', y=1.01)

    extentVec = pT.createExtentVec(plate_IFU, hdu, dataInd, Re, center=center)

    xticks, yticks = pT.getTicks(
        gal_at_Cen, hex_at_Cen, extentVec, Re, center=center)

    masked_image = np.ma.array(dataMat, mask=maskMat)

    ######### plot axis business ############

    plt.xlabel("$R/R_e$", fontsize=fontsize)
    plt.ylabel("$R/R_e$", fontsize=fontsize)
    plt.xticks(xticks, fontsize=fontsize)
    plt.yticks(yticks, fontsize=fontsize)

    # galaxy axis business

    ######### plot the thing ############

    devs = 3
    if vmin is None:
        vmin = dC.pickVMIN(dataMat[maskMat == 0], devs)

    if vmax is None:
        vmax = dC.pickVMAX(dataMat[maskMat == 0], devs)

    if plotType == 'WHAN' or plotType.startswith('BPT'):
        cmap = mclr.ListedColormap(['cornflowerblue', 'orange', 'yellowgreen'])
        # cmap = cm.get_cmap('coolwarm', 3)
    else:
        cmap = cm.get_cmap('jet')
        # cmap = CALIFAcmap.get_califa_intensity_cmap()

    plt.imshow(masked_image, origin='lower', interpolation='nearest',
               vmin=vmin, vmax=vmax, cmap=cmap,
               extent=extentVec, aspect='auto')

    axes.set_axis_bgcolor('grey')

    if plotType == 'WHAN' or plotType.startswith('BPT'):
        cbar = plt.colorbar()
        cbar.set_ticks([4.0 / 3, 2, 8.0 / 3])
        if plotType.startswith('BPT'):
            cbar.ax.set_yticklabels(['SF', 'Sy', 'Inter'], weight='bold')
        elif plotType == 'WHAN':
            cbar.ax.set_yticklabels(['SF', 'AGN', 'old stars'], weight='bold')
        cbar.ax.tick_params(labelsize=fontsize)

    else:
        try:
            cbar = plt.colorbar()
            # cbar.set_ticks(np.round(np.linspace(np.log10(vmin), np.log10(vmax), 6), 2))
            cbar.ax.tick_params(labelsize=fontsize)
            cbar.set_label(units, fontsize=fontsize)
        except ValueError:
            print("Bad Colormap Value")
        except KeyError:
            cbar.set_label('fraction', fontsize=fontsize)

    ###### fix axis skew ########
    if center == 'GAL':
        x1, x2, y1, y2 = pT.axisSkewGal(axes, gal_at_Cen, hex_at_Cen, Re, extentVec)
        axes.set_xlim(x1, x2)
        axes.set_ylim(y1, y2)
    dOP.plotHexagon(axes, plate_IFU, scale=Re * 0.5)


def plotComparisonPlots(hdu, plate_IFU, dataInd, nFP, EADir, plotType, newFileName1, newFileName2, Re, dataMat1, maskMat1, dataMat2, maskMat2, hex_at_Cen, gal_at_Cen, center, units1, units2):
    fig = plt.figure(figsize=(22, 6))
    axes1 = plt.subplot(1, 3, 1)
    opticalImage(axes1, hdu, plate_IFU, Re, dataInd, EADir, center)

    axes2 = plt.subplot(1, 3, 2)
    spatiallyResolvedPlot(hdu,
                          plotType,
                          newFileName1,
                          plate_IFU,
                          Re,
                          center,
                          dataInd,
                          units1,
                          dataMat1,
                          maskMat1,
                          hex_at_Cen,
                          gal_at_Cen,
                          None,
                          None,
                          axes2)

    axes2.set_title(newFileName1)

    axes3 = plt.subplot(1, 3, 3)
    spatiallyResolvedPlot(hdu,
                          plotType,
                          newFileName2,
                          plate_IFU,
                          Re,
                          center,
                          dataInd,
                          units2,
                          dataMat2,
                          maskMat2,
                          hex_at_Cen,
                          gal_at_Cen,
                          None,
                          None,
                          axes3)

    axes3.set_title(newFileName2)
    fig.tight_layout()

    newFileName = hF.findCompareOverlap(newFileName1, newFileName2)

    # plt.show()
    # print(jello)
    plt.savefig(nFP + 'Comparison of ' + newFileName + '.png', bbox_inches='tight')
    plt.close()


def opticalImage(EADir, hdu, plate_IFU, Re, center, dataInd, axes):
    # extentVec = pT.createExtentVec(plate_IFU, hdu, dataInd, Re, center=center)
    # extentVec = pT.centerVec(extentVec)
    imgType = ''
    try:
        visualImage = mpimg.imread(EADir + '/CAS/' + plate_IFU + '/Visual.png')
        imgType = 'png'
    except FileNotFoundError:
        try:
          visualImage = mpimg.imread(EADir + '/CAS/' + plate_IFU + '/Optical.jpeg')
          imgType = 'jpeg'
        except FileNotFoundError:
          visualImage = mpimg.imread(EADir + '/CAS/No Image Found.png')
    # print(visualImage.shape)
    if imgType == 'png':
        scaleVec = pT.visualImageCropping(plate_IFU, visualImage.shape[:2])
        visualImage = visualImage[scaleVec[0]:scaleVec[1],
                              scaleVec[2]:scaleVec[3]]

    extentVec = [- float(visualImage.shape[0]) / 2, float(visualImage.shape[0]) / 2, -
                 float(visualImage.shape[1]) / 2, float(visualImage.shape[1]) / 2]

    extentVec = np.divide(extentVec, 10)

    plt.imshow(visualImage, extent=extentVec)

    axes.set_title('Original Image :: ' + plate_IFU, fontsize=fontsize + 5, fontweight='bold', y=1.01)

    plt.xlabel('[arcsec]', fontsize=fontsize)
    plt.ylabel('[arcsec]', fontsize=fontsize)
    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)


def plotMajMinAxis(plate_IFU, Re, center, dataMat, errMat, maskMat, units, hex_at_Cen, gal_at_Cen, axes, axisType):

    distances, indexes = pT.major_minor_axis(
        plate_IFU, axisType, hex_at_Cen, gal_at_Cen, center=center)

    ReMax = 3.6

    axes.set_title('Along ' + axisType.title() + ' Axis', fontsize=fontsize, fontweight='bold', y=1.01)
    axes.set_xlabel('$R/R_e$', fontsize=fontsize)
    axes.set_ylabel(units, fontsize=fontsize)
    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)

    dataAxis = []
    errAxis = []
    for ii in indexes:
        tempXind = ii[1]
        tempYind = ii[0]
        # print(ii)
        # dataMat[tempXind, tempYind] = 100
        if maskMat[tempXind, tempYind] != 0:
            dataAxis.append(np.NaN)
            errAxis.append(0)
        else:
            dataAxis.append(dataMat[tempXind, tempYind])
            errAxis.append(errMat[tempXind, tempYind])

    lowInd, highInd = pT.low_high_Inds(distances, Re, ReMax)

    distances = distances[lowInd:highInd]

    dataAxis = np.ma.masked_invalid(dataAxis[lowInd:highInd])
    plt.plot(distances / Re, dataAxis)
    axes.errorbar(distances / Re,
                  dataAxis, yerr=errAxis[lowInd:highInd])


def CAS_spectra(axes, EADir, plate_IFU):
    axes.set_title('Spectra from CAS')
    visualImage = mpimg.imread(EADir + '/CAS/' + plate_IFU + '/' + plate_IFU + '.gif')
    plt.imshow(visualImage)
    plt.axis('off')
