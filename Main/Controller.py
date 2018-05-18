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

    def __init__(self, args):
        self.inputs = args

    def exitProgram(self, message):
        print("Program Error - Exiting...")
        print("    Error message : " + message)
        print("")
        sys.exit()

    def run(self):
        opts, EADirectory = self.obtainUserOptsInput()
        # EADirectory - where all plots and data are saved
        # opts - the arguments following the run command that dictate what
        # plots the user wants to produce

        if(not EADirectory or (not opts or len(opts) < 1)):
            self.exitProgram("Not enough inputs were supplied. Please specify the type of data you would like to generate plots for (e.g. MPL4 or MPL5) and the type of plots you would like")
        print()
        timer = Stopwatch()
        timer.start()
        fileDict = self.requiredFileSearch(opts, EADirectory)
        if not fileDict:
            self.exitProgram(
                r"No files were found in the directory supplied. The program will now close. Avoiding ending the directory with the character '\' and put the entire directory in quotes if there are any spaces in the path")
            timer.stop()
        else:
            print("")
            print('The program found this many .fits and .fits.gz files:  ' +
                  str(len(fileDict.items())))
            print("")
            self.makePLOTS(fileDict, opts, EADirectory)
            timer.stop()
            timer.reportDuration()

    def obtainUserOptsInput(self):
        opts = []
        try:
            EADirectory = self.inputs[1]
            del self.inputs[:2]
            for user_input in self.inputs:
                opts.append(user_input)
        except IndexError:
            self.exitProgram("No directory and/or plot type arguments supplied. Please read documentation of what arguments need to be supplied")
        except ValueError:
            # opts = initiateUserInterface()
            print("no user interface built")
            return None, None

        opts = [opt.lower() for opt in opts]
        return opts, os.path.abspath(EADirectory)

    def requiredFileSearch(self, opts, EADirectory):
        fileDict = defaultdict(list)
        print("")
        print('The program will search this directory for .fits and .fits.gz files:')
        if 'mpl4' in opts:
            print('     ' +     os.path.join(EADirectory, "MPL-4", "DATA", "DAP"))
            fileDict.update(self.makeFilePlotDict(
                opts,           os.path.join(EADirectory, "MPL-4", "DATA", "DAP"), self.dictMPL4files))
            if 'pipe3d' in opts:
                print('     ' + os.path.join(EADirectory, "MPL-4", "DATA", "PIPE3D"))
                fileDict.update(self.makeFilePlotDict(
                    opts,       os.path.join(EADirectory, "MPL-4", "DATA", "PIPE3D"), self.dictPIPE3Dfiles))
        if 'mpl5' in opts:
            print('     ' +     os.path.join(EADirectory, "MPL-5", "DATA", "DAP"))
            fileDict.update(self.makeFilePlotDict(
                opts,           os.path.join(EADirectory, "MPL-5", "DATA", "DAP"), self.dictMPL5files))
            if 'pipe3d' in opts:
                print('     ' + os.path.join(EADirectory, "MPL-5", "DATA", "PIPE3D"))
                fileDict.update(self.makeFilePlotDict(
                    opts,       os.path.join(EADirectory, "MPL-5", "DATA", "PIPE3D"), self.dictPIPE3Dfiles))
        print("")
        return fileDict

    def makeFilePlotDict(self, opts, EADirectory, dictFileTypes):
        filePlotDict = defaultdict(list)
        print("These are the types of plots you can create for this data source")
        for key in dictFileTypes.keys():
            print("   -" + key)
        for key in dictFileTypes.keys():
            if key in opts:
                print("You requested: " + key)
                fileType = dictFileTypes[key]
                fileList = dF.locate(fileType, True, rootD=EADirectory)
                fileList_gz = dF.locate(
                    fileType + '.gz', True, rootD=EADirectory)
                fileList_gz = [
                    x for x in fileList_gz if x[:-3] not in fileList]
                fileList = np.append(fileList, fileList_gz)
                for file in fileList:
                    filePlotDict[file].append(key)
        return filePlotDict

    def makePLOTS(self, fileDict, opts, EADirectory):
        for fileItemPair in fileDict.items():
            file = fileItemPair[0]
            print("")
            print('File:')
            print('     ' + file)
            print('Plots to create:')
            print('     ' + str(fileItemPair[1]))
            print("")

            galaxy = Galaxy(file, fits.open(file))
            plotsToBeCreated = fileItemPair[1]
            myPlottingController = plottingController(
                EADirectory, galaxy, plotsToBeCreated, opts)
            myPlottingController.run()
            galaxy.close()
