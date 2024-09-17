import os
import sys
import astropy.io.fits as pyfits


def log_comment(LOGFILE, comment, verbose=False, show_date=False, mode='a'):

    """
    Log a message to a file, optionally including a date tag
    """
    import time

    if show_date:
        msg = '# ({0})\n'.format(time.ctime())
    else:
        msg = ''

    msg += '{0}\n'.format(comment)

    if LOGFILE is not None:
        fp = open(LOGFILE, mode)
        fp.write(msg)
        fp.close()

    if verbose:
        print(msg[:-1])

    return msg


def update_pure_parallel_wcs(file, logfile="pure_parallel_wcs_logfile",
                             fix_vtype='PARALLEL_PURE', verbose=True):

    """
    Update pointing-related keywords of pure parallel exposures using the
    pointing info from the FGS (and the prime exposures) from the MAST database
    and `pysiaf`
    
    1. Find the FGS log from a MAST query that starts before the pure parallel
       exposure starts and ends after the exposure ends.
    2. Use the ``ra_v1, dec_v1, pa_v3`` values from the FGS log to set the
       pointing attitude with `pysiaf`.
    3. Compute the sky position of the ``CRPIX`` reference pixel of ``file``
       with `pysiaf` and put that position in the ``CRVAL`` keywords.
    
    Parameters
    ----------
    file : str
        Filename of a pure-parallel exposure (typically a rate.fits file)
    
    fix_vtype : str
        Only run if ``file[0].header['VISITYPE'] == fix_vtype``
    
    verbose : bool
        Status messaging
    
    Returns
    -------
    status : None, True
        Returns None if some problem is found 
    
    """
    import pysiaf    
    import mastquery.jwst as jwstquery
    
    if not os.path.exists(file):
        msg = "PureParallelUtils.update_pure_parallel_wcs: "
        msg += f" {file} not found"
        log_comment(logfile, msg, verbose=verbose)
        return None
    
    with pyfits.open(file) as im:
        h0 = im[0].header.copy()
        h1 = im[1].header.copy()
        if 'VISITYPE' not in im[0].header:
            msg = "PureParallelUtils.update_pure_parallel_wcs: "
            msg += f" VISITYPE not found in header {file}"
            log_comment(logfile, msg, verbose=verbose)
            return None
    
    # Only continue if this is a Pure Parallel exposure
    vtype = h0['VISITYPE']
    
    if vtype != fix_vtype:
        msg = "PureParallelUtils.update_pure_parallel_wcs: "
        msg += f" VISITYPE ({vtype}) != {fix_vtype}, skip"
        log_comment(logfile, msg, verbose=verbose)
        return None
    
    crval_init = h1['CRVAL1'], h1['CRVAL2']
    
    # Get correct pointings from FGS logs. Allow the associated FGS exposure
    # to start up to 0.02 day ~ 30 min before the science exposure.
    dt = 0.02
    gs = jwstquery.query_guidestar_log(
             mjd=(h0['EXPSTART']-dt, h0['EXPEND']+dt),
             program=None,
             exp_type=['FGS_FINEGUIDE'],
         )
    
    keep = (gs['expstart'] < h0['EXPSTART'])
    keep &= (gs['expend'] > h0['EXPEND'])
    
    if keep.sum() == 0:
        msg = f"PureParallelUtils.update_pure_parallel_wcs: par_file='{file}'"
        msg += " couldn't find corresponding exposure in FGS logs"
        log_comment(logfile, msg, verbose=verbose)
        return None
    
    gs = gs[keep][0]
    pos = (gs['ra_v1'], gs['dec_v1'], gs['pa_v3'])
    attmat = pysiaf.utils.rotations.attitude(0.0, 0.0, *pos)
        
    # And apply the pointing to the parallel aperture and reference pixel
    par_aper = pysiaf.Siaf(h0['INSTRUME'])[h0['APERNAME']]
    par_aper.set_attitude_matrix(attmat)

    crpix = h1['CRPIX1'], h1['CRPIX2']
    crpix_init = par_aper.sky_to_sci(*crval_init)
    
    crval_fix = par_aper.sci_to_sky(*crpix)
    
    msg = (
        f"PureParallelUtils.update_pure_parallel_wcs: File: {file}\n"
        f"PureParallelUtils.update_pure_parallel_wcs: FGS: {gs['fileName']}\n"
        f"PureParallelUtils.update_pure_parallel_wcs: original crval: "
        f"{crval_init[0]:.7f} {crval_init[1]:.7f}\n"
        f"PureParallelUtils.update_pure_parallel_wcs:      new crval: "
        f"{crval_fix[0]:.7f} {crval_fix[1]:.7f}\n"
        f"PureParallelUtils.update_pure_parallel_wcs:         d(pix): "
        f"{crpix[0] - crpix_init[0]:6.3f} {crpix[1] - crpix_init[1]:6.3f}"
    )
    
    _ = log_comment(logfile, msg, verbose=verbose)
    
    with pyfits.open(file, mode='update') as im:
        im[1].header['RA_V1'] = gs['ra_v1']
        im[1].header['DEC_V1'] = gs['dec_v1']
        im[1].header['PA_V3'] = gs['pa_v3']
        im[1].header['CRVAL1'] = crval_fix[0]
        im[1].header['CRVAL2'] = crval_fix[1]
        im[1].header['PUREPWCS'] = True, 'WCS updated from query of FGS log file'
        im[1].header['PUREPEXP'] = gs['fileName'], 'FGS log file'
        
        im.flush()
    
    return True


if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        print('Syntax: update_parallel_wcs.py fitsfile <verbose>')
        print('        where fitsfile is typically a _rate.fits or _rateints.fits file')
        print('        and <verbose> is a boolean to decide whether or not')
        print('        to print the results (the default is `True`)')
        sys.exit()
    fitsfile = str(sys.argv[1])
    verbose = True
    if len(sys.argv) > 2:
        if str(sys.argv[2]).upper() != 'TRUE':
            verbose = False
    update_pure_parallel_wcs(fitsfile, verbose=verbose)
