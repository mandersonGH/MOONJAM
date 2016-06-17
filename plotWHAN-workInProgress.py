#to supress printing warnings to screen
import warnings
warnings.filterwarnings("ignore")

#import statements 
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from sys import argv
from matplotlib import rc

#for taking in user inputed filename
script, filename=argv
temp=fits.open(filename)
#for splitting the filename 
name=filename.split('.')

#extract OIII and make into 1D array
OIII=temp[1].data[3]
OIII1D=OIII.reshape(1, OIII.size)

#extract Hb and make into 1D array
Hb=temp[1].data[1]
Hb1D=Hb.reshape(1, Hb.size)

#extract NII and make into 1D array
NII=temp[1].data[6]
NII1D=NII.reshape(1, NII.size)

#extract Ha and make into a 1D array
Ha=temp[1].data[7]
Ha1D=Ha.reshape(1, Ha.size)

# extract EW(Ha) and make into a 1D array
EWHa = temp[11].data[7]
EWHa1D = EWHa.reshape(1, EWHa.size)

#plot
logX=np.log(NII1D/Ha1D)
#for BPT
#logY=np.log(OIII1D/Hb1D)
#for WHAN
logY=np.log(EWHa1D)


#removing large X values
for i in range(0, logX.size):
	if (logX[:, i]> 20):
		logX[:, i] = np.NaN

#removing small X values
for i in range(0, logX.size):
	if (logX[:,i]<-20):
		logX[:, i] = np.NaN

#removing large Y values
for i in range(0, logY.size):
	if (logY[:, i]> 20):
		logY[:, i] = np.NaN

#removing small Y values 
for i in range(0, logY.size):
	if (logY[:,i]<-20):
		logY[:, i] = np.NaN

demarkX1=[-6, 6]
demarkY1=[.5, .5]
	
demarkX2=[-.4, -.4]
demarkY2=[.5,10]

#plot and save
plt.scatter(logX, logY)
plt.plot(demarkX1, demarkY1, 'k')
#plt.label("SF", -3, 7)
plt.plot(demarkX2, demarkY2, 'k')
plt.title("Spatially Resolved WHAN Diagram")
plt.ylabel("EW H${\\alpha}$")
plt.xlabel("log [NII]/H${\\alpha}$")
plt.ylim(-1,10)
plt.xlim(-6, 6)
plt.savefig(name[0]+'_BPT.png')
plt.show()