"""Functions file used in JDAT notebook: JWST_Mstar_dataAnalysis_PointSourceDetectorBasedExtraction.ipynb

:History:

Created on Mon Jan 10 10:15:00 2022

@author: Dr. Ioannis Argyriou (Institute of Astronomy, KU Leuven, Belgium, ioannis.argyriou@kuleuven.be)
"""

# import python modules
import numpy as np
from scipy.optimize import curve_fit
import scipy.interpolate as scp_interpolate

# Definition
#--auxilliary data
def mrs_aux(band):
    allbands = ['1A','1B','1C','2A','2B','2C','3A','3B','3C','4A','4B','4C']
    allchannels = ['1','2','3','4']
    allsubchannels = ['A','B','C']

    # slice IDs on detector
    sliceid1=[111,121,110,120,109,119,108,118,107,117,106,116,105,115,104,114,103,113,102,112,101]
    sliceid2=[201,210,202,211,203,212,204,213,205,214,206,215,207,216,208,217,209]
    sliceid3=[316,308,315,307,314,306,313,305,312,304,311,303,310,302,309,301]
    sliceid4=[412,406,411,405,410,404,409,403,408,402,407,401]

    MRS_bands = {'1A':[4.885,5.751],
        '1B':[5.634,6.632],
        '1C':[6.408,7.524],
        '2A':[7.477,8.765],
        '2B':[8.711,10.228],
        '2C':[10.017,11.753],
        '3A':[11.481,13.441],
        '3B':[13.319,15.592],
        '3C':[15.4,18.072],
        '4A':[17.651,20.938],
        '4B':[20.417,24.22],
        '4C':[23.884,28.329]} # microns

    MRS_R = {'1A':[3320.,3710.],
        '1B':[3190.,3750.],
        '1C':[3100.,3610.],
        '2A':[2990.,3110.],
        '2B':[2750.,3170.],
        '2C':[2860.,3300.],
        '3A':[2530.,2880.],
        '3B':[1790.,2640.],
        '3C':[1980.,2790.],
        '4A':[1460.,1930.],
        '4B':[1680.,1770.],
        '4C':[1630.,1330.]} # R = lambda / delta_lambda

    MRS_lambpix = {'1A':0.0008,
        '1B':0.0009,
        '1C':0.001,
        '2A':0.0014,
        '2B':0.0017,
        '2C':0.0020,
        '3A':0.0023,
        '3B':0.0026,
        '3C':0.0030,
        '4A':0.0036,
        '4B':0.0042,
        '4C':0.0048} # average pixel spectral size

    MRS_nslices = {'1':21,'2':17,'3':16,'4':12} # number of slices

    MRS_alphapix = {'1':0.196,'2':0.196,'3':0.245,'4':0.273} # arcseconds

    MRS_slice = {'1':0.176,'2':0.277,'3':0.387,'4':0.645} # arcseconds

    MRS_FOV = {'1':[3.70,3.70],'2':[4.51,4.71],'3':[6.13,6.19],'4':[7.74,7.74]} # arcseconds along and across slices

    MRS_FWHM = {'1':0.423,'2':0.647,'3':0.99,'4':1.518} # MRS PSF

    return allbands,allchannels,allsubchannels,MRS_bands[band],MRS_R[band],MRS_alphapix[band[0]],MRS_slice[band[0]],MRS_FOV[band[0]],MRS_FWHM[band[0]],MRS_lambpix[band]

def gauss1d_wBaseline(x, A, mu, sigma, baseline):
    return  A*np.exp(-(x-mu)**2/(2*sigma)**2) + baseline

def gauss2d(xy, amp, x0, y0, sigma_x, sigma_y, base):
    # assert that values are floats
    amp, x0, y0, sigma_x, sigma_y, base = float(amp),float(x0),float(y0),float(sigma_x),float(sigma_y),float(base)
    x, y = xy
    a = 1/(2*sigma_x**2)
    b = 1/(2*sigma_y**2)
    inner = a * (x - x0)**2
    inner += b * (y - y0)**2
    return amp * np.exp(-inner) + base

def point_source_centroiding(band,sci_img,d2cMaps,spec_grid=None,fit='2D',center=None,offset_slice=0,verbose=True):
    # distortion maps
    sliceMap  = d2cMaps['sliceMap']
    lambdaMap = d2cMaps['lambdaMap']
    alphaMap  = d2cMaps['alphaMap']
    betaMap   = d2cMaps['betaMap']
    nslices   = d2cMaps['nslices']
    MRS_alphapix = {'1':0.196,'2':0.196,'3':0.245,'4':0.273} # arcseconds
    MRS_FWHM = {'1':2.16*MRS_alphapix['1'],'2':3.30*MRS_alphapix['2'],
                '3':4.04*MRS_alphapix['3'],'4':5.56*MRS_alphapix['4']} # MRS PSF
    mrs_fwhm  = MRS_FWHM[band[0]]
    lambcens,lambfwhms = spec_grid[0],spec_grid[1]
    unique_betas = np.sort(np.unique(betaMap[(sliceMap>100*int(band[0])) & (sliceMap<100*(int(band[0])+1))]))
    fov_lims  = [alphaMap[np.nonzero(lambdaMap)].min(),alphaMap[np.nonzero(lambdaMap)].max()]

    if verbose:
        print('STEP 1: Rough centroiding')
    if center is None:
        # premise> center of point source is located in slice with largest signal
        # across-slice center:
        sum_signals = np.zeros(nslices)
        for islice in range(1,1+nslices):
            sum_signals[islice-1] = sci_img[(sliceMap == 100*int(band[0])+islice) & (~np.isnan(sci_img))].sum()
        source_center_slice = np.argmax(sum_signals)+1
        source_center_slice+=offset_slice

        # along-slice center:
        det_dims = (1024,1032)
        img = np.full(det_dims,0.)
        sel = (sliceMap == 100*int(band[0])+source_center_slice)
        img[sel]  = sci_img[sel]

        source_center_alphas = []
        for row in range(det_dims[0]):
            source_center_alphas.append(alphaMap[row,img[row,:].argmax()])
        source_center_alphas = np.array(source_center_alphas)
        source_center_alpha  = np.average(source_center_alphas[~np.isnan(source_center_alphas)])
    else:
        source_center_slice,source_center_alpha = center[0],center[1]
    if verbose:
        # summary:
        print( 'Slice {} has the largest summed flux'.format(source_center_slice))
        print( 'Source position: beta = {}arcsec, alpha = {}arcsec \n'.format(round(unique_betas[source_center_slice-1],2),round(source_center_alpha,2)))

    if fit == '0D':
        return source_center_slice,unique_betas[source_center_slice-1],source_center_alpha

    if verbose:
        print( 'STEP 2: 1D Gaussian fit')

    # Fit Gaussian distribution to along-slice signal profile
    sign_amp,alpha_centers,alpha_fwhms,bkg_signal = [np.full((len(lambcens)),np.nan) for j in range(4)]
    sign_amp_sliceoffsetminus1,alpha_centers_sliceoffsetminus1,alpha_fwhms_sliceoffsetminus1,bkg_signal_sliceoffsetminus1 = [np.full((len(lambcens)),np.nan) for j in range(4)]
    sign_amp_sliceoffsetplus1,alpha_centers_sliceoffsetplus1,alpha_fwhms_sliceoffsetplus1,bkg_signal_sliceoffsetplus1 = [np.full((len(lambcens)),np.nan) for j in range(4)]
    failed_fits = []
    for ibin in range(len(lambcens)):
        coords = np.where((sliceMap == 100*int(band[0])+source_center_slice) & (np.abs(lambdaMap-lambcens[ibin])<=lambfwhms[ibin]/2.) & (~np.isnan(sci_img)))
        coords_sliceoffsetminus1 = np.where((sliceMap == 100*int(band[0])+source_center_slice-1) & (np.abs(lambdaMap-lambcens[ibin])<=lambfwhms[ibin]/2.) & (~np.isnan(sci_img)))
        coords_sliceoffsetplus1 = np.where((sliceMap == 100*int(band[0])+source_center_slice+1) & (np.abs(lambdaMap-lambcens[ibin])<=lambfwhms[ibin]/2.) & (~np.isnan(sci_img)))
        if len(coords[0]) == 0:
            failed_fits.append(ibin); continue
        try:
            popt,pcov = curve_fit(gauss1d_wBaseline, alphaMap[coords], sci_img[coords], p0=[sci_img[coords].max(),source_center_alpha,mrs_fwhm/2.355,0],method='lm')
            popt_sliceoffsetminus1,pcov = curve_fit(gauss1d_wBaseline, alphaMap[coords_sliceoffsetminus1], sci_img[coords_sliceoffsetminus1], p0=[sci_img[coords_sliceoffsetminus1].max(),source_center_alpha,mrs_fwhm/2.355,0],method='lm')
            popt_sliceoffsetplus1,pcov = curve_fit(gauss1d_wBaseline, alphaMap[coords_sliceoffsetplus1], sci_img[coords_sliceoffsetplus1], p0=[sci_img[coords_sliceoffsetplus1].max(),source_center_alpha,mrs_fwhm/2.355,0],method='lm')
        except:
            failed_fits.append(ibin); continue
        sign_amp[ibin]      = popt[0]+popt[3]
        alpha_centers[ibin] = popt[1]
        alpha_fwhms[ibin]   = 2.355*np.abs(popt[2])
        bkg_signal[ibin]    = popt[3]

        sign_amp_sliceoffsetminus1[ibin]      = popt_sliceoffsetminus1[0]+popt_sliceoffsetminus1[3]
        alpha_centers_sliceoffsetminus1[ibin] = popt_sliceoffsetminus1[1]
        alpha_fwhms_sliceoffsetminus1[ibin]   = 2.355*np.abs(popt_sliceoffsetminus1[2])
        bkg_signal_sliceoffsetminus1[ibin]    = popt_sliceoffsetminus1[3]

        sign_amp_sliceoffsetplus1[ibin]      = popt_sliceoffsetplus1[0]+popt_sliceoffsetplus1[3]
        alpha_centers_sliceoffsetplus1[ibin] = popt_sliceoffsetplus1[1]
        alpha_fwhms_sliceoffsetplus1[ibin]   = 2.355*np.abs(popt_sliceoffsetplus1[2])
        bkg_signal_sliceoffsetplus1[ibin]    = popt_sliceoffsetplus1[3]

    # omit outliers
    for i in range(len(np.diff(sign_amp))):
        if np.abs(np.diff(alpha_centers)[i]) > 0.05:
            sign_amp[i],sign_amp[i+1],alpha_centers[i],alpha_centers[i+1],alpha_fwhms[i],alpha_fwhms[i+1] = [np.nan for j in range(6)]

    if verbose:
        print( '[Along-slice fit] The following bins failed to converge:')
        print( failed_fits)

    # Fit Gaussian distribution to across-slice signal profile (signal brute-summed in each slice)
    summed_signal,beta_centers,beta_fwhms = [np.full((len(lambcens)),np.nan) for j in range(3)]
    failed_fits = []
    for ibin in range(len(lambcens)):
        if np.isnan(alpha_centers[ibin]):
            failed_fits.append(ibin)
            continue
        sel = (np.abs(lambdaMap-lambcens[ibin])<=lambfwhms[ibin]/2.) & (~np.isnan(sci_img))
        try:
            signals = np.array([sci_img[(sliceMap == 100*int(band[0])+islice) & sel][np.abs(alphaMap[(sliceMap == 100*int(band[0])+islice) & sel]-alpha_centers[ibin]).argmin()] for islice in range(1,1+nslices)])
            signals[source_center_slice-2:source_center_slice+1] = np.array([sign_amp_sliceoffsetminus1[ibin],sign_amp[ibin],sign_amp_sliceoffsetplus1[ibin]])
        except ValueError:
            failed_fits.append(ibin)
            continue
        try:
            popt,pcov = curve_fit(gauss1d_wBaseline, unique_betas, signals, p0=[signals.max(),unique_betas[source_center_slice-1],mrs_fwhm/2.355,0],method='lm')
        except:
            failed_fits.append(ibin)
            continue
        summed_signal[ibin] = popt[0]+popt[3]
        beta_centers[ibin]  = popt[1]
        beta_fwhms[ibin]    = 2.355*np.abs(popt[2])

    # # omit outliers
    # for i in range(len(np.diff(summed_signal))):
    #     if np.abs(np.diff(beta_centers)[i]) > 0.05:
    #         summed_signal[i],summed_signal[i+1],beta_centers[i],beta_centers[i+1],beta_fwhms[i],beta_fwhms[i+1] = [np.nan for j in range(6)]
    if verbose:
        print( '[Across-slice fit] The following bins failed to converge:')
        print( failed_fits)
        print( '')

    if fit == '1D':
        sigma_alpha, sigma_beta = alpha_fwhms/2.355, beta_fwhms/2.355
        return sign_amp,alpha_centers,beta_centers,sigma_alpha,sigma_beta,bkg_signal

    elif fit == '2D':
        if verbose:
            print( 'STEP 3: 2D Gaussian fit')
        sign_amp2D,alpha_centers2D,beta_centers2D,sigma_alpha2D,sigma_beta2D,bkg_amp2D = [np.full((len(lambcens)),np.nan) for j in range(6)]
        failed_fits = []

        for ibin in range(len(lambcens)):
            # initial guess for fitting, informed by previous centroiding steps
            amp,alpha0,beta0  = sign_amp[ibin],alpha_centers[ibin],beta_centers[ibin]
            sigma_alpha, sigma_beta = alpha_fwhms[ibin]/2.355, beta_fwhms[ibin]/2.355
            base = 0
            guess = [amp, alpha0, beta0, sigma_alpha, sigma_beta, base]
            bounds = ([0,-np.inf,-np.inf,0,0,-np.inf],[np.inf,np.inf,np.inf,np.inf,np.inf,np.inf])

            # data to fit
            coords = (np.abs(lambdaMap-lambcens[ibin])<lambfwhms[ibin]/2.)
            alphas, betas, zobs   = alphaMap[coords],betaMap[coords],sci_img[coords]
            alphabetas = np.array([alphas,betas])

            # perform fitting
            try:
                popt,pcov = curve_fit(gauss2d, alphabetas, zobs, p0=guess,bounds=bounds)
            except:
                failed_fits.append(ibin); continue

            sign_amp2D[ibin]      = popt[0]
            alpha_centers2D[ibin] = popt[1]
            beta_centers2D[ibin]  = popt[2]
            sigma_alpha2D[ibin]   = popt[3]
            sigma_beta2D[ibin]    = popt[4]
            bkg_amp2D[ibin]       = popt[5]
        if verbose:
            print( 'The following bins failed to converge:')
            print( failed_fits)

        return sign_amp2D,alpha_centers2D,beta_centers2D,sigma_alpha2D,sigma_beta2D,bkg_amp2D

def evaluate_psf_cdp(psffits,d2cMaps,source_center=[0,0],norm=True,cdp_slice=None):
    # PSF CDP is provided as a spectral cube
    #>get values
    psf_values = psffits[1].data.transpose(2,1,0).copy() # flip data from Z,Y,X to X,Y,Z
    if norm:
        #>normalize values
        print('Normalizing PSF (divide by sum of all spaxel values)')
        for layer in range(psf_values.shape[2]):
            psf_values[:,:,layer] /= psf_values[:,:,layer].sum()
    if cdp_slice is not None:
        # use only a single layer of the PSF CDP cube
        print('Using single slice of PSF cube')
        for layer in range(psf_values.shape[2]):
            psf_values[:,:,layer] = psf_values[:,:,cdp_slice]

    #>get grid
    NAXIS1,NAXIS2,NAXIS3 = psf_values.shape

    alphastpix = psffits[1].header['CRPIX1'] # pixel nr
    alpha_step = psffits[1].header['CDELT1'] # arcsec/pix
    stalpha    = psffits[1].header['CRVAL1']-(alphastpix-1)*alpha_step # arcsec

    betastpix = psffits[1].header['CRPIX2'] # pixel nr
    beta_step = psffits[1].header['CDELT2'] # arcsec/pix
    stbeta    = psffits[1].header['CRVAL2']-(betastpix-1)*beta_step # arcsec

    stwavl = psffits[1].header['CRVAL3'] # microns
    wavl_step   = psffits[1].header['CDELT3'] # microns/pix

    alpha_slices = np.linspace(stalpha,stalpha+ (NAXIS1-1.5)*alpha_step,NAXIS1)
    beta_slices  = np.linspace(stbeta,stbeta+ (NAXIS2-1.5)*beta_step,NAXIS2)
    wvl_slices   = np.linspace(stwavl ,stwavl+NAXIS3*wavl_step,NAXIS3)

    #> center psf to source
    alpha_slices += source_center[0]
    beta_slices  += source_center[1]

    #> create interpolant based on regular grid
    interpolpsf = scp_interpolate.RegularGridInterpolator((alpha_slices,beta_slices,wvl_slices),psf_values)
    interpolpsf.fill_value=0.
    interpolpsf.bounds_error=False

    # evaluate psf at each pixel center and pixel corner
    alphaULMap = d2cMaps['alphaULMap']
    alphaURMap = d2cMaps['alphaURMap']
    alphaLLMap = d2cMaps['alphaLLMap']
    alphaLRMap = d2cMaps['alphaLRMap']
    alphaMap   = d2cMaps['alphaMap']

    betaULMap = d2cMaps['betaULMap']
    betaURMap = d2cMaps['betaURMap']
    betaLLMap = d2cMaps['betaLLMap']
    betaLRMap = d2cMaps['betaLRMap']
    betaMap   = d2cMaps['betaMap']

    lambdaULMap = d2cMaps['lambdaULMap']
    lambdaURMap = d2cMaps['lambdaURMap']
    lambdaLLMap = d2cMaps['lambdaLLMap']
    lambdaLRMap = d2cMaps['lambdaLRMap']
    lambdaMap = d2cMaps['lambdaMap']

    #> interpolate psf to science image pixel centers and corners
    #-- assume no significant change in wavelength over one pixel size
    psfUL  = interpolpsf((alphaULMap,betaULMap,lambdaULMap))
    psfUR  = interpolpsf((alphaURMap,betaURMap,lambdaURMap))
    psfLL  = interpolpsf((alphaLLMap,betaLLMap,lambdaLLMap))
    psfLR  = interpolpsf((alphaLRMap,betaLRMap,lambdaLRMap))
    psfCEN = interpolpsf((alphaMap,betaMap,lambdaMap))

    #> evaluate psf as a weighted average
    w = np.array([0.125,0.125,0.125,0.125,0.5]) # WARNING: ARBITRARY!
    sumweights = w.sum()

    psf = (w[0]*psfUL+w[1]*psfUR+w[2]*psfLL+w[3]*psfLR+w[4]*psfCEN)/sumweights

    print('DONE')
    return psf
