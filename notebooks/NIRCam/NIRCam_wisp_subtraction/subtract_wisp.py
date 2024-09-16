#! /usr/bin/env python

"""
Scales and subtracts wisp templates from full-frame NIRCam images.

Authors
-------
    Ben Sunnquist, 2024

Use
---
    To run from the command line using all default arguments (assumes input files
    and wisp templates are in the current working directory):
    >>> python subtract_wisp.py

    To run on all NRCB4 files with no wisp scaling or segmap creation, and flagging 
    wisp values above 0.01 in the input images' data quality arrays:
    >>> python subtract_wisp.py --files ./*nrcb4_cal.fits --no-scale_wisp --no-create_segmap --flag_wisp_thresh 0.01

    To run the same example above within python e.g. a Jupyter notebook:
    >>> from subtract_wisp import process_files
    >>> process_files(files='./*nrcb4_cal.fits', create_segmap=False, scale_wisp=False, flag_wisp_thresh=0.01)

Notes
-----
    Wisp templates designed to work with this code are available at the following STScI Box link:
    https://stsci.app.box.com/s/1bymvf1lkrqbdn9rnkluzqk30e8o2bne

    This code was developed using the JWST Pipeline v1.14.0 environment:
    https://github.com/spacetelescope/jwst
        > conda create -n <env_name> python=3.11
        > conda activate <env_name>
        > pip install jwst==1.14.0
    Other environments may work fine, but be sure to use Python 3.9+.
"""

import argparse
from functools import partial
import multiprocessing
import os
import warnings

from astropy.convolution import convolve, Gaussian2DKernel
from astropy.io import fits
from astropy.stats import median_absolute_deviation, sigma_clipped_stats
from astropy.wcs import WCS
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from photutils.segmentation import detect_sources, detect_threshold
from scipy.ndimage import binary_dilation, generate_binary_structure
matplotlib.use('Agg')

warnings.filterwarnings('ignore', message="Input data contains invalid values*")  # nan values expected throughout code
warnings.filterwarnings('ignore', message="All-NaN slice encountered*")
warnings.filterwarnings('ignore', message="'obsfix' made the change*")  # from astropy wcs during lw segmap blotting
warnings.filterwarnings('ignore', message="'datfix' made the change*")  # from astropy wcs during lw segmap blotting


# -----------------------------------------------------------------------------


def make_segmap(f, seg_from_lw=True, sigma=0.8, npixels=10, dilate_segmap=5, save_segmap=False):
    """
    Make a segmentation map for the input file.
    
    Parameters
    ----------
    f : str
        The filename to make a segmentation map for, e.g.
        jw01063006004_02101_00005_nrca3_cal.fits. Source-finding is only performed
        on cal files, so the cal file must be present if a rate file is input here.

    seg_from_lw : bool
        Option to perform the source-finding on the corresponding
        longwave image. This is generally preferred since the longwave is not
        affected by wisps.

    sigma: float
        The source detection sigma threshold.

    npixels: int
        The number of connected pixels above sigma to include as a source.

    dilate_segmap: int
        The number of pixels to grow the segmap outwards by.
    
    save_segmap : bool
        Option to save the generated segmentation map.

    Returns
    -------
    segmap : numpy.ndarray
        The generated segmentation map.

    Outputs
    -------
    {f}_seg.fits : fits image
        The generated segmentation map.
    """

    print('Making segmap for {}'.format(f))
    outfile = f.replace('.fits', '_seg.fits')

    # Get the input data; always source-find on the cal image
    detector = os.path.basename(f).split('_')[-2].lower()
    f_sw = f.replace('_rate.fits', '_cal.fits')
    if (seg_from_lw) & ('long' not in detector):
        if 'a' in detector:
            f_lw = f.replace(detector.lower(), 'nrcalong').replace('_rate.fits', '_cal.fits')
        if 'b' in detector:
            f_lw = f.replace(detector.lower(), 'nrcblong').replace('_rate.fits', '_cal.fits')
        data = fits.getdata(f_lw, 'SCI')
        dq = fits.getdata(f_lw, 'DQ')
    else:
        data = fits.getdata(f_sw, 'SCI')
        dq = fits.getdata(f_sw, 'DQ')

    # Make the segmentation map
    threshold = detect_threshold(data, sigma)
    g = Gaussian2DKernel(x_stddev=3)
    data_conv = convolve(data, g, mask=dq & 1 != 0)  # Smooth input image before detecting sources
    seg = detect_sources(data_conv, threshold, npixels=npixels, mask=dq & 1 != 0)  # avoid bad pixels as sources
    segmap_data = seg.data
    segmap_data[segmap_data != 0] = 1

    # Dilate the segmap outwards
    if dilate_segmap != 0:
        segmap_data = binary_dilation(segmap_data, iterations=dilate_segmap, structure=generate_binary_structure(2, 2))
        segmap_data[segmap_data != 0] = 1
    
    # Blot LW segmap back onto SW detector space
    if (seg_from_lw) & ('long' not in detector):
        segmap_tmp = np.zeros(segmap_data.shape).astype(int)
        wcs = WCS(fits.getheader(f_lw, 'SCI'))  # lw cal wcs
        seg_y, seg_x = np.where(segmap_data != 0)
        sky_coords = wcs.pixel_to_world(seg_x, seg_y)
        wcs = WCS(fits.getheader(f_sw, 'SCI'))  # sw cal wcs
        coords = wcs.world_to_pixel(sky_coords)
        for i in np.arange(len(coords[0])):
            y, x = int(coords[1][i]), int(coords[0][i])
            if (y < 2048) & (x < 2048) & (y >= 0) & (x >= 0):
                segmap_tmp[y, x] = 1
        # Dilate to compensate for y,x rounding due to different lw/sw pixel scales
        segmap_data = binary_dilation(segmap_tmp, iterations=1, structure=generate_binary_structure(2, 2)).astype(int)

    # Save the segmap
    segmap_data = segmap_data.astype(int)
    if save_segmap:
        fits.writeto(outfile, segmap_data, overwrite=True)

    return segmap_data


# -----------------------------------------------------------------------------


def process_file(f, wisp_dir='./', create_segmap=True, seg_from_lw=True, sigma=0.8, npixels=10, dilate_segmap=5,
                 save_segmap=False, sub_wisp=True, gauss_smooth_wisp=False, gauss_stddev=3.0, scale_wisp=True,
                 scale_method='mad', poly_degree=5, factor_min=0.0, factor_max=2.0, factor_step=0.01, min_wisp=None, 
                 flag_wisp_thresh=None, dq_val=1, correct_rows=True, correct_cols=False, save_data=True, save_model=True, 
                 plot=True, show_plot=False, suffix='_wisp'):
    """
    The main processing function. Combines the segmap creation and wisp scaling/subtraction steps together.

    See make_segmap() and subtract_wisp() docstrings for more details on all of the input arguments.

    Parameters
    ----------
    f : str
        The input filename to subtract the wisp from. Must be a full-frame NIRCam image, e.g.
        jw01063006004_02101_00005_nrca3_cal.fits.

    wisp_dir : str
        The directory containing the wisp templates. The templates are assumed to have the 
        form WISP_{DETECTOR}_{FILTER}_{PUPIL}.fits.
    """

    # Get the relevant wisp template
    print('Processing {}'.format(f))
    header = fits.getheader(f)
    det, fltr, pupil = header['DETECTOR'], header['FILTER'], header['PUPIL']
    file_type = f.split('_')[-1].replace('.fits', '').upper()  # CAL or RATE
    wisp_data = fits.getdata(os.path.join(wisp_dir, 'WISP_{}_{}_{}.fits'.format(det, fltr, pupil)), file_type)

    # Make the segmentation map
    if create_segmap:
        segmap_data = make_segmap(f, seg_from_lw=seg_from_lw, sigma=sigma, npixels=npixels, 
                                  dilate_segmap=dilate_segmap, save_segmap=save_segmap)
    else:
        segmap_data = np.zeros(wisp_data.shape).astype(int)

    # Scale and subtract wisp template
    _ = subtract_wisp(f, wisp_data=wisp_data, segmap_data=segmap_data, sub_wisp=sub_wisp, 
                      gauss_smooth_wisp=gauss_smooth_wisp, gauss_stddev=gauss_stddev, 
                      scale_wisp=scale_wisp, scale_method=scale_method, poly_degree=poly_degree, 
                      factor_min=factor_min, factor_max=factor_max, factor_step=factor_step, 
                      min_wisp=min_wisp, flag_wisp_thresh=flag_wisp_thresh, dq_val=dq_val, 
                      correct_rows=correct_rows, correct_cols=correct_cols, save_data=save_data, 
                      save_model=save_model, plot=plot, show_plot=show_plot, suffix=suffix)
    print('Processing complete for {}'.format(f))

# -----------------------------------------------------------------------------


def process_files(files, nproc=6, **kwargs):
    """"Wrapper around the process_file() function to allow for multiprocessing."""

    # Remove any files that are not in a detector impacted by wisps
    files = [f for f in files if any(substring in f for substring in ['nrca3', 'nrca4', 'nrcb3', 'nrcb4'])]
    print('Found {} relevant input files.'.format(len(files)))
    
    # Proess the files
    process_file_partial = partial(process_file, **kwargs)
    p = multiprocessing.Pool(nproc)
    _ = p.map(process_file_partial, files)
    p.close()
    p.join()


# -----------------------------------------------------------------------------


def subtract_wisp(f, wisp_data, segmap_data=None, sub_wisp=True, gauss_smooth_wisp=False, gauss_stddev=3.0, scale_wisp=True,
                  scale_method='mad', poly_degree=5, factor_min=0.0, factor_max=2.0, factor_step=0.01, min_wisp=None, 
                  flag_wisp_thresh=None, dq_val=1, correct_rows=True, correct_cols=False, save_data=True, save_model=True, plot=True, 
                  show_plot=False, suffix='_wisp'):
    """Scales and subtracts a wisp template from the input file.

    Parameters
    ----------
    f : str
        The file to subtract the wisp from. Must be a full-frame NIRCam image, e.g.
        jw01063006004_02101_00005_nrca3_cal.fits.

    wisp_data : numpy.ndarray
        The wisp template data. Must be the same shape as input file data.

    segmap_data : numpy.ndarray
        A mask of the sources in the input file. Must be the same shape as input file data.

    sub_wisp : bool
        Option to subtract the wisp template from the input file. Generally this is always True
        except for cases where you only want to flag high wisp values in the input file's data
        quality array, i.e. using flag_wisp_thresh.

    gauss_smooth_wisp: bool
        Option to smooth the wisp template with a Gaussian filter before scaling/subtracting it.

    gauss_stddev: float
        The standard deviation of the Gaussian filter to apply to the wisp if gauss_smooth_wisp is True.

    scale_wisp : bool
        Option to scale the wisp templates before subtracting it from the input file.

    scale_method : str
        The method used to scale the wisp template. Options are 'mad' and 'median'. The former
        chooses the scale factor by minimizing the median absolute deviation of the wisp-corrected
        image. The latter chooses the scale factor by minimizing the overall signal level
        difference between the wisp-affected region and the remaining detector region.

    poly_degree : int
        The degree of the fitting polynomial applied to the residuals of the chosen scale_method.
        The minimum of this polynomial fit decides the wisp scale factor. Set to 0 to ignore, 
        which is generally recommended when scale_method is 'median'.

    factor_min: float
        The lowest factor to scale the wisp template by.

    factor_max: float
        The highest factor to scale the wisp template by.

    factor_step: float
        The step distance between factor_min and factor_max to try scaling the wisp template by.
        Scale factors from factor_min to factor_max in iterations equal to the step distance 
        specified here will all be tested.

    min_wisp : float
        The minimum wisp value to perform wisp subtraction. Everything below this value will be set
        to zero in the wisp template before subtracting from the input file. The units of this
        value should match the units in the input file. Set to None to ignore.

    flag_wisp_thresh : float
        Flag values in the wisp template above this threshold in the input file's data quality 
        array. The units of this value should match the units in the input file. Set to None to ignore.
        The DQ value used here is set by the dq_val parameter.

    dq_val : int
        The data quality value applied to the input file's DQ array to pixels above flag_wisp_thresh.
        The default of 1, i.e. DO_NOT_USE in the JWST Pipeline, results in these pixels being ignored
        in the JWST Pipeline image3 drizzling step by default. 1073741824, i.e. OTHER_BAD_PIXEL, is another
        option to use if you want these pixels flagged in the input file's DQ array, but still used in the  
        default drizzling step. Only relevant if flag_wisp_thresh is True.
    
    correct_rows : bool
        Option to correct horizontal noise in the input file (e.g. 1/f noise residuals). This won't be 
        subtracted from the input file; it is only used to help the wisp scaling step.

    correct_cols : bool
        Option to correct vertical noise in the input file (e.g. residual odd-even column effects 
        and amp offsets). This noise is generally much lower than the horizontal noise in correct_rows.
        This won't be subtracted from the input file; it is only used to help the wisp scaling step.

    save_data : bool
        Option to save the wisp-subtracted data. The filename will be {f}{suffix}.fits.

    save_model : bool
        Option to save the wisp model subtracted fom the input file. The filename will 
        be {f}{suffix}_model.fits.

    plot : bool
        Option to save a diagnostic plot showing the original data, wisp-subtracted data, final wisp model, 
        and a plot of the various wisp scale factors tested with their corresponding residual noise.
        The filename will be {f}{suffix}_plots.png.

    show_plot : bool
        Option to show the diagnostic plot in e.g. jupyter notebook (note you'll have to set 
        %matplotlib inline in the notebook as well for this to work).

    suffix : str
        The suffix added to all of the output products. If left blank, the original input file will be 
        overwritten if save_data is True.

    Returns
    -------
    new_data : numpy.ndarray
        The wisp-subtracted data.

    wisp_model : numpy.ndarray
        The wisp model subtracted from the input file.

    factors : numpy.ndarray
        The wisp scale factors tested.

    residuals : numpy.ndarray
        The residuals that resulted when applying each of the wisp scale factors tested. The exact 
        meaning of the residuals depends on the chosen scale_method.

    factor : float
        The chosen scale factor applied to the wisp template to create wisp_model.

    Outputs
    -------
    {f}{suffix}.fits : fits image
        The wisp-subtracted input file. Only generated if save_data is True.

    {f}{suffix}_model.fits : fits image
        The wisp model that was subtracted from the input file. Only generated if save_model is True.

    {f}{suffix}_plots.png : png image
        A diagnostic plot showing the original data, wisp-subtracted data, final wisp model, and 
        a plot of the various wisp scale factors tested with their corresponding residuals.
        Only generated if plot is True.
    """

    # Get the input data
    print('Applying wisp template to {}'.format(f))
    h = fits.open(f)
    data = h['SCI'].data
    dq = h['DQ'].data
    if segmap_data is None:
        print('Warning: No segmap data given for {}. Assuming no sources.'.format(f))
        segmap_data = np.zeros(data.shape)

    # Smooth wisp template
    if gauss_smooth_wisp:
        g = Gaussian2DKernel(x_stddev=gauss_stddev)
        wisp_data = convolve(wisp_data, g)

    # Scale the wisp template
    if scale_wisp:
        # Make a mask of the brightest wisp region
        mean, med, stddev = sigma_clipped_stats(wisp_data)
        wisp_mask = (wisp_data > med + 2 * stddev).astype(int)

        # Make versions of the original data and wisp model where only good 
        # pixels in the wisp region are unmasked.
        data_masked = np.copy(data)
        wisp_data_masked = np.copy(wisp_data)
        data_masked[(dq & 1 != 0) | (segmap_data != 0) | (wisp_mask == 0)] = np.nan
        wisp_data_masked[(dq & 1 != 0) | (segmap_data != 0) | (wisp_mask == 0)] = np.nan

        # Make a version of the original data where only good pixels outside 
        # the wisp region are unmasked.
        data_masked_ff = np.copy(data)
        data_masked_ff[(dq & 1 != 0) | (segmap_data != 0) | (wisp_mask != 0)] = np.nan

        # Correct median-collapsed row/column offsets, representing the 1/f residuals 
        # and odd-even column residuals and amp offsets, respectively.
        med = np.nanmedian(data_masked_ff)
        if correct_rows:
            collapsed_rows = np.nanmedian(data_masked_ff - med, axis=1)
        else:
            collapsed_rows = np.zeros(2048)
        if correct_cols:
            collapsed_cols = np.nanmedian(data_masked_ff - med, axis=0)
        else:
            collapsed_cols = np.zeros(2048)
        correction_image = np.tile(collapsed_cols, (2048, 1)) + np.swapaxes(np.tile(collapsed_rows, (2048, 1)), 0, 1)
        data_masked = data_masked - correction_image        
        data_masked_ff = data_masked_ff - correction_image
        med = np.nanmedian(data_masked_ff)
        
        # Scale wisp template and record residuals
        factors = np.arange(factor_min, factor_max, factor_step)
        residuals = []
        for factor in factors:
            wisp_model = wisp_data_masked * factor
            new_data = data_masked - wisp_model
            if scale_method == 'mad':
                residual = median_absolute_deviation(new_data, ignore_nan=True)
            if scale_method == 'median':
                residual = abs(med - np.nanmedian(new_data))
            residuals.append(residual)
        residuals = np.array(residuals)

        # Choose the wisp template with the lowest noise
        if poly_degree != 0:
            fn = np.poly1d(np.polyfit(factors, residuals, poly_degree))  # smooth results
            factor = factors[np.argmin(fn(factors))]
        else:
            factor = factors[np.argmin(residuals)]
        wisp_model = wisp_data * factor
    else:
        # Don't scale the wisp data
        factors, residuals = np.ones(1), np.zeros(1)  # dummy data
        factor = 1.0
        wisp_model = wisp_data * factor

    # Only subtract wisp values above the specified threshold
    if min_wisp is not None:
        wisp_model[wisp_model < min_wisp] = 0

    # Flag wisp values above the specified thereshold in DQ array
    if flag_wisp_thresh is not None:
        new_dq = np.copy(dq)
        new_dq[(dq & dq_val == 0) & (wisp_model > flag_wisp_thresh)] += dq_val
    else:
        new_dq = dq

    # Subtract the final wisp template
    if sub_wisp:
        new_data = data - wisp_model
    else:
        new_data = data

    # Save the wisp-subtracted data and model
    if save_data:
        h['SCI'].data = new_data.astype('float32')
        h['DQ'].data = new_dq
        h.writeto(f.replace('.fits', '{}.fits'.format(suffix)), overwrite=True)
    if save_model:
        fits.writeto(f.replace('.fits', '{}_model.fits'.format(suffix)), wisp_model, overwrite=True)
    h.close()

    # Make diagnostic plots
    if plot:
        fig, axes = plt.subplots(1, 4, figsize=(60, 10))
        for ax in axes:
            ax.tick_params(axis='both', which='major', labelsize=20)
        # Plot original image
        mean, med, stddev = sigma_clipped_stats(data)
        vmin, vmax = med-3*stddev, med+3*stddev
        im = axes[0].imshow(data, origin='lower', vmin=vmin, vmax=vmax, cmap='gray')
        cbar = fig.colorbar(im, ax=axes[0])
        cbar.ax.tick_params(labelsize=20)
        axes[0].set_title('Original', fontsize=35)
        # Plot wisp-corrected image
        im = axes[1].imshow(new_data, origin='lower', vmin=vmin, vmax=vmax, cmap='gray')
        cbar = fig.colorbar(im, ax=axes[1])
        cbar.ax.tick_params(labelsize=20)
        axes[1].set_title('Wisp Corrected', fontsize=35)
        # Plot wisp model
        mean, med, stddev = sigma_clipped_stats(wisp_model)
        im = axes[2].imshow(wisp_model, origin='lower', vmin=0, vmax=med+5*stddev, cmap='gray')
        cbar = fig.colorbar(im, ax=axes[2])
        cbar.ax.tick_params(labelsize=20)
        axes[2].set_title('Wisp Model', fontsize=35)
        # Plot scatterplot of wisp scale factors tested vs residuals
        if (scale_wisp) & (poly_degree != 0):
            axes[3].plot(factors, fn(factors), color='black')
        axes[3].scatter(factors, residuals)
        axes[3].axvline(factor, color='black')
        y_label = 'Residual Median Absolute Deviation' if scale_method == 'mad' else 'Residual Median Difference'
        axes[3].set_ylabel(y_label, fontsize=25)
        axes[3].set_xlabel('Wisp Factor', fontsize=25)
        axes[3].set_title('Chosen Wisp Factor: {:.3f}'.format(factor), fontsize=35)
        axes[3].grid(ls='--', alpha=0.5)
        fig.savefig(f.replace('.fits', '{}_plots.png'.format(suffix)), dpi=100, bbox_inches='tight')
        if not show_plot:
            plt.close()

    return new_data, wisp_model, factors, residuals, factor


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


def parse_args():
    """
    Parses command line arguments.

    See make_segmap() and subtract_wisp() docstrings for more details on all of the input arguments.
    
    Returns
    -------
    args : object
        Contains the input arguments.
    """

    # Make the help strings
    files_help = 'The files to subtract the wisp templates from. Wildcards are supported, e.g. ./data/*nrca3*_cal.fits'
    nproc_help = 'The number of processes to use during multiprocessing.'
    wisp_dir_help = 'The directory containing the wisp templates. The templates are assumed to have the form WISP_{DETECTOR}_{FILTER}_{PUPIL}.fits.'
    create_segmap_help = 'Option to make a source segmentation map to help with scaling the wisp template.'

    # Add the potential arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--files', dest='files', action='store', nargs='+', type=str, required=False, help=files_help, default='./*_cal.fits')
    parser.add_argument('--nproc', dest='nproc', action='store', type=int, required=False, help=nproc_help, default=6)
    parser.add_argument('--wisp_dir', dest='wisp_dir', action='store', type=str, required=False, help=wisp_dir_help, default='./')
    parser.add_argument('--create_segmap', dest='create_segmap', action=argparse.BooleanOptionalAction, required=False, help=create_segmap_help, default=True)
    
    # Add arguments for make_segmap()
    parser.add_argument('--seg_from_lw', dest='seg_from_lw', action=argparse.BooleanOptionalAction, required=False, default=True)
    parser.add_argument('--sigma', dest='sigma', action='store', type=float, required=False, default=0.8)
    parser.add_argument('--npixels', dest='npixels', action='store', type=int, required=False, default=10)
    parser.add_argument('--dilate_segmap', dest='dilate_segmap', action='store', type=int, required=False, default=5)
    parser.add_argument('--save_segmap', dest='save_segmap', action=argparse.BooleanOptionalAction, required=False, default=False)

    # Add arguments for subtract_wisp()
    parser.add_argument('--sub_wisp', dest='sub_wisp', action=argparse.BooleanOptionalAction, required=False, default=True)
    parser.add_argument('--gauss_smooth_wisp', dest='gauss_smooth_wisp', action=argparse.BooleanOptionalAction, required=False, default=False)
    parser.add_argument('--gauss_stddev', dest='gauss_stddev', action='store', type=float, required=False, default=3.0)
    parser.add_argument('--scale_wisp', dest='scale_wisp', action=argparse.BooleanOptionalAction, required=False, default=True)
    parser.add_argument('--scale_method', dest='scale_method', action='store', type=str, required=False, default='mad')
    parser.add_argument('--poly_degree', dest='poly_degree', action='store', type=int, required=False, default=5)
    parser.add_argument('--factor_min', dest='factor_min', action='store', type=float, required=False, default=0.0)
    parser.add_argument('--factor_max', dest='factor_max', action='store', type=float, required=False, default=2.0)
    parser.add_argument('--factor_step', dest='factor_step', action='store', type=float, required=False, default=0.01)
    parser.add_argument('--min_wisp', dest='min_wisp', action='store', type=float, required=False, default=None)
    parser.add_argument('--flag_wisp_thresh', dest='flag_wisp_thresh', action='store', type=float, required=False, default=None)
    parser.add_argument('--dq_val', dest='dq_val', action='store', type=int, required=False, default=1)
    parser.add_argument('--correct_rows', dest='correct_rows', action=argparse.BooleanOptionalAction, required=False, default=True)
    parser.add_argument('--correct_cols', dest='correct_cols', action=argparse.BooleanOptionalAction, required=False, default=False)
    parser.add_argument('--save_data', dest='save_data', action=argparse.BooleanOptionalAction, required=False, default=True)
    parser.add_argument('--save_model', dest='save_model', action=argparse.BooleanOptionalAction, required=False, default=True)
    parser.add_argument('--plot', dest='plot', action=argparse.BooleanOptionalAction, required=False, default=True)
    parser.add_argument('--show_plot', dest='show_plot', action=argparse.BooleanOptionalAction, required=False, default=False)
    parser.add_argument('--suffix', dest='suffix', action='store', type=str, required=False, default='_wisp')

    # Get the arguments
    args = parser.parse_args()

    return args


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


if __name__ == '__main__':

    # Get the command line arguments
    args = parse_args()

    # Process the input files
    results = process_files(**vars(args))
    print('subtract_wisp.py complete.')
