import numpy as np
from collections import defaultdict
import os
import sys
import time
from astropy.io import fits

currentDirectory = os.path.dirname(os.path.abspath(__file__))
pythonDirectoryPathname = currentDirectory
sys.path.append(pythonDirectoryPathname + '/plots/PIPE3D')
sys.path.append(pythonDirectoryPathname + '/plots/DAP')

import direcFuncs as dF
from plotDAP import plotDAP
from plotPIPE3D import plotPIPE3D

dictPIPE3Dfiles = {'sfh': 'p_e.rad_SFH_lum_Mass.fits',
                   '_____': 'p_e.Sigma_Mass.fits',
                   'requested': '.cube.fits',
                   'lum_fracs': 'SFH.cube.fits',
                   'stellpops': 'SSP.cube.fits',
                   'flux_elines': '.cube.fits',
                   'indices.cs': '.cube.fits',
                   'elines': 'ELINES.cube.fits'}

dictMPL4files = {'bpt': 'default.fits',
                 'whan': 'default.fits',
                 'emlines_gflux': 'default.fits',
                 'emlines_ew': 'default.fits',
                 'respectra': 'LOGCUBE.fits'}

dictMPL5files = {'bpt': 'MAPS-SPX-GAU-MILESHC.fits',
                 'whan': 'MAPS-SPX-GAU-MILESHC.fits',
                 'emlines_gflux': 'MAPS-SPX-GAU-MILESHC.fits',
                 'emlines_ew': 'MAPS-SPX-GAU-MILESHC.fits',
                 'respectra': 'LOGCUBE-SPX-GAU-MILESHC.fits'}


def obtainUserOptsInput(inputs):
    opts = []
    try:
        EADirectory = inputs[1]
        del inputs[:2]
        for user_input in inputs:
            opts.append(user_input)
    except ValueError:
        # opts = initiateUserInterface()
        print("no user interface built")

    opts = [opt.lower() for opt in opts]

    return opts, EADirectory


def requiredFileSearch(opts, EADirectory):
    fileDict = defaultdict(list)
    if 'mpl4' in opts:
        fileDict.update(makeFilePlotDict(opts, EADirectory + "MPL-4\\DATA\\DAP\\", dictMPL4files))
        if 'pipe3d' in opts:
            fileDict.update(makeFilePlotDict(opts, EADirectory + "MPL-4\\DATA\\PIPE3D\\", dictPIPE3Dfiles))
    if 'mpl5' in opts:
#         print('MPL-5 not available yet')
        print('MPL-5 in development')
        fileDict.update(makeFilePlotDict(opts, EADirectory + "MPL-5\\DATA\\DAP\\", dictMPL5files))
        
    return fileDict


def makeFilePlotDict(opts, EADirectory, dictFileTypes):
    filePlotDict = defaultdict(list)
    for key in dictFileTypes.keys():
        if key in opts:
            fileType = dictFileTypes[key]
            fileList = dF.locate(fileType, True, rootD=EADirectory)
            fileList = np.append(fileList, dF.locate(fileType + '.gz', True, rootD=EADirectory))
            for file in fileList:
                filePlotDict[file].append(key)
    return filePlotDict


def makePLOTS(fileDict, opts, EADirectory):
    for fileItemPair in fileDict.items():
        file = fileItemPair[0]
        print("")
        print('File:')
        print('     ' + file)
        print('Plots to create:')
        print('     ' + str(fileItemPair[1]))
        print("")

        hdu = fits.open(file)
        # hdu.info()
        # for j in hdu[0].header.keys():
        #     print(str(j) + "  ::   " + str(hdu[0].header[j]))
        # print(jello)
        for plotType in fileItemPair[1]:
            if plotType in dictPIPE3Dfiles.keys():
                plotPIPE3D(file, plotType, hdu, EADirectory)
            if 'mpl4' in opts and plotType in dictMPL4files.keys():
                plotDAP(EADirectory, 'MPL-4', file, hdu, plotType)
            if 'mpl5' in opts and plotType in dictMPL5files.keys():
                plotDAP(EADirectory, 'MPL-5', file, hdu, plotType)

        hdu.close()

# opts, dataDirectory = obtainUserOptsInput(sys.argv)

inputs = ['', r'C:\Users\Miguel\Cloud Storage\Google Drive\2016 MOONJAM PROJECT\E + A Directory' + "\\",'mpl5','bpt']

# inputs = ['', r'C:\Users\Miguel\Cloud Storage\Google Drive\2016 MOONJAM PROJECT\E + A Directory' + "\\",'mpl4','bpt']


print("")
opts, EADirectory = obtainUserOptsInput(inputs)

print(EADirectory)

start = time.time()

fileDict = requiredFileSearch(opts, EADirectory)

makePLOTS(fileDict, opts, EADirectory)
end = time.time()
print("The time elapsed is " + str(round(end - start, 2)) + " seconds")
