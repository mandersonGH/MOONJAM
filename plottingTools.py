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


def createAxis(plate_IFU, temp, i, dataType):
    IFU = plate_IFU.split("-")[1]
    fiberNo = int(IFU[:IFU.find('0')])

    dictFiber_Arcsec = {19: 12.5, 37: 17.5, 61: 22.5, 91: 27.5, 127: 32.5}
    # # to be done once axis labels are found
    # axis1_lbl = temp[i].header[17]
    # axis2_lbl = temp[i].header[18]

    NAXIS_vec, refPnt = pullSpecificInfo(temp, i)

    # axis1_n = tempHeader[3]
    # axis2_n = tempHeader[4]

    # if dataType is 'LOGCUBE':
    #     refPnt = [tempHeader[81], tempHeader[82]]
    # elif dataType is 'default':
    #     refPnt = [tempHeader[9], tempHeader[10]]
    # else:
    #     refPnt = [0, 0]

    axis1 = np.linspace(0, NAXIS_vec[0], NAXIS_vec[0] + 1) - refPnt[0]
    axis2 = np.linspace(0, NAXIS_vec[1], NAXIS_vec[1] + 1) - refPnt[1]

    # print(axis1_n)

    dx = (dictFiber_Arcsec[fiberNo] / (NAXIS_vec[0] + 1))
    dy = (dictFiber_Arcsec[fiberNo] / (NAXIS_vec[1] + 1))
    axis1 = axis1 * dx
    axis2 = axis2 * dy
    xmin = min(axis1)
    xmax = max(axis1)
    ymin = min(axis2)
    ymax = max(axis2)

    return np.meshgrid(np.arange(xmin, xmax + dx, dx) -
                       dx / 2., np.arange(ymin, ymax + dy, dy) - dy / 2.)


def calculateDistance(x1, y1, x2, y2):
    return np.sqrt(np.square(x2 - x1) + np.square(y2 - y1))


def createDistanceMatrix(dataShape, refPnt, SPAX):
    disMat = np.zeros(dataShape)
    for i in range(0, dataShape[0]):
        for j in range(0, dataShape[1]):
            disMat[i, j] = calculateDistance(
                i * SPAX[0], j * SPAX[1], refPnt[0] * SPAX[0], refPnt[1] * SPAX[1])

    return disMat


def findIndex(waveVec, wavelength):
    index = np.argmin(abs(waveVec - wavelength))
    return index


def pullGeneralInfo(prihdr, filename):
    if "PLATEIFU" in prihdr.keys():
        plate_IFU = prihdr[
            prihdr.keys().index("PLATEIFU")]
    elif ("PLATEID" in prihdr.keys()) and ("IFUDSGN" in prihdr.keys()):
        plate_IFU = str(prihdr[prihdr.keys().index("PLATEID")]) + \
            "-" + \
            str(prihdr[prihdr.keys().index("IFUDSGN")])
    else:
        plate_IFU = '-'.join((filename.split('/')
                              [-1]).split('.')[0].split('-')[1:3])

    if "SPAXDX" in prihdr.keys():
        SPAXD_vec = [prihdr[prihdr.keys().index(
            "SPAXDX")], prihdr[prihdr.keys().index("SPAXDY")]]
    else:
        SPAXD_vec = [0.5, 0.5]

    return plate_IFU, SPAXD_vec


def pullSpecificInfo(fitsFile, i):
    if "NAXIS1" in fitsFile[i].header.keys():
        NAXIS_vec = [fitsFile[i].header[fitsFile[i].header.keys().index(
            "NAXIS1")], fitsFile[i].header[fitsFile[i].header.keys().index("NAXIS2")]]
    else:
        NAXIS_vec = [fitsFile[i].data.shape[1], fitsFile[i].data.shape[2]]

    if "CRPIX1" in fitsFile[i].header.keys():
        refPnt = [fitsFile[i].header[fitsFile[i].header.keys().index("CRPIX1")], fitsFile[
            i].header[fitsFile[i].header.keys().index("CRPIX2")]]
    else:
        refPnt = [0, 0]

    return NAXIS_vec, refPnt
