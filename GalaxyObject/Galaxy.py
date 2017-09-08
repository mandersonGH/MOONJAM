'''
Created on Sep 8, 2017

@author: Mande
'''

import direcFuncs as dF
import GalaxyObject.fitsExtraction as fE

class Galaxy():
    '''
    classdocs
    '''
    
    def __init__(self, file, hdu):
        self.myCompleteFilePath = file
        self.myFilename = dF.getFilename(self.myCompleteFilePath)
        self.myHDU = hdu
        #self.printInfo()
        
        self.pullInfo()
        
    def printInfo(self):
        self.myHDU.info()
        for j in self.myHDU[0].header.keys():
            print(str(j) + "  ::   " + str(self.myHDU[0].header[j]))
        print(jello)
        
        
    def pullInfo(self):
        self.pullPLATEIFU()
        
        
    def pullPLATEIFU(self):
        self.PLATEIFU = fE.pullPLATEIFU(self.myHDU[0].header, self.myFilename)
        
    def pullRe(self, EADirectory,  DAPtype):
        self.Re = fE.getRe(EADirectory, DAPtype, self.PLATEIFU)
        
    def setCenterType(self, centerType):
        self.myCenterType = centerType
        
    def extractDataCubes(self, dataInd, errInd, maskInd):
        self.myDataCube = self.myHDU[dataInd].data
        self.myErrorCube = self.myHDU[errInd].data
        self.myMaskCube = self.myHDU[maskInd].data
     
    def close(self):
        self.myHDU.close()