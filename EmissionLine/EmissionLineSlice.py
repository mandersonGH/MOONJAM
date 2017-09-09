'''
Created on Sep 8, 2017

@author: Mande
'''


class EmissionLineSlice(object):

    def setName(self, name):
        self.myName = name

    def setFancyName(self, fancyName):
        self.myFancyName = fancyName

    def setData(self, data):
        self.myData = data

    def setMask(self, mask):
        self.myMask = mask

    def setError(self, error):
        self.myError = error

    def setUnits(self, units):
        self.myUnits = units