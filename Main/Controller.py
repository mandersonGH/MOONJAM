'''
Created on Sep 8, 2017

@author: Mande
'''
import numpy as np
from Utilities.Stopwatch import Stopwatch
from collections import defaultdict
import Utilities.direcFuncs as dF
from astropy.io import fits
from GalaxyObject.Galaxy import Galaxy
from PlottingDrivers.plottingController import plottingController
import os
import sys


class Controller:

    resourceFolder = os.path.join(os.path.abspath(
        os.path.join(__file__, "..", "..")), "resources")

    dictMPL4files = eval(
        open(os.path.join(resourceFolder, "dictMPL4files.txt")).read())
    dictMPL5files = eval(
        open(os.path.join(resourceFolder, "dictMPL5files.txt")).read())
    dictPIPE3Dfiles = eval(
        open(os.path.join(resourceFolder, "dictPIPE3Dfiles.txt")).read())

    def __init__(self, ea_directory, data_versions, requested_plots):
        self.ea_directory = ea_directory
        self.data_versions = data_versions
        self.requested_plots = requested_plots

    def exitProgram(self, message):
        print("Program Error - Exiting...")
        print("    Error message : " + message)
        print("")
        sys.exit()

    def run(self):
        print()
        timer = Stopwatch()
        timer.start()
        fileDict = self.requiredFileSearch(self.ea_directory, self.data_versions, self.requested_plots)
        if not fileDict:
            timer.stop()
            self.exitProgram(
                r"No files were found in the directory supplied to create the plots you requested. The program will now close. Avoiding ending the directory with the character '\' and put the entire directory in quotes if there are any spaces in the path")
        print("")
        print('The program found this many .fits and .fits.gz files:  ' +
              str(len(fileDict.items())))
        print("")
        self.makePLOTS(fileDict, self.data_versions, self.ea_directory)
        timer.stop()
        timer.reportDuration()

    def requiredFileSearch(self, EADirectory, data_versions, requested_plots):
        fileDict = defaultdict(list)
        print("")
        print('The program will search this directory for .fits and .fits.gz files:')
        if 'mpl4' in data_versions:
            print('     ' +     os.path.join(EADirectory, "MPL-4", "DATA", "DAP"))
            fileDict.update(self.makeFilePlotDict(requested_plots,
                                os.path.join(EADirectory, "MPL-4", "DATA", "DAP"), self.dictMPL4files))
            if 'pipe3d' in data_versions:
                print('     ' + os.path.join(EADirectory, "MPL-4", "DATA", "PIPE3D"))
                fileDict.update(self.makeFilePlotDict(requested_plots,
                                os.path.join(EADirectory, "MPL-4", "DATA", "PIPE3D"), self.dictPIPE3Dfiles))
        if 'mpl5' in data_versions:
            print('     ' +     os.path.join(EADirectory, "MPL-5", "DATA", "DAP"))
            fileDict.update(self.makeFilePlotDict(requested_plots,
                                os.path.join(EADirectory, "MPL-5", "DATA", "DAP"), self.dictMPL5files))
            if 'pipe3d' in data_versions:
                print('     ' + os.path.join(EADirectory, "MPL-5", "DATA", "PIPE3D"))
                fileDict.update(self.makeFilePlotDict(requested_plots,
                                os.path.join(EADirectory, "MPL-5", "DATA", "PIPE3D"), self.dictPIPE3Dfiles))
        print("")
        return fileDict

    def makeFilePlotDict(self, requested_plots, EADirectory, dictFileTypes):
        filePlotDict = defaultdict(list)
        print("These are the types of plots you can create for this data source")
        for plot_type in dictFileTypes.keys():
            print("   -" + plot_type)
        for plot_type in dictFileTypes.keys():
            if plot_type in requested_plots:
                print("You requested: " + plot_type)
                fileType = dictFileTypes[plot_type]
                fileList = dF.locate(fileType, True, rootD=EADirectory)
                fileList_gz = dF.locate(
                    fileType + '.gz', True, rootD=EADirectory)
                fileList_gz = [
                    x for x in fileList_gz if x[:-3] not in fileList]
                fileList = np.append(fileList, fileList_gz)
                for file in fileList:
                    filePlotDict[file].append(plot_type)
        return filePlotDict

    def makePLOTS(self, fileDict, data_versions, EADirectory):
        for fileItemPair in fileDict.items():
            file = fileItemPair[0]
            plotsToBeCreated = fileItemPair[1]
            # print("")
            # print('File:')
            # print('     ' + file)
            # print('Plots to create:')
            # print('     ' + str(plotsToBeCreated))
            # print("")

            galaxy = Galaxy(file, fits.open(file))
            myPlottingController = plottingController(
                EADirectory, galaxy, plotsToBeCreated, data_versions)
            myPlottingController.run()
            galaxy.close()
