# create plots for analysis of single galaxy

from plotGband import *
from plotD4000 import *
from plotBPT import *
from plotWHAN import *
import sys
import direcFuncs as dF
import time

start = time.time()

opts = []

if len(sys.argv) == 2:
    opts = ['linear', 'log', 'd4000', 'gband', 'bpt', 'whan']
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

if 'bpt' in opts or 'gband' in opts or 'whan' in opts:
    for file in dF.locate("*default.fits", sys.argv[1]) + dF.locate("*default.fits.gz", sys.argv[1]):
        if 'gband' in opts:
            for i in LOGvec:
                if i == 0:
                    LOGstr = ' '
                else:
                    LOGstr = ' LOG '
                print("")
                print("##########-Making GBand" + LOGstr +
                      "plots from " + file + "-##########")
                plotGband(file, i)

        if 'bpt' in opts:
            print("")
            print("##########-Making BPT plots from " + file + "-##########")
            plotBPT(file)

        if 'whan' in opts:
            print("")
            print("##########-Making WHAN plots from " + file + "-##########")
            plotWHAN(file)

if 'd4000' in opts:
    for file in dF.locate("*LOGCUBE.fits", sys.argv[1]) + dF.locate("*LOGCUBE.fits.gz", sys.argv[1]):
        print("")
        print("##########-Making D4000 plots from " + file + "-##########")
        plotD4000(file)

end = time.time()
print("The time elapsed is " + str(end - start) + " seconds")
