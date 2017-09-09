'''
Created on Sep 8, 2017

@author: Mande
'''

import numpy as np

import matplotlib.pyplot as plt

import Utilities.helperFuncs as hF
import Utilities.mathFuncs as mF
import Utilities.direcFuncs as dF
import GalaxyObject.fitsExtraction as fE
import PlottingTools.plottingTools as pT
from PlottingTools.plotFuncs import CAS_spectra


def plotReSpectra(EADir, galaxy, DAPtype, plotType, dataInd, dataCube, waveVec):
    nFP = dF.assure_path_exists(
        EADir + DAPtype + '/PLOTS/DAP/' + galaxy.PLATEIFU + '/ReSpectra/')
    # unitsY = hdu[0].header['BUNIT']
    unitsX = 'Wavelength (Angstroms)'
    # unitsY = '$' + unitsY + '$'
    # unitsX = '$' + unitsX + '$'

    unitsY = '$f_{\\lambda}$ ' + \
        ' (' + '$10^{-17}$' + 'erg/s/cm' + '$^{2}$' + '/Ang)'

    hex_at_Cen, gal_at_Cen = fE.getCenters(
        galaxy.myHDU, galaxy.PLATEIFU, dataInd)

    refPnt = [hex_at_Cen[1], hex_at_Cen[0]]

    radii = [0.25, .5, 1.0]
    # radii = [1, 2, 3]

    # ReSpectra, dictRadiiSpaxNum = createRadialSpectra(waveVec, dataCube, radii, refPnt, Re)
    NormalizedReSpectra, dictRadiiSpaxNum = createRadialSpectra(
        waveVec, dataCube, radii, refPnt, galaxy.Re, normWavelength=5500)

    # ReSpectra, dictWedgeSpaxNum = createWedgeSpectra(dataCube, radii, refPnt, Re, hdu, plate_IFU, dataInd, center)

    # plotSideBySideSpectra(plate_IFU, radii, waveVec, ReSpectra, dictRadiiSpaxNum, unitsX, unitsY, EADir, nFP, '123')
    # plotStackedSpectra(plate_IFU, radii, waveVec, ReSpectra, dictRadiiSpaxNum, unitsX, unitsY, EADir, nFP)
    plotStackedSpectra(galaxy.PLATEIFU, radii, waveVec, NormalizedReSpectra, dictRadiiSpaxNum,
                       unitsX, unitsY, EADir, nFP, extraLabel='Normed')


def normalizeSpectra(waveVec, ReSpectra, wavelength):
    lowInd = mF.findIndex(waveVec, wavelength - 50)
    highInd = mF.findIndex(waveVec, wavelength + 50)

    normFactor = np.median(ReSpectra[lowInd:highInd])

    return np.divide(ReSpectra, normFactor)


def createWedgeSpectra(dataCube, radii, refPnt, Re, hdu, plate_IFU, dataInd, center):
    ReSpectra = [np.zeros(dataCube.shape[0]) for i in range(len(radii) * 4)]
    spaxCounts = np.zeros(len(radii) * 4)
    dictWedgeSpaxNum = {}

    hex_at_Cen, gal_at_Cen = fE.getCenters(hdu, plate_IFU, dataInd)
    axisCoordMaj, mMaj, bMaj = pT.getAxisLineProperties(
        plate_IFU, 'major', center, gal_at_Cen, hex_at_Cen)
    axisCoordMin, mMin, bMin = pT.getAxisLineProperties(
        plate_IFU, 'minor', center, gal_at_Cen, hex_at_Cen)

    wedgeLabelMat = createWedgeLabelMat(
        dataCube[0].shape, radii, Re, refPnt, mMaj, bMaj, mMin, bMin)

    # plt.figure()
    # plt.imshow(wedgeLabelMat, origin='lower', interpolation='nearest')
    # plt.colorbar()
    # plt.show()
    # print(jello)

    for y in range(wedgeLabelMat.shape[0]):
        for x in range(wedgeLabelMat.shape[1]):
            for mod in range(1, 5):
                if wedgeLabelMat[y, x] % 5 == mod:
                    currDist = mF.calculateDistance(x, y, refPnt[0], refPnt[1])
                    for r in range(len(radii)):
                        if currDist <= radii[r] * Re:
                            index = mod + r * 5 - 1
                            if index > 4:
                                index -= 1
                            if index > 9:
                                index -= 1
                            ReSpectra[index] = ReSpectra[index] + \
                                dataCube[:, y, x]

    return ReSpectra, dictWedgeSpaxNum


def createWedgeLabelMat(shape, radii, Re, refPnt, mMaj, bMaj, mMin, bMin):
    wedgeLabelMat = np.zeros(shape)

    for y in range(wedgeLabelMat.shape[0]):
        for x in range(wedgeLabelMat.shape[1]):
            currDist = mF.calculateDistance(x, y, refPnt[0], refPnt[1])
            # print(x, y, currDist)
            for r in reversed(range(len(radii))):
                if currDist <= radii[r] * Re:
                    wedgeLabelMat[y, x] = r * 4 + 1
            if wedgeLabelMat[y, x] != 0:
                yMaj = mMaj * x + bMaj
                yMin = mMin * x + bMin
                if y > yMaj and y < yMin:
                    wedgeLabelMat[y, x] += 1
                elif y < yMaj and y < yMin:
                    wedgeLabelMat[y, x] += 2
                elif y < yMaj and y > yMin:
                    wedgeLabelMat[y, x] += 3
                if wedgeLabelMat[y, x] > 8:
                    wedgeLabelMat[y, x] += 2
                elif wedgeLabelMat[y, x] > 4:
                    wedgeLabelMat[y, x] += 1

    return wedgeLabelMat


def createRadialSpectra(waveVec, dataCube, radii, refPnt, Re, normWavelength=''):
    ReSpectra = []
    dictRadiiSpaxNum = {}
    for k in range(len(radii)):
        ReSpectra.append(np.zeros(dataCube.shape[0]))

    for k in range(len(radii)):
        count = 0
        for i in range(dataCube.shape[1]):
            for j in range(dataCube.shape[2]):
                if mF.calculateDistance(refPnt[0], refPnt[1], i, j) / Re <= radii[k]:
                    count += 1
                    ReSpectra[k] = ReSpectra[k] + dataCube[:, i, j]
        dictRadiiSpaxNum[radii[k]] = count
        if normWavelength != '':
            ReSpectra[k] = normalizeSpectra(
                waveVec, ReSpectra[k], normWavelength)
    return ReSpectra, dictRadiiSpaxNum


def plotSideBySideSpectra(plate_IFU, radii, waveVec, ReSpectra, dictRadiiSpaxNum, unitsX, unitsY, EADir, nFP, extraLabel=''):
    fontsize = 30
    legVec = []
    aspectRatio = 14.0 / 7
    height = 19
    fig = plt.figure(figsize=(aspectRatio * height, height))
    # fig = plt.figure()

    axes1 = plt.subplot(2, 3, 2)
    CAS_spectra(axes1, EADir, plate_IFU)

    for i in range(len(radii)):
        axesTemp = plt.subplot(2, 3, 4 + i)
        plt.plot(waveVec, ReSpectra[i])
        spaxNum = dictRadiiSpaxNum[radii[i]]
        axesTemp.set_title(
            'From 0 to ' + str(radii[i]) + '$R_e$ :: ' + str(spaxNum) + ' spaxel(s)', fontsize=fontsize)
        highInd = mF.findIndex(waveVec, 9300)
        axesTemp.set_ylim([0, max(ReSpectra[i][0:highInd])])
        axesTemp.set_xlim([min(waveVec), 9300])

        plt.xlabel(unitsX, fontsize=fontsize)
        plt.ylabel(unitsY, fontsize=fontsize)
        plt.xticks(fontsize=fontsize)
        plt.yticks(fontsize=fontsize)

    # fig.tight_layout()
    # plt.show()
    # print(jello)
    plt.savefig(nFP + plate_IFU + '_' + extraLabel +
                'SideBySideReSpectra.png', bbox_inches='tight')
    # print(jello)
    plt.close()


def plotStackedSpectra(plate_IFU, radii, waveVec, ReSpectra, dictRadiiSpaxNum, unitsX, unitsY, EADir, nFP, extraLabel=''):
    fontsize = 25
    legVec = []
    aspectRatio = 23.0 / 7
    height = 7
    fig = plt.figure(figsize=(aspectRatio * height, height))

    axes1 = plt.subplot(1, 2, 1)
    CAS_spectra(axes1, EADir, plate_IFU)

    axes2 = plt.subplot(1, 2, 2)
    axes2.set_title(plate_IFU, fontsize=fontsize)
    maxx = 0
    highInd = mF.findIndex(waveVec, 9300)
    for i in range(len(radii)):
        plt.plot(waveVec, ReSpectra[i])
        spaxNum = dictRadiiSpaxNum[radii[i]]
        legVec.append('R <= ' + str(radii[i]) +
                      '$R_e$ ' + str(spaxNum) + ' spaxel(s)')
        if max(ReSpectra[i][0:highInd]) > maxx:
            maxx = max(ReSpectra[i][0:highInd])

    plt.legend(legVec, fontsize=fontsize - 3, bbox_to_anchor=[1, 0.45])
    plt.xlabel(unitsX, fontsize=fontsize)
    plt.ylabel(unitsY, fontsize=fontsize)
    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)

    axes2.set_ylim([0, maxx])
    axes2.set_xlim([min(waveVec), 9300])

    fig.tight_layout()
    plt.show()
    #print(jello)
    plt.savefig(nFP + plate_IFU + '_' + extraLabel +
                'StackedReSpectra.png', bbox_inches='tight')
    # print(jello)
    plt.close()
