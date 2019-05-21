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

    def __init__(self, mplNum):
        self.DAPtype = mplNum

    def createSlice(self, dataMat, maskMat, units):
        slice = EmissionLineSlice()
        slice.setData(dataMat)
        slice.setMask(maskMat)
        slice.setUnits(units)
        return slice

    def plot(self, EADir, galaxy, plotType):
        

        if plotType == 'sfh' and self.DAPtype == 'MPL-4':
            plotSFH(EADir, galaxy)
        else:
            if not self.are_there_plots_to_make(galaxy.myFilename, plotType):
                return
            # print(galaxy.myFilename)
            # print(plotType)

            PIPE3D_Dir = os.path.join(EADir, self.DAPtype, "PLOTS", "PIPE3D")
            # print("PIPE3D_Dir=" + str(PIPE3D_Dir))
            
            galaxy.setCenterType('HEX')
            
            galaxy.pullRe(EADir, self.DAPtype)
            # print("Re=" + str(galaxy.Re))
            
            NAXIS3 = fE.getNAXIS3(galaxy.myHDU)
            # print("NAXIS3=" + str(NAXIS3))
            
            titleHdr = fE.getTitleHeaderPrefix(galaxy.myHDU)
            # print("titleHdr=" + str(titleHdr))

            dataInd = 0
            # print("dataInd=" + str(dataInd))

            plotsToMake = self.createDictionaries(galaxy,
                                                  NAXIS3,
                                                  titleHdr,
                                                  dataInd)
            numberOfNormalPlotsToMake = sum([1 for p in plotsToMake.keys() if 'index' in plotsToMake[p]])
            numberOfErrorPlotsToMake = sum([1 for p in plotsToMake.keys() if 'error' in plotsToMake[p]])
            numberOfPairPlotsToMake = sum([1 for p in plotsToMake.keys() if 'pair' in plotsToMake[p]])

            print(
                "normalPlots=" + str(numberOfNormalPlotsToMake),
                "errorPlots=" + str(numberOfErrorPlotsToMake),
                "pairPlots=" + str(numberOfPairPlotsToMake)
            )
            
            if plotType == 'requested' or plotType == 'requested2':
                # if requested plots then remove unecessary plot titles and change directory
                requestedWithin = [
                    ['velocity', 'stellar population'],
                    ['Ha'],
                    ['Hd'],
                    ['Halpha']
                ]
                plotsToMake = self.removeNonRequested( plotsToMake, requestedWithin )

                numberOfNormalPlotsToMake = sum([1 for p in plotsToMake.keys() if 'index' in plotsToMake[p]])
                numberOfErrorPlotsToMake = sum([1 for p in plotsToMake.keys() if 'error' in plotsToMake[p]])
                numberOfPairPlotsToMake = sum([1 for p in plotsToMake.keys() if 'pair' in plotsToMake[p]])

                print(
                    "normalPlots=" + str(numberOfNormalPlotsToMake),
                    "errorPlots=" + str(numberOfErrorPlotsToMake),
                    "pairPlots=" + str(numberOfPairPlotsToMake)
                )



            if numberOfNormalPlotsToMake == 0:
                print("No plots of type (" + plotType +
                       ") to make for the file " + galaxy.myFilename)
                return
            
            nFP, nFPraw = self.create_directories(plotType, PIPE3D_Dir, galaxy.PLATEIFU)

            hex_at_Cen, gal_at_Cen = fE.getCenters(
                    galaxy.myHDU, galaxy.PLATEIFU, dataInd)

            for rawPlotTitle, plotInfo in plotsToMake.items():
                dataMat, maskMat, newFileName, plotTitle, units = self.prepData(
                    plotInfo['index'],
                    rawPlotTitle,
                    galaxy,
                    dataInd,
                    NAXIS3
                )
                if dataMat is None:
                    return
                slice = self.createSlice(dataMat, maskMat, units)

                if nFPraw != '':
                    try:
                        self.plotRaw(galaxy,
                                     newFileName,
                                     dataInd,
                                     plotType,
                                     slice,
                                     hex_at_Cen,
                                     gal_at_Cen,
                                     nFPraw)
                    except Exception as e:
                        print(e)
                        plt.close()
                        continue
                
                if numberOfNormalPlotsToMake < 20:
                    pF.plotDuoPlot(EADir,
                                   galaxy,
                                   nFP,
                                   dataInd,
                                   slice,
                                   newFileName,
                                   plotTitle,
                                   plotType,
                                   vmax=None,
                                   vmin=None)


                if 'error' in plotInfo.keys():
                    errorPlotTitle = plotInfo['error']
                    errMat = galaxy.myHDU[dataInd].data[plotsToMake[errorPlotTitle]['index']]
                    slice.setError(errMat)
                    try:
                        pF.plotQuadPlot(EADir,
                                        galaxy,
                                        nFP,
                                        dataInd,
                                        slice,
                                        newFileName,
                                        plotTitle,
                                        vmax=None,
                                        vmin=None)
                    except Exception as e:
                        plt.close()
                        print(e)
                        if numberOfNormalPlotsToMake >= 20:
                            pF.plotDuoPlot(EADir,
                                           galaxy,
                                           nFP,
                                           dataInd,
                                           slice,
                                           newFileName,
                                           plotTitle,
                                           vmax=None,
                                           vmin=None)

                if 'pair' in plotInfo.keys():
                    dataMat2, maskMat2, newFileName2, plotTitle2, units2 = self.prepData(
                        plotInfo['index'], plotsToMake[plotInfo['pair']]['index'], galaxy, dataInd, NAXIS3)

                    if dataMat2 is None:
                        return
                    
                    slice2 = self.createSlice(dataMat2, maskMat2, units2)
                    pF.plotComparisonPlots(galaxy,
                                           dataInd,
                                           nFP,
                                           EADir,
                                           plotType,
                                           newFileName,
                                           newFileName2,
                                           slice,
                                           slice2,
                                           hex_at_Cen,
                                           gal_at_Cen)


            return

    def plotRaw(self, galaxy, newFileName, dataInd, plotType, slice, hex_at_Cen, gal_at_Cen, nFPraw):
        aspectRatio = 16.0 / 13
        height = 10
        fig = plt.figure(figsize=(aspectRatio * height, height))
        plt.suptitle(galaxy.PLATEIFU + " :: " + newFileName)
        axes = plt.gca()
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
        print("saving " + os.path.join(nFPraw,newFileName + '.png'))
        plt.savefig(os.path.join(nFPraw,newFileName + '.png'))
        # print(jello)
        plt.close()

    def are_there_plots_to_make(self, galaxy_filename, plotType):
        if plotType == 'flux_elines':
            if not galaxy_filename.startswith(plotType):
                print("No plots of type (" + plotType +
                      ") to make for the file " + galaxy_filename)
                return False
        
        if plotType == 'indices.cs':
            if not galaxy_filename.startswith(plotType[:7]):
                print("No plots of type (" + plotType +
                      ") to make for the file " + galaxy_filename)
                return False

        if galaxy_filename.endswith('Pipe3D.cube.fits.gz'):
            print('skipping Pipe3D.cube.fits.gz')
            return False
        return True


    def create_directories(self, plotType, PIPE3D_Dir, plateifu):
        if plotType == 'requested' or plotType == 'requested2':
            nFP = dF.assure_path_exists(os.path.join(
                PIPE3D_Dir, plotType, plateifu))
            nFPraw = dF.assure_path_exists(os.path.join(
                PIPE3D_Dir, plotType, plateifu, 'RAW'))
        else:
            nFP = dF.assure_path_exists(os.path.join(
                PIPE3D_Dir, plateifu, plotType))
            nFPraw = dF.assure_path_exists(os.path.join(
                PIPE3D_Dir, plateifu, plotType, 'RAW'))

        return nFP, nFPraw


    def prepData(self, plotIndex, rawPlotTitle, galaxy, dataInd, NAXIS3):
        if NAXIS3 == 0:
            dataMat = galaxy.myHDU[dataInd].data
            newFileName = galaxy.myFilename
        else:
            dataMat = galaxy.myHDU[dataInd].data[plotIndex]
            newFileName = rawPlotTitle

        maskMat = np.zeros(dataMat.shape)
        maskMat[dataMat == 0] = 1
        maskMat[np.abs(dataMat) > 30000] = 1

        plotTitle = galaxy.PLATEIFU + " :: " + newFileName

        if not galaxy.myFilename.startswith('flux_elines') and not galaxy.myFilename.startswith('indices'):
            if plotIndex > 99:
                units = galaxy.myHDU[dataInd].header["UNITS_" + str(99)]
            else:
                units = galaxy.myHDU[dataInd].header["UNITS_" +
                                                     str(plotIndex)]
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

    def removeNonRequested(self, plotsToMake, requestedWithin):
        plotNames = copy.copy(list(plotsToMake.keys()))
        for key in plotNames:
            flag = False
            for withinTextVec in requestedWithin:
                currFlag = True
                for withinComponent in withinTextVec:
                    if not flag and withinComponent not in key:
                        currFlag = False
                if currFlag:
                    flag = True
            if not flag:
                del plotsToMake[key]
        return plotsToMake

    def createDictionaries(self, galaxy, NAXIS3, titleHdr, dataInd):
        plotsToMake = {}
        # dictPlotTitles_Index = {}
        # dictPlotTitles_Error = {}
        # dictPlotTitles_Pair = {}

        for i in range(NAXIS3):
            try:
                plotTitle = galaxy.myHDU[dataInd].header[titleHdr + str(i)]
                plotTitle = plotTitle.strip()
                plotsToMake[plotTitle] = {
                    'index' : i
                }
                # dictPlotTitles_Index[plotTitle] = i
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

        # for key in dictPlotTitles_Index.keys():
        for key in plotsToMake.keys():
            for errorPrefix in errorPrefixes:
                if errorPrefix in key:
                    TitleFromWhereErrorBelongs = key[len(errorPrefix):]
                    if TitleFromWhereErrorBelongs in plotsToMake.keys():
                        # dictPlotTitles_Error[TitleFromWhereErrorBelongs] = key
                        plotsToMake[TitleFromWhereErrorBelongs]['error'] = key
                    else:
                        for key2 in plotsToMake.keys():
                            if key != key2 and key2.endswith(TitleFromWhereErrorBelongs):
                                # dictPlotTitles_Error[key2] = key
                                plotsToMake[key2]['error'] = key
                    break

            for i in range(len(pairSuffixes)):
                pairSuffix = pairSuffixes[i]
                if not pairFlagsFirstFound[i] and key.endswith(pairSuffix):
                    tempPairKey[i] = key
                    pairFlagsFirstFound[i] = True
                elif not pairFlagsSecondFound[i] and key.endswith(pairSuffix):
                    # print(str(i) + " " + str(pairFlagsSecondFound[i]))
                    # dictPlotTitles_Pair[tempPairKey[i]] = key
                    plotsToMake[tempPairKey[i]]['pair'] = key
                    pairFlagsSecondFound[i] = True

        return plotsToMake
