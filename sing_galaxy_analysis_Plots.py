# create plots for analysis of single galaxy

from plotGband_defaultFits import *
from plotD4000_LOGCUBE import *
import sys
import os

opts = []

if len(sys.argv) == 2:
    opts = ['linear', 'log', 'd4000', 'gband', 'bpt']
else:
    opts = [sys.argv[i].lower() for i in range(2, len(sys.argv))]

if 'log' in opts:
    if 'linear' in opts:
        LOGinput = 2
    else:
        LOGinput = 1
else:
    LOGinput = 0

if LOGinput == 0:
    LOGvec = [0]
elif LOGinput == 1:
    LOGvec = [1]
else:
    LOGvec = [0, 1]

print("")
print("Looking for .fits files in {" + sys.argv[1] + "}")
for file in os.listdir(sys.argv[1]):
    if 'bpt' in opts or 'gband' in opts:
        if (file.endswith("default.fits") or file.endswith("default.fits.gz")):
            if 'gband' in opts:
                for i in LOGvec:
                    if i == 0:
                        LOGstr = ' '
                    else:
                        LOGstr = ' LOG '
                    print("")
                    print("########################-Making GBand" + LOGstr +
                          "plots from " + file + "-########################")
                    plotGband_defaultFits(sys.argv[1] + file, i)

    if 'd4000' in opts and (file.endswith("LOGCUBE.fits") or
                            file.endswith("LOGCUBE.fits.gz")):
        print("")
        print("########################-Making D4000 plots from " +
              file + "-########################")
        plotD4000_LOGCUBE(sys.argv[1] + file)

if 'bpt' in opts:
    print("")
    print("BPT diagram in development, check back later")


# try:
#     fin = sys.argv[1]
# except IndexError:
#     print('Usage: python {0} mangadap-{{plate}}-{{ifu}}-default.fits.gz'
#           ''.format(sys.argv[0]))
#     sys.exit(1)
