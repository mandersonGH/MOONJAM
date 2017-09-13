'''
Created on Sep 8, 2017

@author: Mande
'''
import numpy as np
import os

from astropy.io.fits.verify import VerifyError, VerifyWarning
import matplotlib.pyplot as plt

import copy
import string

import Utilities.direcFuncs as dF
import PlottingTools.plottingTools as pT
import PlottingTools.plotFuncs as pF
import GalaxyObject.fitsExtraction as fE
from EmissionLine.EmissionLineSlice import EmissionLineSlice

from PlottingDrivers.PlotterABC import PlotterABC
from PlottingDrivers.PIPE3D.plotSFH import plotSFH


class plotter_PIPE3D(PlotterABC):

    def createSlice(self, dataMat, maskMat, units):
        slice = EmissionLineSlice()
        slice.setData(dataMat)
        slice.setMask(maskMat)
        slice.setUnits(units)
        return slice

    def plot(self, EADir, galaxy, plotType):

        if plotType == 'sfh':
            plotSFH(EADir, galaxy)
        else:
            if plotType == 'flux_elines':
                if not galaxy.myFilename.startswith(plotType):
                    print("No plots of type (" + plotType +
                          ") to make for the file " + galaxy.myFilename)
                    return
            if plotType == 'indices.cs':
                if not galaxy.myFilename.startswith(plotType[:7]):
                    print("No plots of type (" + plotType +
                          ") to make for the file " + galaxy.myFilename)
                    return

            galaxy.setCenterType('HEX')
            galaxy.pullRe(EADir, 'MPL-4')

            NAXIS3 = fE.getNAXIS3(galaxy.myHDU)

            titleHdr = fE.getTitleHeaderPrefix(galaxy.myHDU)

            dataInd = 0

            dictPlotTitles_Index, dictPlotTitles_Error, dictPlotTitles_Pair = self.createDictionaries(
                galaxy, NAXIS3, titleHdr, dataInd)

            PIPE3D_Dir = os.path.join(EADir, "MPL-4", "PLOTS", "PIPE3D")

            if plotType == 'requested':
                requestedWithin = [['velocity', 'stellar population'], [
                    'Ha'], ['Hd'], ['Halpha']]

                dictPlotTitles_Index, dictPlotTitles_Error, dictPlotTitles_Pair = self.removeNonRequested(
                    dictPlotTitles_Index, dictPlotTitles_Error, dictPlotTitles_Pair, requestedWithin)

                nFP = dF.assure_path_exists(os.path.join(
                    PIPE3D_Dir, plotType, galaxy.PLATEIFU))
                nFPraw = ''
            else:
                nFP = dF.assure_path_exists(os.path.join(
                    PIPE3D_Dir, galaxy.PLATEIFU, plotType))
                nFPraw = dF.assure_path_exists(os.path.join(
                    PIPE3D_Dir, galaxy.PLATEIFU, plotType, 'RAW'))

            if not bool(dictPlotTitles_Index):
                print("No plots of type (" + plotType +
                      ") to make for the file " + galaxy.myFilename)
                return
            elif nFPraw != '':
                hex_at_Cen, gal_at_Cen = fE.getCenters(
                    galaxy.myHDU, galaxy.PLATEIFU, dataInd)
                for key in dictPlotTitles_Index.keys():
                    if key in dictPlotTitles_Error.values():
                        continue
                    dataMat, maskMat, newFileName, plotTitle, units = self.prepData(
                        dictPlotTitles_Index, key, galaxy, dataInd, NAXIS3)
                    if dataMat is None:
                        continue
                    aspectRatio = 16.0 / 13
                    height = 10
                    fig = plt.figure(figsize=(aspectRatio * height, height))
                    plt.suptitle(galaxy.PLATEIFU + " :: " + newFileName)
                    axes = plt.gca()
                    slice = self.createSlice(dataMat, maskMat, units)
                    pF.spatiallyResolvedPlot(galaxy,
                                             plotType,
                                             newFileName,
                                             dataInd,
                                             slice,
                                             hex_at_Cen,
                                             gal_at_Cen,
                                             None,
                                             None,
                                             axes)
                    # fig.tight_layout()
                    # plt.show()
                    # print(jello)
                    plt.savefig(os.path.join(nFPraw,newFileName + '.png'))
                    # print(jello)
                    plt.close()

            if bool(dictPlotTitles_Error):
                for key in dictPlotTitles_Error.keys():
                    dataMat, maskMat, newFileName, plotTitle, units = self.prepData(
                        dictPlotTitles_Index, key, galaxy, dataInd, NAXIS3)
                    if dataMat is None:
                        continue
                    keyOfError = dictPlotTitles_Error[key]
                    errMat = galaxy.myHDU[dataInd].data[dictPlotTitles_Index[keyOfError]]
                    slice = self.createSlice(dataMat, maskMat, units)
                    slice.setError(errMat)
                    pF.plotQuadPlot(EADir,
                                    galaxy,
                                    nFP,
                                    dataInd,
                                    slice,
                                    newFileName,
                                    plotTitle,
                                    vmax=None,
                                    vmin=None)

            if bool(dictPlotTitles_Pair):
                for key in dictPlotTitles_Pair.keys():
                    dataMat1, maskMat1, newFileName1, plotTitle1, units1 = self.prepData(
                        dictPlotTitles_Index, key, galaxy, dataInd, NAXIS3)
                    dataMat2, maskMat2, newFileName2, plotTitle2, units2 = self.prepData(
                        dictPlotTitles_Index, dictPlotTitles_Pair[key], galaxy, dataInd, NAXIS3)
                    if dataMat1 is None or dataMat2 is None:
                        continue
                    slice1 = self.createSlice(dataMat1, maskMat1, units1)
                    slice2 = self.createSlice(dataMat2, maskMat2, units2)
                    pF.plotComparisonPlots(galaxy,
                                           dataInd,
                                           nFP,
                                           EADir,
                                           plotType,
                                           newFileName1,
                                           newFileName2,
                                           slice1,
                                           slice2,
                                           hex_at_Cen,
                                           gal_at_Cen
                                           )

    def prepData(self, titleDict, key, galaxy, dataInd, NAXIS3):
        if NAXIS3 == 0:
            dataMat = galaxy.myHDU[dataInd].data
            newFileName = galaxy.myFilename
        else:
            dataMat = galaxy.myHDU[dataInd].data[titleDict[key]]
            newFileName = key

        maskMat = np.zeros(dataMat.shape)
        maskMat[dataMat == 0] = 1
        maskMat[np.abs(dataMat) > 30000] = 1

        plotTitle = galaxy.PLATEIFU + " :: " + newFileName

        if not galaxy.myFilename.startswith('flux_elines') and not galaxy.myFilename.startswith('indices'):
            if titleDict[key] > 99:
                units = galaxy.myHDU[dataInd].header["UNITS_" + str(99)]
            else:
                units = galaxy.myHDU[dataInd].header["UNITS_" +
                                                     str(titleDict[key])]
            units = units.strip()
            if units == 'yr':
                units = 'log(Age(Gyr))'
                dataMat = np.log10(dataMat)
            elif units == 'Solar metallicity':
                units = '[Z/H]'

            if units == 'km':
                units = 'km/s'

            if 'mass weighted' in newFileName:
                units = units + '_{MW}'
            elif 'luminosity weighted' in newFileName:
                units = units + '_{LW}'

            units = '$' + units + '$'
        else:
            units = ""

        newFileName = newFileName.strip()
        newFileName = string.capwords(newFileName)

        return dataMat, maskMat, newFileName, plotTitle, units

    def removeNonRequested(self, dictPlotTitles_Index, dictPlotTitles_Error, dictPlotTitles_Pair, requestedWithin):
        dictKeys = copy.copy(list(dictPlotTitles_Index.keys()))
        for key in dictKeys:
            flag = False
            for withinTextVec in requestedWithin:
                currFlag = True
                for withinComponent in withinTextVec:
                    if not flag and withinComponent not in key:
                        currFlag = False
                if currFlag:
                    flag = True
            if not flag:
                del dictPlotTitles_Index[key]
                if key in dictPlotTitles_Error.keys():
                    del dictPlotTitles_Error[key]
                if key in dictPlotTitles_Pair.keys():
                    del dictPlotTitles_Pair[key]
        return dictPlotTitles_Index, dictPlotTitles_Error, dictPlotTitles_Pair

    def createDictionaries(self, galaxy, NAXIS3, titleHdr, dataInd):
        dictPlotTitles_Index = {}
        dictPlotTitles_Error = {}
        dictPlotTitles_Pair = {}

        for i in range(NAXIS3):
            try:
                plotTitle = galaxy.myHDU[dataInd].header[titleHdr + str(i)]
                plotTitle = plotTitle.strip()
                dictPlotTitles_Index[plotTitle] = i
            except VerifyError:
                print('The header title ' + titleHdr + str(i) +
                      ' is corrupt for the file ' + galaxy.myFilename)
                continue

        errorPrefixes = ['e_', 'error in the ',
                         'error of the ', 'error of ', 'error in ', 'error ']
        pairSuffixes = ['weighted metallicity of the stellar population',
                        'weighted age of the stellar population', ]
        pairFlagsFirstFound = [False, False]
        pairFlagsSecondFound = [False, False]
        tempPairKey = ['', '']

        for key in dictPlotTitles_Index.keys():
            for errorPrefix in errorPrefixes:
                if errorPrefix in key:
                    TitleFromWhereErrorBelongs = key[len(errorPrefix):]
                    if TitleFromWhereErrorBelongs in dictPlotTitles_Index.keys():
                        dictPlotTitles_Error[TitleFromWhereErrorBelongs] = key
                    else:
                        for key2 in dictPlotTitles_Index.keys():
                            if key != key2 and key2.endswith(TitleFromWhereErrorBelongs):
                                dictPlotTitles_Error[key2] = key
                    break

            for i in range(len(pairSuffixes)):
                pairSuffix = pairSuffixes[i]
                if not pairFlagsFirstFound[i] and key.endswith(pairSuffix):
                    tempPairKey[i] = key
                    pairFlagsFirstFound[i] = True
                elif not pairFlagsSecondFound[i] and key.endswith(pairSuffix):
                    # print(str(i) + " " + str(pairFlagsSecondFound[i]))
                    dictPlotTitles_Pair[tempPairKey[i]] = key
                    pairFlagsSecondFound[i] = True

        return dictPlotTitles_Index, dictPlotTitles_Error, dictPlotTitles_Pair
