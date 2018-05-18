import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.cm as cm
import matplotlib.colors as mclr

import PlottingTools.plottingTools as pT
from GalaxyObject import fitsExtraction as fE
import dataCorrection as dC
import Utilities.helperFuncs as hF
import PlottingTools.drawOnPlots as dOP

import Utilities.CALIFAcolourmap as CALIFAcmap

from astropy.io.fits.verify import VerifyError, VerifyWarning

fontsize = 30


def plotAxisCrossSections(galaxy, slice, hex_at_Cen, gal_at_Cen, axes2):
    try:
        dOP.addCrossHairs(axes2, galaxy.PLATEIFU, galaxy.Re, hex_at_Cen)
    except KeyError:
        print("Center and axis unknown for this galaxy")
    dOP.addReCircles(axes2)
    try:
        axes3 = plt.subplot(2, 2, 3)
        plotMajMinAxis(galaxy, slice, hex_at_Cen,
                       gal_at_Cen, axes3, 'major')
        axes4 = plt.subplot(2, 2, 4)
        plotMajMinAxis(galaxy, slice, hex_at_Cen,
                       gal_at_Cen, axes4, 'minor')
    except KeyError:
        print("Center and axis unknown for this galaxy")


def plotQuadPlot(EADir, galaxy, nFP, dataInd, slice, newFileName, plotTitle, vmax=None, vmin=None):

    hex_at_Cen, gal_at_Cen = fE.getCenters(
        galaxy.myHDU, galaxy.PLATEIFU, dataInd)

    # print("Masking " + str(round(float(sum(sum(maskMat)) * 100) /
    #                              (maskMat.shape[0] * maskMat.shape[1]), 2)) + ' percent of the data matrix; ~40 percent is great data')

    aspectRatio = 17.0 / 13
    height = 19
    fig = plt.figure(figsize=(height * aspectRatio, height))
    fig.subplots_adjust(hspace=0.25)
    # plt.figure()
    plt.suptitle(plotTitle, fontsize=fontsize + 5, fontweight='bold')

    axes1 = plt.subplot(2, 2, 1)
    opticalImage(EADir, galaxy, dataInd, axes1)
    # dOP.plotHexagon(axes1, plate_IFU)

    axes2 = plt.subplot(2, 2, 2)
    spatiallyResolvedPlot(galaxy, "", newFileName, dataInd,
                          slice, hex_at_Cen, gal_at_Cen, vmax, vmin, axes2)

    simple = 'No'
    if simple == 'No':
        plotAxisCrossSections(galaxy, slice, hex_at_Cen, gal_at_Cen, axes2)

    # fig.tight_layout()
    try:
        #plt.show()
        #print(jello)
        plt.savefig(os.path.join(nFP, newFileName + '.png'))
    except AttributeError:
        print("Error generating plots. Plot not saved :: "+ os.path.join(nFP, newFileName + '.png'))
    #print(jello)
    plt.close()


def selectBoundsForColorMap(slice, vmax, vmin):
    devs = 3
    if vmin is None:
        vmin = dC.pickVMIN(slice.myData[slice.myMask == 0], devs)
    if vmax is None:
        vmax = dC.pickVMAX(slice.myData[slice.myMask == 0], devs)
    return vmin, vmax


def pickColorMap(plotType):
    if plotType == 'WHAN' or plotType.startswith('BPT'):
        cmap = mclr.ListedColormap(['cornflowerblue', 'orange', 'yellowgreen'])
    else:
        cmap = cm.get_cmap('jet')
    # cmap = CALIFAcmap.get_califa_intensity_cmap()
    # cmap = cm.get_cmap('coolwarm', 3)
    return cmap


def spatiallyResolvedPlot(galaxy, plotType, newFileName, dataInd, slice, hex_at_Cen, gal_at_Cen, vmax, vmin, axes):

    axes.set_title('Spatially Resolved', fontsize=fontsize +
                   5, weight='bold', y=1.01)

    try:
        extentVec = pT.createExtentVec(
            galaxy.PLATEIFU, galaxy.myHDU, dataInd, galaxy.Re, center=galaxy.myCenterType)

        xticks, yticks = pT.getTicks(
            gal_at_Cen, hex_at_Cen, extentVec, galaxy.Re, center=galaxy.myCenterType)

        plt.xticks(xticks, fontsize=fontsize)
        plt.yticks(yticks, fontsize=fontsize)
    except AttributeError:
        print("No Re found")

    masked_image = np.ma.array(slice.myData, mask=slice.myMask)

    ######### plot axis business ############

    plt.xlabel("$R/R_e$", fontsize=fontsize)
    plt.ylabel("$R/R_e$", fontsize=fontsize)

    # galaxy axis business

    ######### plot the thing ############

    if vmin is None or vmax is None:
        vmin, vmax = selectBoundsForColorMap(slice, vmax, vmin)

    cmap = pickColorMap(plotType)

    plt.imshow(masked_image, origin='lower', interpolation='nearest',
               vmin=vmin, vmax=vmax, cmap=cmap,
               extent=extentVec, aspect='auto')

    axes.set_facecolor('grey')

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
            cbar.set_label(slice.myUnits, fontsize=fontsize)
        except ValueError:
            print("Bad Colormap Value")
        except KeyError:
            cbar.set_label('fraction', fontsize=fontsize)

    ###### fix axis skew ########
    if galaxy.myCenterType == 'GAL':
        x1, x2, y1, y2 = pT.axisSkewGal(
            axes, gal_at_Cen, hex_at_Cen, galaxy.Re, extentVec)
        axes.set_xlim(x1, x2)
        axes.set_ylim(y1, y2)
    dOP.plotHexagon(axes, galaxy.PLATEIFU, scale=galaxy.Re * 0.5)


def plotComparisonPlots(galaxy, dataInd, nFP, EADir, plotType, newFileName1, newFileName2, slice1, slice2, hex_at_Cen, gal_at_Cen):
    fig = plt.figure(figsize=(22, 6))
    axes1 = plt.subplot(1, 3, 1)
    opticalImage(axes1, galaxy, dataInd, EADir)

    axes2 = plt.subplot(1, 3, 2)
    spatiallyResolvedPlot(galaxy,
                          plotType,
                          newFileName1,
                          dataInd,
                          slice1,
                          hex_at_Cen,
                          gal_at_Cen,
                          None,
                          None,
                          axes2)

    axes2.set_title(newFileName1)

    axes3 = plt.subplot(1, 3, 3)
    spatiallyResolvedPlot(galaxy,
                          plotType,
                          newFileName2,
                          dataInd,
                          slice2,
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
    plt.savefig(os.path.join(nFP, 'Comparison of ' + newFileName +
                '.png'), bbox_inches='tight')
    plt.close()


def opticalImage(EADir, galaxy, dataInd, axes):
    # extentVec = pT.createExtentVec(plate_IFU, hdu, dataInd, Re, center=center)
    # extentVec = pT.centerVec(extentVec)
    imgType = ''
    try:
    	FileNotFoundError
    except NameError:
        #py2
        FileNotFoundError = IOError
    try:
        visualImage = mpimg.imread(os.path.join(
            EADir, "CAS", galaxy.PLATEIFU, 'Visual.png'))
        imgType = 'png'
    except FileNotFoundError:
        try:
            visualImage = mpimg.imread(os.path.join(
                EADir, "CAS", galaxy.PLATEIFU, 'Optical.png'))
            imgType = 'jpeg'
        except FileNotFoundError:
            visualImage = mpimg.imread(os.path.join(EADir,"CAS", "No Image Found.png"))
    # print(visualImage.shape)
    if imgType == 'png':
        scaleVec = pT.visualImageCropping(
            galaxy.PLATEIFU, visualImage.shape[:2])
        visualImage = visualImage[scaleVec[0]:scaleVec[1],
                                  scaleVec[2]:scaleVec[3]]

    extentVec = [- float(visualImage.shape[0]) / 2, float(visualImage.shape[0]) / 2, -
                 float(visualImage.shape[1]) / 2, float(visualImage.shape[1]) / 2]

    extentVec = np.divide(extentVec, 10)

    plt.imshow(visualImage, extent=extentVec)

    axes.set_title('Original Image :: ' + galaxy.PLATEIFU,
                   fontsize=fontsize + 5, fontweight='bold', y=1.01)

    plt.xlabel('[arcsec]', fontsize=fontsize)
    plt.ylabel('[arcsec]', fontsize=fontsize)
    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)


def plotMajMinAxis(galaxy, slice, hex_at_Cen, gal_at_Cen, axes, axisType):
    distances, indexes = pT.major_minor_axis(
        galaxy.PLATEIFU, axisType, hex_at_Cen, gal_at_Cen, center=galaxy.myCenterType)
    ReMax = 3.6

    axes.set_title('Along ' + axisType.title() + ' Axis',
                   fontsize=fontsize, fontweight='bold', y=1.01)
    axes.set_xlabel('$R/R_e$', fontsize=fontsize)
    axes.set_ylabel(slice.myUnits, fontsize=fontsize)
    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)

    dataAxis = []
    errAxis = []
    for ii in indexes:
        tempXind = ii[1]
        tempYind = ii[0]
        # print(ii)
        # dataMat[tempXind, tempYind] = 100
        if slice.myMask[tempXind, tempYind] != 0:
            dataAxis.append(np.NaN)
            errAxis.append(0)
        else:
            dataAxis.append(slice.myData[tempXind, tempYind])
            errAxis.append(slice.myError[tempXind, tempYind])

    lowInd, highInd = pT.low_high_Inds(distances, galaxy.Re, ReMax)

    distances = distances[lowInd:highInd]

    dataAxis = np.ma.masked_invalid(dataAxis[lowInd:highInd])

    plt.plot(distances / galaxy.Re, dataAxis)
    axes.errorbar(distances / galaxy.Re,
                  dataAxis, yerr=errAxis[lowInd:highInd])


def CAS_spectra(axes, EADir, plate_IFU):
    axes.set_title('Spectra from CAS')
    visualImage = mpimg.imread(os.path.join(
        EADir, "CAS", plate_IFU, plate_IFU + '.gif'))
    plt.imshow(visualImage)
    plt.axis('off')
