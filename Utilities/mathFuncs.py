'''
Created on Sep 9, 2017

@author: Mande
'''
import numpy as np


def findIndex(vector, value):
    index = np.argmin(np.abs([v - value for v in vector]))
    return index


def createLineEquation(twoPoints):
    m = float(twoPoints[0][1] - twoPoints[1][1]) / \
        (twoPoints[0][0] - twoPoints[1][0])

    b = twoPoints[1][1] - m * twoPoints[1][0]

    return [m, b]


def calculateDistance(x1, y1, x2, y2):
    return np.sqrt(np.square(x2 - x1) + np.square(y2 - y1))