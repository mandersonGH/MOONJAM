from matplotlib.collections import RegularPolyCollection
import numpy as np


def plotHexagon(center, size, axes):

    offsets = center

    collection = RegularPolyCollection(
        # fig.dpi,
        6,  # a hexagon
        rotation=(np.pi / 180) * 30,  # rotated 30 degrees [in radians]
        sizes=(size,),
        facecolors='w',
        edgecolors='black',
        linewidths=(2,),
        offsets=offsets,
        transOffset=axes.transData,
    )
    axes.add_collection(collection)


def createAxis(fiberNo, tempHeader, dataType):
    dictFiber_Arcsec = {19: 12.5, 37: 17.5, 61: 22.5, 91: 27.5, 127: 32.5}
    # # to be done once axis labels are found
    # axis1_lbl = temp[i].header[17]
    # axis2_lbl = temp[i].header[18]

    if dataType is 'LOGCUBE':
        axis1_n = tempHeader[3]
        axis2_n = tempHeader[4]
        refPnt = [tempHeader[81], tempHeader[82]]
    elif dataType is 'default':
        axis1_n = tempHeader[3]
        axis2_n = tempHeader[4]
        refPnt = [tempHeader[9], tempHeader[10]]

    axis1 = np.linspace(0, axis1_n, axis1_n + 1) - refPnt[0]
    axis2 = np.linspace(0, axis2_n, axis2_n + 1) - refPnt[1]

    # print(axis1_n)

    dx = (dictFiber_Arcsec[fiberNo] / (axis1_n + 1))
    dy = (dictFiber_Arcsec[fiberNo] / (axis2_n + 1))
    axis1 = axis1 * dx
    axis2 = axis2 * dy
    xmin = min(axis1)
    xmax = max(axis1)
    ymin = min(axis2)
    ymax = max(axis2)

    return np.meshgrid(np.arange(xmin, xmax + dx, dx) -
                       dx / 2., np.arange(ymin, ymax + dy, dy) - dy / 2.)
