import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from sys import argv
from matplotlib import rc
import dataCorrection as dC

script, filename=argv


def plotPipe3D(filename):
	temp=fits.open(filename)
	dataCube=temp[0].data

	for i in range(109):
	        print(str(i) + " -- " +
	              str(temp[0].header.keys()[i]) + " -- " + str(temp[0].header[i]))

	units={}
	desc={}
	ID={}
	for i in range(0,dataCube.shape[0]):
		for j in range(0, 109):
			if str(temp[0].header.keys()[j]).endswith(str(i)):
				if str(temp[0].header.keys()[j]).startswith("DES"):
					desc[i]=temp[0].header[j]
				if str(temp[0].header.keys()[j]).startswith("UNITS"):
					units[i]=temp[0].header.keys()[j]
				if str(temp[0].header.keys()[j]).startswith("ID"):
					ID[i]=temp[0].header[j]

	for i in range(0,dataCube.shape[0]):
		plt.figure()
		sliceMat = dC.flagOutsideZeros(dataCube[i])
		sliceMat=dC.flagHighValues(sliceMat, 10000)
		sliceMat=dC.flagOutlierValues(sliceMat, 10)
		sliceMat = dC.maskInvalidFlaggedVals(sliceMat)
		cmap1 = plt.cm.jet
		cmap1.set_bad('0.75')
		v_max=np.nanmax(sliceMat)
		v_min=np.nanmin(sliceMat)
		plt.pcolormesh(sliceMat, cmap=cmap1, vmin=v_min, vmax=v_max)
		plt.xlabel("spaxel")
		plt.ylabel("spaxel")
		plt.colorbar(cmap=cmap1)
		plt.title(desc[i])
	plt.show()

plotPipe3D(filename)