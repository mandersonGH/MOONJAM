'''
Created on Sep 8, 2017

@author: Mande
'''


class EmissionLineSlice(object):

    def __init__(self, galaxy, dataIndex, name, fancyName, units):
        self.myName = name
        self.myFancyName = fancyName
        self.myGalaxysPlateIfu = galaxy.PLATEIFU
        self.myData = galaxy.myDataCube[dataIndex]
        self.myMask = galaxy.myMaskCube[dataIndex]
        self.myError = galaxy.myErrorCube[dataIndex]
        self.myUnits = units

    def __str__(self):
        return self.myGalaxysPlateIfu + " :: " + self.myName