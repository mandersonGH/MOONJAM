Verison 6 - 6/21/2016
AMNH - MOONJAM

This is the single galaxy analysis of data from the MaNGA galaxies in DR13 of SDSS IV.

The code can use files that end with 'default.fits', 'default.fits.gz', 'LOGCUBE.fits', or 'LOGCUBE.fits.gz'

The code can be run in two modes:

1) Simple:

	To do this type 'ipython' followed by the file 'sing_Run.py' into the terminal and following the printed commands. 
	Example:
	$ ipython ./Google\ Drive/2016\ MOONJAM\ PROJECT/Software/Python/Single_Galaxy_Analysis/sing_Run.py

2) Advanced:

	Type 'ipython', followed by 'sing_Run.py', followed by the directory that the '.fits' files are located.
	Example:
	$ ipython ./Google\ Drive/2016\ MOONJAM\ PROJECT/Software/Python/Single_Galaxy_Analysis/sing_Run.py ./Google\ Drive/2016\ MOONJAM\ PROJECT/GALAXY\ CLASSIFICATIONS/

	In this mode all analysis plots will be created but you can add options after this to limit the analysis.
	Example:
	$ ipython ./Google\ Drive/2016\ MOONJAM\ PROJECT/Software/Python/Single_Galaxy_Analysis/sing_Run.py ./Google\ Drive/2016\ MOONJAM\ PROJECT/GALAXY\ CLASSIFICATIONS/ GBand WHAN BPT
		- this will produce GBand, WHAN and BPT plots