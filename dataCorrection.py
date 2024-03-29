# data correction
import numpy as np
import matplotlib.pyplot as plt


def zeroOutNegatives(dataIn):
    dataIn[dataIn < 0] = 0
    return dataIn


def flagOutsideZeros(dataIn):
    for i in range(0, dataIn.shape[0]):
        flag = False
        for j in range(0, dataIn.shape[1]):
            if flag is True:
                break
            if dataIn[i, j] != 0:
                for jj in range(dataIn.shape[1] - 1, j - 1, -1):
                    if dataIn[i, jj] != 0:
                        flag = True
                        dataIn[i, :j] = np.NaN
                        dataIn[i, jj:] = np.NaN
                        break
            if j == dataIn.shape[1] - 1:
                flag = True
                dataIn[i, :] = np.NaN
                break
    return dataIn


def flagHighValues(dataIn, value):
    dataIn[abs(dataIn) > value] = np.NaN
    return dataIn


def flagOutlierValues(dataIn, devs):
    dataIn[dataIn > np.nanmean(dataIn) + devs * np.nanstd(dataIn)] = np.NaN
    dataIn[dataIn < np.nanmean(dataIn) - devs * np.nanstd(dataIn)] = np.NaN
    return dataIn


def maskInvalidFlaggedVals(dataIn):
    dataIn = np.ma.masked_invalid(dataIn)
    return dataIn


def checkFreqHisto(dataIn, title):
    plt.figure()
    plt.hist(dataIn[~np.isnan(dataIn)], bins=np.arange(
        np.nanmin(dataIn), np.nanmax(dataIn) + 1, 1))
    plt.title(title)


def pickVMIN(dataIn, devs):
    try:
        if np.nanmean(dataIn) - devs * np.nanstd(dataIn) < np.nanmin(dataIn):
            return np.nanmin(dataIn)
        else:
            return np.nanmean(dataIn) - devs * np.nanstd(dataIn)
    except ValueError:
        return 1


def pickVMAX(dataIn, devs):
    try:
        if np.nanmean(dataIn) + devs * np.nanstd(dataIn) > np.nanmax(dataIn):
            return np.nanmax(dataIn)
        else:
            return np.nanmean(dataIn) + devs * np.nanstd(dataIn)
    except ValueError:
        return 1


def printDataInfo(dataIn):
    print("   min/max [" + str(np.nanmin(dataIn)) +
          ", " + str(np.nanmax(dataIn)) + "]")
    print("   avg " + str(np.nanmean(dataIn)))
    print("   std " + str(np.nanstd(dataIn)))
