Hello!

Welcome to MOONJAM!!

########################################

This program serves a single purpose. It creates and saves plots for galaxies surveryed by SDSS MaNGA MPL-4 and MPL-5. 

The aim of the program is to create plots of galaxies to figure out whether they are E+A galxaies or not.

This program can make WHAN Diagrams, BPT Diagrams, Spatially Resolved Emission Line plots, radial spectra plots, some PIPE3D plots and some FIREFLY plots.
	(PIPE3D and FIREFLY are spectral analysis programs created by Astronomers other this project)

########################################

This program was created by the MOONJAM team in the summer of 2016 during an REU Internship at the American Museum of Natural History. 

The contributers to the project are: (listed alphabetically and listed with their affliated institution at the time) 
Miguel Ricardo Anderson (Duke) 
Julia Falcone (Case Western) 
Olivia James (CUNY York College) 
Allen Liu (Harvard) 
Nicole Wallack (Caltech) 
Muhammad Wally (Xavier U. of Louisiana) 
Olivia Weaver (Florida Atlantic) 
Supervisor - Dr. Charles Liu (CUNY - Staten Island)

#########################################

Requirements to run:
 - Python (2.6 or later, there might be compatibility issues in Python 3 - this was not tested)
 - Astropy and several other additional python packages
 	(an installation of Anaconda will provide Python and all required packages)
 - A directory of .fits or fits.gz organized in a specific manner (see Directory Requirements)
 - An interest in the results!!
 
#########################################
 
Directory Requirements:

The directory must be organized with a specific hierarchy due to the saving mechanisms in the program.
1. The folders in the primary directory should be "CAS", "MPL-4" and "MPL-5". 
	 - "CAS" stores photos and single slit spectra of the galaxies in question. 
	 - "MPL-4" and "MPL-5" store everything from the corresponding data release format of MaNGA

2. The next level in the "MPL-4" and "MPL-5" folders should be, at the very least, a folder called "DATA"

3. Within the "DATA" folders there should be a folder for each data analysis tool used to extract data 
	- (examples: "DAP", "FIREFLY", "PIPE3D" and "SED")
	- There should also be a .fits file in here that begins with "drp". This file contains information about every galaxy in that data release and is very important in creating informative plots.
	
4. Within these folders, the next level should have a folder for each galaxy named with PLATE-IFU (ex: 7443-1902 or 8588-3704)
    - Note: the folders in the "CAS" should be of this level next. (i.e. opening the CAS folder should show a bunch of folders with PLATE-IFU numbers)

5. Within a galaxy's folder should be the .fits or .fits.gz file.

#######################################################
How to use the program:

1. Open command prompt
2. Change directory to the 