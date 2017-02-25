from astropy.io import fits

# file = r'C:\Users\Miguel\Downloads\Chrome Downloads\manga-8979-1902-MAPS-SPX-GAU-MILESHC.fits.gz'
file = r'C:\Users\Miguel\Downloads\Chrome Downloads\manga-8979-1902-MAPS-ALL-GAU-MILESHC.fits.gz'

hdu = fits.open(file)
hdu.info()

print("")

for j in range(len(hdu[0].header.keys())):
    print(str(hdu[0].header.keys()[j]) + "  ::   " + str(hdu[0].header[j]))
    
print("")

for j in range(len(hdu[30].header.keys())):
    print(str(hdu[30].header.keys()[j]) + "  ::   " + str(hdu[30].header[j]))
