'''
Created on Sep 8, 2017

@author: Mande
'''

import direcFuncs as dF
import plottingTools as pT
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
from astropy.io.fits.verify import VerifyError, VerifyWarning

times = [1.00E+06,
         3.00E+06,
         3.98E+06,
         5.62E+06,
         8.91E+06,
         1.00E+07,
         1.26E+07,
         1.41E+07,
         1.78E+07,
         2.00E+07,
         2.51E+07,
         3.16E+07,
         3.98E+07,
         5.62E+07,
         6.30E+07,
         6.31E+07,
         7.08E+07,
         1.00E+08,
         1.12E+08,
         1.26E+08,
         1.59E+08,
         2.00E+08,
         2.82E+08,
         3.55E+08,
         5.01E+08,
         7.08E+08,
         8.91E+08,
         1.12E+09,
         1.26E+09,
         1.41E+09,
         2.00E+09,
         2.51E+09,
         3.55E+09,
         4.47E+09,
         6.31E+09,
         7.94E+09,
         1.00E+10,
         1.26E+10,
         1.41E+10]


def plotSFH(EADir, galaxy):
    nFP = dF.assure_path_exists(EADir + '/PLOTS/PIPE3D/SFH/')

    dCube = galaxy.myHDU[0].data

    plt.figure(figsize=(15, 9))

    if galaxy.myFilename.startswith('sigma') or galaxy.myFilename.startswith('comp'):
        plt.imshow(dCube, extent=[6, 10, 3.6, 0], aspect='auto')
    else:
        axMain = plt.subplot(2, 3, 2)
        mask = np.zeros(dCube.shape)
        mask[dCube < -100000] = 1
        for j in reversed(range(dCube.shape[0])):
            if np.sum(mask[j, :]) != dCube.shape[1]:
                maxRe = float(j) / 10 + .2
                # print(maxRe)
                break
        masked_image = np.ma.array(dCube, mask=mask)
        plt.imshow(masked_image, vmin=-3,
                   extent=[6, 10, 3.6, 0], aspect='auto')
    plt.suptitle(galaxy.myFilename)

    plt.ylabel('$R/R_e$')
    plt.xlabel("Age log(yr)")
    cbar = plt.colorbar()
    cbar.set_label('$log(M_{sun}/pc^2)$')

    if not galaxy.myFilename.startswith('sigma') and not galaxy.myFilename.startswith('comp'):
        timeVec = [10, 17, 25]

        for ii in range(3):
            titleStr = 'From log(yr)=' + str(np.log10(times[0])) + ' to log(yr)=' + str(
                np.round(np.log10(times[timeVec[ii]]), 2))
            tempVec = []
            ReVec = []
            for j in reversed(range(dCube.shape[0])):
                ReVec.append(float(j) / 10)
                tempVec.append(np.sum(10**dCube[j, :timeVec[ii]]))
            if ii == 0:
                ax1 = plt.subplot(2, 3, ii + 4, sharey=axMain)
                ax1.set_title(titleStr, fontsize=10)
            else:
                axElse = plt.subplot(2, 3, ii + 4, sharey=axMain)
                axElse.set_title(titleStr, fontsize=10)
            plt.plot(tempVec, ReVec)
            plt.ylabel('$R/R_e$')
            plt.xlabel('Summed Stellar Mass Density ' +
                       '$M_{sun}/pc^2$', fontsize=8)
            plt.ylim([maxRe, 0])

    plt.savefig(nFP + galaxy.myFilename + '.png')
