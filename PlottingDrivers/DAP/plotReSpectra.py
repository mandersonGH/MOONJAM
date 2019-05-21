'''
Created on Sep 8, 2017

@author: Mande
'''

import numpy as np
import os
import matplotlib.pyplot as plt

import Utilities.helperFuncs as hF
import Utilities.mathFuncs as mF
import Utilities.direcFuncs as dF
import GalaxyObject.fitsExtraction as fE
import PlottingTools.plottingTools as pT
from PlottingTools.plotFuncs import CAS_spectra

re_colors = ['olive', 'tomato', 'darkturquoise']

def plotReSpectra(EADir, galaxy, DAPtype, plotType, dataInd, dataCube, waveVec):
    print( galaxy.PLATEIFU)
    nFP = dF.assure_path_exists(os.path.join(
        EADir, DAPtype, 'PLOTS', 'DAP', galaxy.PLATEIFU, 'ReSpectra'))
    # unitsY = hdu[0].header['BUNIT']
    unitsX = '$\\lambda$ (Ang)'
    # unitsY = '$' + unitsY + '$'
    # unitsX = '$' + unitsX + '$'

    hex_at_Cen, gal_at_Cen = fE.getCenters(
        galaxy.myHDU, galaxy.PLATEIFU, dataInd)

    refPnt = [hex_at_Cen[1], hex_at_Cen[0]]

    radii_buckets = [
        (0,1),
        (1,2),
        (2,3)
    ]

    normed = True
    if normed:
        unitsY = '$f_{\\lambda}$ / $f_{5500 nm}$'
    else:
        unitsY = '$f_{\\lambda}$ ' + \
        ' (' + '$10^{-17}$' + 'erg/s/cm' + '$^{2}$' + '/Ang)'


    ReSpectraValues, dictRadiiSpaxNum = createRadiiRangesBuckets(
        waveVec, dataCube, radii_buckets, refPnt, galaxy.Re, normWavelength=5500 if normed else None)   

    # plotSideBySideSpectra(galaxy.PLATEIFU, radii_buckets, waveVec, ReSpectraValues, dictRadiiSpaxNum,
    #                    unitsX, unitsY, EADir, nFP, normed)
    plotSharingAxesSpectra(galaxy.PLATEIFU, radii_buckets, waveVec, ReSpectraValues, dictRadiiSpaxNum,
                       unitsX, unitsY, EADir, nFP, normed)
    # print(jello)

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

def createRadiiRangesBuckets(waveVec, dataCube, radiiRangeBounds, refPnt, Re, normWavelength=None):
    ReSpectra = []
    dictRadiiSpaxNum = {}
    for k in range(len(radiiRangeBounds)):
        ReSpectra.append(np.zeros(dataCube.shape[0]))

    for k in range(len(radiiRangeBounds)):
        count = 0
        for i in range(dataCube.shape[1]):
            for j in range(dataCube.shape[2]):
                
                RoverRe = mF.calculateDistance(refPnt[0], refPnt[1], i, j) / Re
                if radiiRangeBounds[k][0] < RoverRe and RoverRe <= radiiRangeBounds[k][1]:
                    count += 1
                    ReSpectra[k] = ReSpectra[k] + dataCube[:, i, j]
        dictRadiiSpaxNum[k] = count
        if normWavelength is not None:
            ReSpectra[k] = normalizeSpectra(
                waveVec, ReSpectra[k], normWavelength)
    return ReSpectra, dictRadiiSpaxNum

def plotSideBySideSpectra(plate_IFU, radii, waveVec, ReSpectra, dictRadiiSpaxNum, unitsX, unitsY, EADir, nFP, normed):
    fontsize = 30
    legVec = []
    aspectRatio = 4
    height = 19.0 / 2
    fig = plt.figure(figsize=(aspectRatio * height, height))

    for i in range(len(radii)):
        axesTemp = plt.subplot(1,3,i+1)

        plt.plot(waveVec, ReSpectra[i], color=re_colors[i])

        spaxNum = dictRadiiSpaxNum[i]
        axesTemp.set_title(
            'From '+str(radii[i][0] if i is not 0 else 0) +'$R_e$ to ' + str(radii[i][1]) + '$R_e$ :: ' + str(spaxNum) + ' spaxel(s)', fontsize=fontsize)
        highInd = mF.findIndex(waveVec, 9300)
        axesTemp.set_ylim([0, max(ReSpectra[i][0:highInd])])
        
        axesTemp.set_xlim([min(waveVec), 9300])

        if normed:
            axesTemp.set_ylim([0, 1.5])

        plt.xlabel(unitsX, fontsize=fontsize)
        plt.ylabel(unitsY, fontsize=fontsize)
        plt.xticks(fontsize=fontsize)
        plt.yticks(fontsize=fontsize)

    fig.tight_layout()
    # plt.show()
    # print(jello)
    plt.savefig(getPicFilename(nFP, plate_IFU, 'SideBySide', normed), bbox_inches='tight')
    # print(jello)
    plt.close()

def plotSharingAxesSpectra(plate_IFU, radii, waveVec, ReSpectra, dictRadiiSpaxNum, unitsX, unitsY, EADir, nFP, normed):
    thin = True
    fontsize = 25
    legVec = []
    aspectRatio = 23.0 / (7 if not thin else 14)
    height = 7
    fig = plt.figure(figsize=(aspectRatio * height, height))

    # axes1 = plt.subplot(1, 2, 1)
    # try:
    #     CAS_spectra(axes1, EADir, plate_IFU)
    # except:
    #     print('no image')

    axes2 = plt.subplot(1, 1, 1)
    axes2.set_title(plate_IFU, fontsize=fontsize)
    maxx = 0
    highInd = mF.findIndex(waveVec, 9300)
    for i in range(len(radii)):
        plt.plot(waveVec, ReSpectra[i], color=re_colors[i])
        spaxNum = dictRadiiSpaxNum[i]
        legVec.append(str(radii[i][0]) + ' < ' + 
                      'R/$R_e$ <= ' + str(radii[i][1]) +
                      ' '+ str(spaxNum) + ' spaxel(s)')
        if max(ReSpectra[i][0:highInd]) > maxx:
            maxx = max(ReSpectra[i][0:highInd])


    axes2.set_xlim([min(waveVec), 9300])
    axes2.set_ylim([0, 1.5 if normed else maxx])

    if normed or thin:
        plt.legend(legVec, fontsize=fontsize - 10, loc=0, borderaxespad=0.1)
    else:
        plt.legend(legVec, fontsize=fontsize - 3, bbox_to_anchor=(1.05, 1.05), loc=1, borderaxespad=0.)

    plt.xlabel(unitsX, fontsize=fontsize)
    plt.ylabel(unitsY, fontsize=fontsize)
    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)

    fig.tight_layout()
    # plt.show()
    # print(jello)
    plt.savefig(getPicFilename(nFP, plate_IFU, 'Sharing', normed, '' if not thin else '_Thin'), bbox_inches='tight')
    # print(jello)
    plt.close()

def getPicFilename(nFP, plate_IFU, pType, normed, suffix):
    return os.path.join(nFP, plate_IFU + '_' + pType + '_' + ('' if normed else 'Not') + 'Normed_ReSpectra'+suffix+'.png')
