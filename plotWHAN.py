# to supress printing warnings to screen
import warnings
warnings.filterwarnings("ignore")

# import statements
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import direcFuncs as dF
import plottingTools as pT


def plotWHAN(filename):

    hdu = fits.open(filename)
    # temp.info()
    # for i in range(0, 10):
    #     print(temp[i].header.keys)

    nFP = dF.setupNewDir(filename, "", 'WHAN')

    plate_IFU, SPAXD_vec = pT.pullGeneralInfo(hdu[0].header, filename)

    # Taking data from GFlux
    headerInd = 1

    NAXIS_vec, refPnt = pT.pullSpecificInfo(hdu, headerInd)

    dMat = pT.createDistanceMatrix(NAXIS_vec, refPnt, SPAXD_vec)

    # extract NII and make into 1D array
    NII = hdu[headerInd].data[6]
    NII1D = NII.reshape(1, NII.size)

    # extract Ha and make into a 1D array
    Ha = hdu[headerInd].data[7]
    Ha1D = Ha.reshape(1, Ha.size)

    # Taking data from EW
    headerInd = 11

    # extract EW(Ha) and make into a 1D array
    EWHa = hdu[headerInd].data[7]
    EWHa1D = EWHa.reshape(1, EWHa.size)

    # plot
    logX = np.log(NII1D / Ha1D)
    logY = np.log(EWHa1D)

    # removing large and small X values
    logX[abs(logX) > 20] = np.NaN

    # removing large and small Y values
    logY[abs(logY) > 20] = np.NaN

    # plot and save
    plt.figure()
    plt.scatter(logX, logY, c=dMat, cmap=plt.cm.plasma)
    cbar = plt.colorbar()
    cbar.set_label("arcsec from center")
    axes = plt.gca()
    xmin, xmax = axes.get_xlim()
    ymin, ymax = axes.get_ylim()

    # demarkations
    demarkX1 = [xmin, xmax]
    demarkY1 = [.5, .5]
    demarkX2 = [-.4, -.4]
    demarkY2 = [.5, ymax]

    plt.plot(demarkX1, demarkY1, 'k')
    plt.plot(demarkX2, demarkY2, 'k')
    plt.xlim([xmin, xmax])
    plt.ylim([ymin, ymax])
    plt.title("WHAN Diagram")
    plt.xlabel("log [NII]/H${\\alpha}$")
    plt.ylabel("log EW(H${\\alpha}$)")
    plt.annotate('SF', xy=((-0.4 + xmin) / 2, (0.5 + ymax) * 0.75))
    plt.annotate('AGN', xy=((-0.4 + xmax) / 2, (0.5 + ymax) * 0.75))
    plt.annotate('Old Stars', xy=((xmin + xmax) * 0.5, (ymin + 0.5) * 0.25))
    plt.annotate("Plate-IFU: " + plate_IFU, xy=(xmin +
                                                           (xmax - xmin) * 0.02, ymin + (ymax - ymin) * 0.02), size=10)
    plt.savefig(nFP + plate_IFU + '_WHAN.png', bbox_inches='tight')
    # plt.show()
    plt.close()
