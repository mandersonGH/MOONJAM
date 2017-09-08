import numpy as np

from astropy.io import fits

from EA_data import *


def getNAXIS(hdu, dataInd):
    if "NAXIS1" in hdu[dataInd].header.keys():
        NAXIS_vec = [hdu[dataInd].header["NAXIS1"],
                     hdu[dataInd].header["NAXIS2"]]
    else:
        NAXIS_vec = [hdu[dataInd].data.shape[1], hdu[dataInd].data.shape[2]]

    return NAXIS_vec


def pullPLATEIFU(prihdr, filename):
    if "PLATEIFU" in prihdr.keys():
        plate_IFU = prihdr["PLATEIFU"]
    elif ("PLATEID" in prihdr.keys()) and ("IFUDSGN" in prihdr.keys()):
        plate_IFU = str(prihdr["PLATEID"]) + "-" + str(prihdr["IFUDSGN"])
    else:
        deComposedFilename = filename.split('/')[-1].split('.')
        partwith_plate_IFU = ''
        for part in deComposedFilename:
            if part.startswith('manga'):
                partwith_plate_IFU = part
                break

        plate_IFU = '-'.join(partwith_plate_IFU.split('-')[1:])

    return plate_IFU


def getCenters(hdu, plate_IFU, dataInd):

    if "CRPIX1" in hdu[dataInd].header.keys():
        gal_at_Cen = [hdu[dataInd].header['CRPIX1'],
                      hdu[dataInd].header['CRPIX2']]
    else:
        NAXIS_vec = getNAXIS(hdu, dataInd)
        gal_at_Cen = [np.round(NAXIS_vec[0] / 2), np.round(NAXIS_vec[1] / 2)]

    try:
        hex_at_Cen = dictCenters[plate_IFU]
    except KeyError:
        hex_at_Cen = gal_at_Cen

    return hex_at_Cen, gal_at_Cen


def getRe(EADir, DAPtype, plate_IFU):
    drpallFilename = ""
    if DAPtype == "MPL-4":
        drpallFilename = 'drpall-v1_5_1.fits'
    elif DAPtype == "MPL-5":
        drpallFilename = 'drpall-v2_0_1.fits'

    drpallFile = EADir + DAPtype + '/DATA/' + drpallFilename

    try:
        print(drpallFile)
        drpall = fits.open(drpallFile)

        for i in range(1, len(drpall[1].data[0]) + 1):
            if 'nsa_petro_th50' == str(drpall[1].header['TTYPE' + str(i)]):
                ReCol = i - 1
                break

        for i in range(0, len(drpall[1].data)):
            if drpall[1].data[i][2] == plate_IFU:
                Re = drpall[1].data[i][ReCol]
                # effective radius in arcsec
                break

        drpall.close()
    except TypeError:
        Re = 10
    return Re


def getNAXIS3(hdu):
    if hdu[0].header['NAXIS'] != 3:
        NAXIS3 = 0
    else:
        NAXIS3 = hdu[0].header["NAXIS3"]
    return NAXIS3


def getTitleHeaderPrefix(hdu):
    if 'NAME1' in hdu[0].header.keys():
        titleHdr = "NAME"
    elif 'INDEX1' in hdu[0].header.keys():
        titleHdr = "INDEX"
    else:
        titleHdr = "DESC_"

    return titleHdr
