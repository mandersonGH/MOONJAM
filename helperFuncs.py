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


def calcHexGalShift(hex_at_Cen, gal_at_Cen, Re):
    return [float(gal_at_Cen[m] - hex_at_Cen[m]) / Re for m in range(len(gal_at_Cen))]


def findCompareOverlap(fileName1, fileName2):
    vec1 = fileName1.split(' ')
    vec2 = fileName2.split(' ')
    shorterLen = np.min([len(vec1), len(vec2)])
    cutInd = 0
    for i in range(1, shorterLen + 1):
        if vec1[-i] != vec2[-i]:
            cutInd = -i + 1
            break
    return ' '.join(vec1[cutInd:])


def ensureWideEnoughAxisRange(limits, currLimits, strict=False):
    x1 = limits[0]
    x2 = limits[1]
    y1 = limits[2]
    y2 = limits[3]

    if strict:
        return x1, x2, y1, y2
    else:
        xmin = currLimits[0]
        xmax = currLimits[1]
        ymin = currLimits[2]
        ymax = currLimits[3]

        if xmin > x1:
            xmin = x1

        if xmax < x2:
            xmax = x2

        if ymin > y1:
            ymin = y1

        if ymax < y2:
            ymax = y2

        return xmin, xmax, ymin, ymax
