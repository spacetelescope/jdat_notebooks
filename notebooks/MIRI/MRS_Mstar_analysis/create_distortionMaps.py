"""
Function to create cube coordinate maps on detector, based on detector pixel coordinates ("d2c maps")
The function uses the distortion maps described in MIRI-TN-00001-ETH
The output is a single dictionary with:
          * one map of slice identifiers for each detector pixel
          * one map of spectral (wavelength) coordinates at detector pixel centers
          * five maps of along-slice ("alpha") spatial coordinates (at center and four corners of each detector pixel)
          * five maps of across-slice ("beta") spatial coordinates (at center and four corners of each detector pixel)
          * the start value of the across-slice spatial coordinate ("bzero") and the width of a slice ("bdel")

Creation date: February 2017

Original code author: Dr. Bart Vandenbussche (Institute of Astronomy, KU Leuven)
Code edited by Ioannis Argyriou (Institute of Astronomy, KU Leuven)

=============EXAMPLE OF USE:===============
# import function to desired script
from distortionMaps import d2cMapping

# Give directory where distortion cdps are located
cdpDir   = '/PATH/TO/CDP_DATA/'

# choose spectral band
band = '2A'

# make dictionary containing all cube coordinate maps
d2cMaps = d2cMapping(band,cdpDir)

# plot wavelength map
import matplotlib.pyplot as plt
plt.imshow(d2cMaps['lambdaMap'])
plt.show()
==========================================
"""

import numpy as np

def d2cMapping(band,cdpDir,slice_transmission='80pc',fileversion = "8B.05.02"):

    # all MRS distortion files
    distcdp = {}
    distcdp["3C"] = "MIRI_FM_MIRIFULONG_34LONG_DISTORTION_%s.fits" %fileversion
    distcdp["3B"] = "MIRI_FM_MIRIFULONG_34MEDIUM_DISTORTION_%s.fits" %fileversion
    distcdp["3A"] = "MIRI_FM_MIRIFULONG_34SHORT_DISTORTION_%s.fits" %fileversion

    distcdp["1C"] = "MIRI_FM_MIRIFUSHORT_12LONG_DISTORTION_%s.fits" %fileversion
    distcdp["1B"] = "MIRI_FM_MIRIFUSHORT_12MEDIUM_DISTORTION_%s.fits" %fileversion
    distcdp["1A"] = "MIRI_FM_MIRIFUSHORT_12SHORT_DISTORTION_%s.fits" %fileversion

    distcdp["4C"] = distcdp["3C"]
    distcdp["4B"] = distcdp["3B"]
    distcdp["4A"] = distcdp["3A"]

    distcdp["2C"] = distcdp["1C"]
    distcdp["2B"] = distcdp["1B"]
    distcdp["2A"] = distcdp["1A"]


    # import parameters needed for d2c mapping
    if fileversion[:5] in ['7B.05','07.05','8B.05','08.05']:
        from astropy.io import fits
        dist = fits.open(cdpDir+distcdp[band])
        alphaPoly = dist['Alpha_CH{}'.format(band[0])].data
        lambdaPoly = dist['Lambda_CH{}'.format(band[0])].data
        bdel = dist[0].header['B_DEL{}'.format(band[0])]
        bzero = dist[0].header['B_ZERO{}'.format(band[0])]

        slice_idx = int(slice_transmission[0])-1
        sliceMap = dist['Slice_Number'].data[slice_idx,:,:]
        dist.close()

    else:
        from astropy.io import fits
        dist = fits.open(cdpDir+distcdp[band])
        alphaPoly = dist['Alpha_CH{}'.format(band[0])].data
        lambdaPoly = dist['Lambda_CH{}'.format(band[0])].data
        bdel = dist[0].header['B_DEL{}'.format(band[0])]
        bzero = dist[0].header['B_ZERO{}'.format(band[0])]

        slice_idx = int(slice_transmission[0])-1
        sliceMap = dist['Slice_Number'].data
        dist.close()

    # create maps with wavelengths, alpha and beta coordinates and pixel size

    channel = int(band[0])
    #> slice numbers in the slice map of the distortion CDP for this band
    sliceInventory = np.unique(sliceMap)
    slicesInBand = sliceInventory[np.where( (sliceInventory >= 100*channel ) & (sliceInventory <100*(channel+1)))]

    #> initialise the maps with wavelengths, alpha and beta coordinates of corners for every pixel
    lambdaMap  = np.zeros(sliceMap.shape)
    lambdaLLMap = np.zeros(sliceMap.shape)
    lambdaULMap = np.zeros(sliceMap.shape)
    lambdaURMap = np.zeros(sliceMap.shape)
    lambdaLRMap = np.zeros(sliceMap.shape)
    alphaLLMap = np.zeros(sliceMap.shape)
    alphaULMap = np.zeros(sliceMap.shape)
    alphaURMap = np.zeros(sliceMap.shape)
    alphaLRMap = np.zeros(sliceMap.shape)
    betaLLMap  = np.zeros(sliceMap.shape)
    betaULMap  = np.zeros(sliceMap.shape)
    betaURMap  = np.zeros(sliceMap.shape)
    betaLRMap  = np.zeros(sliceMap.shape)
    alphaMap   = np.zeros(sliceMap.shape)
    betaMap    = np.zeros(sliceMap.shape)

    for ss in slicesInBand:
        s = int(ss - 100*channel)
        #> construct a list of y,x coordinates of detector pixels belonging to slices of this band
        pixels = np.where(sliceMap == ss)
        #> for all pixels within the band, construct arrays with center y,x coordinates, and y,z
        # coordinates of the corners of the pixel
        pixelCtry = pixels[0]
        pixelCtrx = pixels[1]
        # old values!
        # pixelLLy = pixelCtry - 0.5
        # pixelLLx = pixelCtrx - 0.5
        # pixelULy = pixelCtry + 0.5
        # pixelULx = pixelCtrx - 0.5
        # pixelURy = pixelCtry + 0.5
        # pixelURx = pixelCtrx + 0.5
        # pixelLRy = pixelCtry - 0.5
        # pixelLRx = pixelCtrx + 0.5
        # new values (flipped old values)!
        pixelLLy = pixelCtry + 0.5
        pixelLLx = pixelCtrx - 0.5
        pixelULy = pixelCtry - 0.5
        pixelULx = pixelCtrx - 0.5
        pixelURy = pixelCtry - 0.5
        pixelURx = pixelCtrx + 0.5
        pixelLRy = pixelCtry + 0.5
        pixelLRx = pixelCtrx + 0.5

        # Calculate wavelengths for center of the pixels, following (Eq 3) in MIRI-TN-00001-ETH
        # lambda(x,y) = SUM_i(SUM_j ( (K_lam(i,j)*(x-xs)**j * y**i)))
        lambdasLL = np.zeros(len(pixelCtry))
        lambdasLR = np.zeros(len(pixelCtry))
        lambdasUL = np.zeros(len(pixelCtry))
        lambdasUR = np.zeros(len(pixelCtry))
        lambdas   = np.zeros(len(pixelCtry))
        lp = lambdaPoly[s-1]
        xs = lp[0]
        for i in range(5):
            for j in range(5):
                cIndex = 1 + i*5 + j
                lambdasLL = lambdasLL + lp[cIndex]*(pixelLLx-xs)**j * pixelLLy**i
                lambdasLR = lambdasLR + lp[cIndex]*(pixelLRx-xs)**j * pixelLRy**i
                lambdasUL = lambdasUL + lp[cIndex]*(pixelULx-xs)**j * pixelULy**i
                lambdasUR = lambdasUR + lp[cIndex]*(pixelURx-xs)**j * pixelURy**i
                lambdas   = lambdas   + lp[cIndex]*(pixelCtrx-xs)**j * pixelCtry**i
        lambdaLLMap[pixels] = lambdasLL
        lambdaLRMap[pixels] = lambdasLR
        lambdaULMap[pixels] = lambdasUL
        lambdaURMap[pixels] = lambdasUR
        lambdaMap[pixels]   = lambdas

        #> Calculate alpha coordinate for the corners of the pixels, following (Eq 2) in
        # MIRI-TN-00001-ETH
        # alpha(x,y) = SUM_i(SUM_j ( (K_alpha(i,j)*(x-xs)**j * y**i)))
        alphasLL = np.zeros(len(pixelCtry))
        alphasLR = np.zeros(len(pixelCtry))
        alphasUL = np.zeros(len(pixelCtry))
        alphasUR = np.zeros(len(pixelCtry))
        alphas   = np.zeros(len(pixelCtry))

        ap = alphaPoly[s-1]
        xs = ap[0]
        for i in range(5):
            for j in range(5):
                cIndex = 1 + i*5 + j
                alphasLL = alphasLL + ap[cIndex]*(pixelLLx-xs)**j * pixelLLy**i
                alphasLR = alphasLR + ap[cIndex]*(pixelLRx-xs)**j * pixelLRy**i
                alphasUL = alphasUL + ap[cIndex]*(pixelULx-xs)**j * pixelULy**i
                alphasUR = alphasUR + ap[cIndex]*(pixelURx-xs)**j * pixelURy**i
                alphas   = alphas   + ap[cIndex]*(pixelCtrx-xs)**j * pixelCtry**i
        alphaLLMap[pixels] = alphasLL
        alphaLRMap[pixels] = alphasLR
        alphaULMap[pixels] = alphasUL
        alphaURMap[pixels] = alphasUR
        alphaMap[pixels]   = alphas

        #> Calculate beta coordinate for the corners of the pixels, following (Eq 4) in
        # MIRI-TN-00001-ETH
        # Beta(s) = Beta_zero + (s-1) * Delta_Beta
        betasLL = bzero + (s-0.5-1)*bdel
        betasLR = bzero + (s-0.5-1)*bdel
        betasUL = bzero + (s+0.5-1)*bdel
        betasUR = bzero + (s+0.5-1)*bdel
        betas   = bzero + (s-1)*bdel

        betaLLMap[pixels] = betasLL
        betaLRMap[pixels] = betasLR
        betaULMap[pixels] = betasUL
        betaURMap[pixels] = betasUR
        betaMap[pixels]   = betas

    d2cMaps = {'sliceMap':sliceMap,'alphaMap':alphaMap,'betaMap':betaMap,'lambdaMap':lambdaMap,
               'alphaLLMap':alphaLLMap,'alphaLRMap':alphaLRMap,'alphaULMap':alphaULMap,'alphaURMap':alphaURMap,
               'betaLLMap':betaLLMap,'betaLRMap':betaLRMap,'betaULMap':betaULMap,'betaURMap':betaURMap,
               'lambdaLLMap':lambdaLLMap,'lambdaLRMap':lambdaLRMap,'lambdaULMap':lambdaULMap,'lambdaURMap':lambdaURMap,
               'bdel':bdel,'bzero':bzero,'nslices':len(slicesInBand),'cdp_filename':distcdp[band]}
    return d2cMaps
