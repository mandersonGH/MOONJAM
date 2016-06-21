# create plots for analysis of single galaxy

from plotGband import *
from plotD4000 import *
from plotBPT import *
from plotWHAN import *
import sys
import direcFuncs as dF
import time


opts = []


def optsPrompt():
    print("")
    print("What diagrams would you like to produce for the .fits files in this directory?")
    print("")
    print("     For files ending in 'default.fits' or 'default.fits.gz':")
    print("")
    print("         GBand -- Spatial Resolution for the 11 most important emission lines")
    print("             Linear -- for linearly scaled plots")
    print("             LOG -- for LOG_10 scaled plots")
    print("         BPT -- BPT diagram")
    print("         WHAN -- WHAN diagram")
    print("")
    print("     For files ending in 'LOGCUBE.fits' or 'LOGCUBE.fits.gz':")
    print("")
    print("         D4000 -- Spatial Resolution of D4000")
    print("")
    print("Options Example: GBand Linear LOG WHAN")
    print("     This would produce linear and LOG_10 plots for GBand and also a WHAN diagram")
    print("")
    opts = raw_input("Please enter the options you would like: ")
    opts = opts.lower()
    if opts.find(' ') != -1:
        opts = opts.split(" ")
    return opts

if len(sys.argv) == 1:
    print("Welcome to the single galaxy analysis for MaNGA .fits file")
    print("Produced by MOONJAM")
    pwd = 'NO'
    while os.isdir(pwd) is False:
        pwd = raw_input(
            "Please enter the directory in which your .fits files are located: ")
    subAns = 'x'
    while subAns.upper() != 'Y' and subAns.upper() != 'N':
        subAns = raw_input(
            "Would you like to search subdirectories as well (Y/N)? ")
    opts = optsPrompt()
else:
    pwd = sys.argv[1]
    subAns = 'Y'
    if len(sys.argv) == 2:
        opts = ['linear', 'log', 'd4000', 'gband', 'bpt', 'whan']
    else:
        opts = [sys.argv[i].lower() for i in range(2, len(sys.argv))]

while 'bpt' not in opts and 'gband' not in opts and 'whan' not in opts and 'd4000' not in opts:
    opts = optsPrompt()

start = time.time()

if 'gband' in opts:
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


if subAns.upper() == 'Y':
    subBin = True
    subStrExt = " and its subfolders"
else:
    subBin = False
    subStrExt = ""

print("")
print("Looking for .fits files in {" + pwd + "}" + subStrExt)

if 'bpt' in opts or 'gband' in opts or 'whan' in opts:
    for file in dF.locate("*default.fits", subBin, pwd) + dF.locate("*default.fits.gz", subBin, pwd):
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
    for file in dF.locate("*LOGCUBE.fits", subBin, pwd) + dF.locate("*LOGCUBE.fits.gz", subBin, pwd):
        print("")
        print("##########-Making D4000 plots from " + file + "-##########")
        plotD4000(file)

end = time.time()
print("The time elapsed is " + str(end - start) + " seconds")
