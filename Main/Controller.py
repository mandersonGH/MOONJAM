'''
Created on Sep 8, 2017

@author: Mande
'''
import numpy as np
from Utilities.Stopwatch import Stopwatch
from collections import defaultdict
import direcFuncs as dF
from astropy.io import fits
from GalaxyObject.Galaxy import Galaxy
from Plotting.plottingController import plottingController


class Controller:

    dictMPL4files = eval(open("../resources/dictMPL4files.txt").read())
    dictMPL5files = eval(open("../resources/dictMPL5files.txt").read())
    dictPIPE3Dfiles = eval(open("../resources/dictPIPE3Dfiles.txt").read())

    def __init__(self, args):
        self.inputs = args

    def run(self):
        opts, EADirectory = self.obtainUserOptsInput()
        # EADirectory - where all plots and data are saved
        # opts - the arguments following the run command that dictate what
        # plots the user wants to produce

        timer = Stopwatch()
        timer.start()
        fileDict = self.requiredFileSearch(opts, EADirectory)
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
            print("No extra arguments supplied")
        except ValueError:
            # opts = initiateUserInterface()
            print("no user interface built")

        opts = [opt.lower() for opt in opts]
        return opts, EADirectory

    def requiredFileSearch(self, opts, EADirectory):
        fileDict = defaultdict(list)
        if 'mpl4' in opts:
            fileDict.update(self.makeFilePlotDict(
                opts, EADirectory + "MPL-4\\DATA\\DAP\\", self.dictMPL4files))
            if 'pipe3d' in opts:
                fileDict.update(self.makeFilePlotDict(
                    opts, EADirectory + "MPL-4\\DATA\\PIPE3D\\", self.dictPIPE3Dfiles))
        if 'mpl5' in opts:
            fileDict.update(self.makeFilePlotDict(
                opts, EADirectory + "MPL-5\\DATA\\DAP\\", self.dictMPL5files))

        return fileDict

    def makeFilePlotDict(self, opts, EADirectory, dictFileTypes):
        filePlotDict = defaultdict(list)
        for key in dictFileTypes.keys():
            if key in opts:
                fileType = dictFileTypes[key]
                fileList = dF.locate(fileType, True, rootD=EADirectory)
                fileList_gz = dF.locate(fileType + '.gz', True, rootD=EADirectory)
                fileList_gz = [x for x in fileList_gz if x[:-3] not in fileList]
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
