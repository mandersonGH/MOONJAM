# to supress printing warnings to screen
import warnings
warnings.filterwarnings("ignore")

#import statements
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from matplotlib import rc
import os


def plotBPT(filename):

    temp = fits.open(filename)

    nFP = setupNewDir(filename, "")

    # for splitting the filename
    name = (filename.split('/')[-1]).split('.')[0]
    name_plateNum_Bundle = '-'.join(name.split('-')[1:3])

    # Taking data from GFlux
    headerInd = 1

    # extract OIII and make into 1D array
    OIII = temp[headerInd].data[3]
    OIII1D = OIII.reshape(1, OIII.size)

    # extract Hb and make into 1D array
    Hb = temp[headerInd].data[1]
    Hb1D = Hb.reshape(1, Hb.size)

    # extract NII and make into 1D array
    NII = temp[headerInd].data[6]
    NII1D = NII.reshape(1, NII.size)

    # extract Ha and make into a 1D array
    Ha = temp[headerInd].data[7]
    Ha1D = Ha.reshape(1, Ha.size)

    # plot
    logX = np.log(NII1D / Ha1D)
    logY = np.log(OIII1D / Hb1D)

    # removing large and small X values
    logX[abs(logX) > 20] = np.NaN

    # removing large and small Y values
    logY[abs(logY) > 20] = np.NaN

    #plot and save
    plt.figure()
    plt.scatter(logX, logY)
    plt.title("Spatially Resolved BPT Diagram -- " + name)
    plt.xlabel("log [NII]/H${\\alpha}$")
    plt.ylabel("log [OIII]/H${\\beta}$")
    plt.savefig(nFP + name_plateNum_Bundle + '_BPT.png')
    # plt.show()
    plt.close()


def setupNewDir(filename, typeStr):
    # ensures new folder
    # sets up folder path for new files
    fileLs = filename.split('/')
    # newFldrNme = fileLs[-1]
    del fileLs[-1]

    newFldrPath = '/'.join(fileLs) + '/Figures/BPT' + typeStr + '/'
    assure_path_exists(newFldrPath)

    return newFldrPath


def assure_path_exists(path):
    # from
    # https://justgagan.wordpress.com/2010/09/22/python-create-path-or-directories-if-not-exist/
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)
        print("New directory made {" + dir + "/}")
