# to supress printing warnings to screen
import warnings
warnings.filterwarnings("ignore")

#import statements
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from sys import argv
from matplotlib import rc

# for taking in user inputed filename
script, filename = argv
temp = fits.open(filename)
# for splitting the filename
name = (filename.split('/')[-1]).split('.')
name_plateNum_Bundle = '-'.join(name[0].split('-')[1:3])

# extract OIII and make into 1D array
OIII = temp[1].data[3]
OIII1D = OIII.reshape(1, OIII.size)

# extract Hb and make into 1D array
Hb = temp[1].data[1]
Hb1D = Hb.reshape(1, Hb.size)

# extract NII and make into 1D array
NII = temp[1].data[6]
NII1D = NII.reshape(1, NII.size)

# extract Ha and make into a 1D array
Ha = temp[1].data[7]
Ha1D = Ha.reshape(1, Ha.size)

# plot
logX = np.log(NII1D / Ha1D)
logY = np.log(OIII1D / Hb1D)

# removing large X values
for i in range(0, logX.size):
    if (logX[:, i] > 20):
        logX[:, i] = np.NaN

# removing small X values
for i in range(0, logX.size):
    if (logX[:, i] < -20):
        logX[:, i] = np.NaN

# removing large Y values
for i in range(0, logY.size):
    if (logY[:, i] > 20):
        logY[:, i] = np.NaN

# removing small Y values
for i in range(0, logY.size):
    if (logY[:, i] < -20):
        logY[:, i] = np.NaN

#plot and save
plt.scatter(logX, logY)
plt.title("Spatially Resolved BPT Diagram")
plt.xlabel("log [NII]/H${\\alpha}$")
plt.ylabel("log [OIII]/H${\\beta}$")
plt.savefig(name_plateNum_Bundle + '_BPT.png')
plt.show()
