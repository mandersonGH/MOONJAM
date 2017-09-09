'''
Created on Sep 8, 2017

@author: Mande
'''
import abc

class PlotterABC(object):
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def plot(self, direc, galaxy, plotType):
        """Create and save plots of a certain type, of a certain galaxy in a certain directory."""
        return
    