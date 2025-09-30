import os
import numpy as np
import shutil
import matplotlib.gridspec as grd
import matplotlib.pyplot as plt
from jwst import datamodels
from itertools import cycle
from astropy.io import fits
from astropy.table import Table
from itables import show as show_table
from matplotlib.ticker import MultipleLocator
from scipy.stats import binned_statistic
from astropy.stats import sigma_clip
from matplotlib.patches import Patch
from matplotlib.pyplot import cm
from jwst.datamodels.dqflags import pixel as flags
try:
    import plotly.graph_objects as go # Determine if Plotly is installed.
    plotly_flag = True
except ImportError:
    print("Plotly package is not installed. Plotly plots will not be available.")
    plotly_flag = False


def read_msa_metadata_tables(msa_metafile):
    """
    Read the SHUTTER_INFO and SOURCE_INFO tables from an MSA metadata FITS file
    and return them in a format that is iterable/searchable.

    Parameters
    ----------
    msa_metafile: str
        Path to the MSA metadata FITS file.

    Returns
    -------
    shutter_info_table, source_info_table: pandas.DataFrame
        DataFrames containing the shutter information and source information tables.
    """

    metadata_tables = {}
    for hdu_name in ['SHUTTER_INFO', 'SOURCE_INFO']:
        table_data = Table.read(msa_metafile, format='fits', hdu=hdu_name)
        metadata_tables[hdu_name] = table_data.to_pandas().applymap(lambda x: x.decode() if isinstance(x, bytes) else x)

    return metadata_tables.get('SHUTTER_INFO'), metadata_tables.get('SOURCE_INFO')


def metafile_editor(source_slitlets,
                    metafile_og_path,
                    bkg_slitlets=[],
                    bkg_method='MB',
                    show_tables=False,
                    suffix=None):
    """
    Metafile Editor: Generates a new modified MSA metadata file based on the original MSA metadata file and a list of slits.
    Source slits can be treated as point or extended sources. Background sources are treated as extended sources.

    NOTE: This function was specifically created with JWST PID 1448.

    Parameters
    ----------
    source_slitlets : list
        List of MSA slitlet names to be treated as point sources.
    metafile_og_path : str
        Path to the original MSA metadata file.
    bkg_slitlets : list, optional
        List of MSA slitlet names to be treated as extended sources (background exposures). Default is an empty list.
    bkg_method : str, optional
        Background subtraction method. Can be 'P2P' (Pixel-to-pixel) or 'MB' (Master background). Default is 'MB'.
    show_tables : bool, optional
        Show the new MSA metadata file tables? Default is False.
    suffix : None,
        End of new file name.

    Returns
    -------
    metafile_table : str
        Path to the new MSA metadata file.
    """

    # ---------- New Metafile Setup ----------
    metafile_path = metafile_og_path[:-5] + ('_mb.fits' if suffix is None else suffix)
    shutil.copy(metafile_og_path, metafile_path)
    metafile_hdu = fits.open(metafile_path, 'update')

    total_dither_positions = max(metafile_hdu[2].data['dither_point_index'])

    metafile_shutter_info = fits.BinTableHDU.from_columns(metafile_hdu[2].columns,
                                                          nrows=len(source_slitlets + bkg_slitlets) * 3 *
                                                          total_dither_positions, fill=True)
    metafile_source_info = fits.BinTableHDU.from_columns(metafile_hdu[3].columns, nrows=len(source_slitlets),
                                                         fill=True)

    # ---------- Shutter Info Table ----------
    source_ids, source_types, seen = [], [], set()

    # Copy desired slitlets to the new shutter info table.
    new_slitlet_shutter_indx = 0
    for slitlet_indx, slitlet in enumerate(metafile_hdu[2].data['slitlet_id']):
        if any(str(slitlet) == slitlet_tuple[0] for slitlet_tuple in source_slitlets):
            metafile_shutter_info.data[new_slitlet_shutter_indx] = metafile_hdu[2].data[slitlet_indx]
            match_index = next(idx for idx, slitlet_tuple in enumerate(source_slitlets) if str(slitlet) == slitlet_tuple[0])
            source_id = metafile_hdu[2].data['source_id'][slitlet_indx]
            source_type = source_slitlets[match_index][1]
            if source_id not in seen:
                seen.add(source_id)
                source_ids.append(source_id)
                source_types.append(source_type)
            new_slitlet_shutter_indx += 1

        if bkg_method == 'MB' and str(slitlet) in bkg_slitlets:
            metafile_shutter_info.data[new_slitlet_shutter_indx] = metafile_hdu[2].data[slitlet_indx]
            metafile_shutter_info.data['background'][new_slitlet_shutter_indx] = 'Y'
            metafile_shutter_info.data['primary_source'][new_slitlet_shutter_indx] = 'N'
            new_slitlet_shutter_indx += 1

    metafile_hdu[2].data = metafile_shutter_info.data

    # ---------- Source Info Table ----------
    new_slitlet_source_indx = 0
    for source_indx, source in enumerate(metafile_hdu[3].data['source_id']):
        if source in source_ids:
            match_index_in_source_ids = source_ids.index(source)
            metafile_source_info.data[new_slitlet_source_indx] = metafile_hdu[3].data[source_indx]
            # Edit stellarity value if source is chosen to be point.
            if source_types[match_index_in_source_ids] == 'point':
                metafile_source_info.data['stellarity'][new_slitlet_source_indx] = 1
            new_slitlet_source_indx += 1

    metafile_hdu[3].data = metafile_source_info.data
    metafile_hdu.close()

    # ---------- Show Tables? ----------
    if show_tables:
        metadata_shutter_info, metadata_source_info = read_msa_metadata_tables(metafile_path)
        show_table(metadata_shutter_info)
        show_table(metadata_source_info)

    return metafile_path


def compile_background_spectra(x1d_files,
                               metadata_file,
                               background_slits=None,
                               trim_len=0):
    """
    This function compiles background data including wavelength, surface brightness, and error.
    It identifies background slitlets either from the provided list of background slitlets (slitlet_ids)
    or from the MSA metadata file SHUTTER_INFO table.

    Parameters
    ----------
    x1d_files : list
        List of X1D FITS file paths.
    background_slits : list of str, optional
        List of background slitlet IDs.
    metadata_file : str
        Path to MSA metadata file.
    trim_len : int, optional
        Length to trim from the beginning and end of the wavelength arrays. Default is 0.

    Returns
    -------
    all_wavelengths, all_fluxes, all_err : list
        List of wavelength, flux, and error arrays for each slitlet.
    """

    all_wavelengths, all_fluxes, all_err, slit_names = [], [], [], []

    shutter_table, source_table = read_msa_metadata_tables(metadata_file)  # Read in tables.

    # Loop through each x1d file -- No background subtraction applied.
    for x1d_file in sorted(x1d_files):
        background = datamodels.open(x1d_file)
        for slit in background.spec:
            if background_slits is None or str(slit.slitlet_id) in background_slits:
                index = np.where(shutter_table['slitlet_id'] == slit.slitlet_id)[0]
                if index.size > 0 and shutter_table['background'][index[0]] == 'Y':
                    slit_names.append(str(slit.slitlet_id))
                    wavelength = slit.spec_table["WAVELENGTH"][trim_len:-trim_len] if trim_len else slit.spec_table["WAVELENGTH"]
                    flux = slit.spec_table["SURF_BRIGHT"][trim_len:-trim_len] if trim_len else slit.spec_table["SURF_BRIGHT"]
                    err = slit.spec_table["SB_ERROR"][trim_len:-trim_len] if trim_len else slit.spec_table["SB_ERROR"]
                    all_wavelengths.append(wavelength)
                    all_fluxes.append(flux)
                    all_err.append(err)
    return all_wavelengths, all_fluxes, all_err, slit_names


def interpolate_onto_common_grid(all_wavelengths,
                                 all_fluxes,
                                 all_errors):
    """
    Interpolates spectra onto a common wavelength grid.

    Parameters
    ----------
    all_wavelengths : list of arrays
        Arrays of wavelength values for each spectrum.
    all_fluxes : list of arrays
        Arrays of flux values for each spectrum.
    all_errors : list of arrays or None
        Arrays of error values for each spectrum, or None if errors are not available.

    Returns
    -------
    common_wavelengths : array
        Common wavelength grid covering the range of all spectra.
    interpolated_flux : list of arrays
        Interpolated flux values for each spectrum on the common wavelength grid.
    interpolated_errors : list of arrays or None
        Interpolated error values for each spectrum on the common wavelength grid, or None if errors are not available.
    """

    # ---------- Define a common wavelength grid ----------

    min_wavelength = min(np.nanmin(w) for w in all_wavelengths)
    max_wavelength = max(np.nanmax(w) for w in all_wavelengths)
    n = max(len(w) for w in all_wavelengths)
    common_wavelengths = np.linspace(min_wavelength, max_wavelength, num=n)

    # ---------- Interpolate flux/error values onto the common grid ----------

    interpolated_flux = [np.interp(common_wavelengths, w, f) for w, f in zip(all_wavelengths, all_fluxes)]

    if all_errors:  # Interpolate error values if available
        interpolated_errors = [np.interp(common_wavelengths, w, err) for w, err in zip(all_wavelengths, all_errors)]

    return common_wavelengths, interpolated_flux, interpolated_errors


def replace_nans_with_median(data):
    """
    Replace NaN values with the median along each column.

    Parameters
    ----------
    data : np.ndarray
        Input data array with NaN values.

    Returns
    -------
    data : np.ndarray
        Data array with NaN values replaced by column-wise medians.
    """
    data = np.array(data)
    median_values = np.nanmedian(data, axis=0)
    nan_indices = np.isnan(data)
    data[nan_indices] = np.take(median_values, np.where(nan_indices)[1])
    return data


def filterout_contaminated_spectra(data,
                                   slit_names,
                                   mad_threshold=5,
                                   method=np.nanmedian):
    """
    Filters out spectra with outlier values using Median/Mean Absolute Deviation (MAD)

    Steps:
    1. Replace NaN values with the median along each column.
    2. Compute the median/mean spectrum.
    3. Calculate normalized deviations from the median/mean.
    4. Calculate median/mean absolute deviations (MAD) along the wavelength axis.
    5. Filter out spectra above the threshold.

    Parameters:
    -----------
    data : list of arrays
        Input data containing spectra.
    slit_names : list
        Names corresponding to each slit/spectrum in the data.
    mad_threshold : float, optional
        Threshold percent value for Median Absolute Deviation (MAD). Spectra with MAD values
        above this percent threshold will be considered as contaminated/many outliers and filtered out.
        Default is to filter anything that varies above the median/mean by 5%.
    method : function, optional
        Method to compute the median spectrum. Default is `np.nanmedian`.

    Returns:
    --------
    filtered_data : list of arrays
        Filtered spectra after removing outliers.
    slit_names : list
        Names of the background slits after filtering.
    """

    # Step 1: Replace NaN values.
    cleaned_data = replace_nans_with_median(data)

    # Step 2: Compute the median/mean spectrum.
    m_spectrum = method(cleaned_data, axis=0)

    # Step 3: Calculate deviations normalized by the median/mean spectrum.
    deviations = np.abs(cleaned_data - m_spectrum) / m_spectrum

    # Step 4: Calculate the Median/Mean Absolute Deviation (MAD).
    mad_values = np.nanmedian(deviations*100, axis=1)

    # Step 5: Identify and exclude outliers based on MAD.
    filtered_indices = np.where(np.array(mad_values) < mad_threshold)[0]
    filtered_data = cleaned_data[filtered_indices, :]

    num_outliers = cleaned_data.shape[0] - filtered_data.shape[0]
    print(f"Number of contaminated/outlier backgrounds {num_outliers}")

    slit_names = [name for i, name in enumerate(slit_names) if i in filtered_indices]

    return filtered_data, slit_names


def create_master_bkg(x1d_file,
                      common_wavelength,
                      median_bkg,
                      output_file='./user_supplied_mb.fits'):
    """
    Creates a master background FITS file with
    provided wavelength, surface brightness, and error arrays.

    Parameters
    ----------
    x1d_file : str
        Path to the input FITS file containing the original header and structure.
    common_wavelength : numpy.ndarray
        Array of common wavelengths for the background spectra.
    median_bkg : numpy.ndarray
        Array of median background surface brightness values.
    output_file : str
        New file name. Default is user_supplied_mb.fits.
    Returns
    -------
    output_file : str
        Path to the created FITS file containing the 1-D master background information.
    """
    # Open example FITS file.
    with fits.open(x1d_file) as hdul:
        # Create a primary HDU with the header from the input x1d_file.
        primary_hdu = fits.PrimaryHDU(header=hdul[0].header)

        # Create an empty table with the same columns as the original data.
        columns = hdul[1].columns
        empty_table = Table(np.zeros((len(median_bkg), len(columns)), dtype=np.float32), names=columns.names)

        # Set all values in the table to NaN where they were originally 0.
        for colname in empty_table.colnames:
            if colname != 'DQ':
                empty_table[colname] = np.where(empty_table[colname] == 0, np.nan, empty_table[colname])

        # Assign the wavelength, surface brightness, and error to the empty table.
        empty_table['WAVELENGTH'] = common_wavelength
        empty_table['SURF_BRIGHT'] = median_bkg
        # empty_table['SB_ERROR'] = standard_error_of_median

        # Create a new BinTableHDU with the empty table and header from the original x1d_file.
        empty_table_hdu = fits.BinTableHDU(empty_table, header=hdul[1].header)

        # Combine the primary HDU and the new BinTableHDU into an HDUList.
        hdul_out = fits.HDUList([primary_hdu, empty_table_hdu])

        # Write the HDUList to a FITS file.
        with open(output_file, 'wb') as fobj:
            hdul_out.writeto(fobj, overwrite=True)
        # hdul_out.writeto(output_file, overwrite=True)

        return output_file


def mean_background_variations(x1d_files,
                               metadata_file,
                               vetted_backgrounds=None,
                               bin_wavelengths=False,
                               bins=50,
                               y_lim=None,
                               mean_color="mediumvioletred",
                               trim_len=0,
                               save_figure=False,
                               sigma=3,
                               mad_threshold=5,
                               save_mb='./user_supplied_mb.fits'):
    """
    This function overlays all 1-D extracted vetted backgrounds and computes the mean background spectrum.
    Additionally, it calculates statistics for the coefficient of variation between each background and
    the mean. This analysis aids in assessing the uniformity of the background across the Field of View (FOV)
    of the Multi-Shutter Array (MSA). Additionally plots the spatial variation of the background across the MSA.

    Parameters
    ----------
    x1d_files : list of str
        A list of files containing the extracted 1-D background spectra.
    metadata_file : str
        File containing metadata for the observations.
    vetted_backgrounds : list of str, optional
        A list of the SLTNAME's for the vetted backgrounds.
    bin_wavelengths : bool, optional
        Bin the spectra?
    bins : int, optional
        Number of bins.
    y_lim : range, optional
        y-limits for background spectra plot.
    cmap : str
        Colormap.
    mean_color : str, optional
        Color of the calculated mean background plot.
    trim_len : int, optional
        Length to trim from the edges of the spectra.
    save_figure : bool, optional
        Option to save the figure.
    sigma : float, optional
        Sigma value for sigma clipping outliers.
    mad_threshold : float, optional
        Threshold percent value for Median Absolute Deviation (MAD). Spectra with MAD values
        above this percent threshold will be considered as contaminated/many outliers and filtered out.
        Default is to filter anything that varies above the median/mean by 5%.
    save_mb : str, None
        Name of saved 1-D master background.

    Returns
    -------
    mean_bkg : np.ndarray
        Mean background spectrum.
    slit_names_updated : list of str
        Filter background slits (un-contaminated).
    """

    # ---------- Set up the Figures ----------

    fig = plt.figure(figsize=(10, 8))
    gs = grd.GridSpec(2, 3, height_ratios=[3, 1], width_ratios=[4, 1, 1], hspace=0.1, wspace=0.05)
    ax = plt.subplot(gs[0, :2]) # Background spectra plot
    ax_residual = plt.subplot(gs[1, :2]) # Coefficient of variaiton plot
    ax_hist = plt.subplot(gs[1, 2:], sharey=ax_residual) # Coefficient of variaiton plot
    color_map = cycle(cm.Greys(np.linspace(0.7, 1.0, 12)))

    # ---------- Find the Vetted Backgrounds ----------
    all_wavelengths, all_fluxes, all_err, slit_names = compile_background_spectra(x1d_files,
                                                                                  metadata_file,
                                                                                  background_slits=vetted_backgrounds,
                                                                                  trim_len=trim_len)

    # ---------- Place all spectra on common wavelength grid ----------
    common_wavelengths, interpolated_flux, interpolated_errors = interpolate_onto_common_grid(all_wavelengths,
                                                                                              all_fluxes,
                                                                                              all_err)

    # ---------- Filter out the contaminated background spectra -----------
    if not vetted_backgrounds:
        filtered_data, slit_names_updated = filterout_contaminated_spectra(interpolated_flux, slit_names, mad_threshold=mad_threshold)
    else:
        filtered_data, slit_names_updated = interpolated_flux, slit_names

    # ---------- Calculate the Median Spectrum (sigma clipped) ----------
    clipped_data = np.array(filtered_data.copy()) # Make a copy of the original data
    clipped_data = sigma_clip(filtered_data, sigma=sigma, axis=0, maxiters=5, masked=True, cenfunc=np.nanmedian)

    # Set the clipped places in the error array to NaN
    masked_indices = np.where(clipped_data.mask)
    interpolated_errors = np.array(interpolated_errors)
    interpolated_errors[masked_indices] = np.nan
    clipped_err_nonan = replace_nans_with_median(interpolated_errors)

    clipped_data = np.array(clipped_data.filled(np.nan), copy=True)
    clipped_data_nonan = replace_nans_with_median(clipped_data)

    # Combine arrays into a list of tuples
    background_spectra = [
        (slit_names_updated[i], common_wavelengths, clipped_data_nonan[i], clipped_err_nonan[i])
        for i in range(len(slit_names_updated))]

    # ---------- Calculate Coefficient of Variation ----------

    mean_bkg = np.nanmean(clipped_data_nonan, axis=0)
    bkg_std = np.nanstd(clipped_data_nonan, axis=0)
    cov = (bkg_std/mean_bkg)

    # Calculate uncertainty_mean and uncertainty_std
    N = len(clipped_err_nonan)
    uncertainty_mean = np.sqrt(np.nansum(clipped_err_nonan ** 2, axis=0) / N) / np.sqrt(N)
    uncertainty_std = np.sqrt(np.nansum(clipped_err_nonan ** 2, axis=0) / (N - 1)) / np.sqrt(2)
    cov_unc = np.sqrt((uncertainty_std / bkg_std)**2 + (uncertainty_mean / mean_bkg)**2) * cov

    # Calculate weights based on uncertainties
    weights = 1 / ((cov_unc ** 2))
    weights[np.isinf(weights)] = np.nan

    # Calculate the means
    #  weighted_mean_cov = np.nansum(weights * cov) / np.nansum(weights)
    mean_cov = np.nanmean(cov)

    # Standard errors relative to mean cov
    regular_sem = np.nanstd(cov, ddof=1) / np.sqrt(len(cov))
    #  weighted_sem = np.sqrt(np.nansum((weights * np.nanstd(cov, ddof=1))**2)) / np.nansum(weights)

    print("Mean COV: " + str(mean_cov))
    print("Uncertainty of the Mean COV: " + str(regular_sem))

    # print("Weighted Mean COV: " + str(weighted_mean_cov))
    # print("Uncertainty of the Weighted COV Mean: " + str(weighted_sem))

    # ---------- Calculate the Variation of each background from the Mean ----------
    variations = [((np.abs(data[2]-mean_bkg))/mean_bkg)*100 for data in background_spectra]
    median_variation = np.nanmean(variations, axis=1)

    # Update background_spectra with variation and median_variation.
    for i in range(len(background_spectra)):
        background_spectra[i] = background_spectra[i] + (median_variation[i],)
    #  slit_var_from_mean = [(data[0], data[4]) for data in background_spectra]

    # ---------- Plot the Background Spectra & Mean ----------
    for i in range(clipped_data_nonan.shape[0]):
        flux = clipped_data_nonan[i, :]  # Access the i-th spectrum.
        # Bins can reduce noise for visualization purposes.
        if bin_wavelengths:
            bin_means = binned_statistic(common_wavelengths, flux, statistic=np.nanmean, bins=bins)
            ax.plot(bin_means[1][:-1], bin_means[0], label=slit_names_updated[i], color=next(color_map))
        else:
            ax.plot(common_wavelengths, flux, label=slit_names_updated[i], color=next(color_map))

    # Plot mean background
    if bin_wavelengths:
        bin_means2 = binned_statistic(common_wavelengths, mean_bkg, statistic=np.nanmean, bins=bins)
        ax.plot(bin_means2[1][:-1], bin_means2[0], color=mean_color, linewidth=3, label="Mean Background")
    else:
        ax.plot(common_wavelengths, mean_bkg, color=mean_color, linewidth=3, label="Mean Background")

    mean_patch = Patch(color=mean_color, label='Mean Background')
    ax.legend(handles=[mean_patch], loc='upper left', fontsize=16)
    ax.tick_params(axis='both', labelsize=14)
    #  ax.grid(alpha=0.4, which='both')
    ax.set_xticks([])
    fig.text(s='1.2 Min Zodi Benchmark Field Background Spectra', x=0.45, y=0.90, fontsize=18, ha='center', va='center')
    ax.set_ylabel("Surface Brightness (MJy/sr)", fontsize=16, labelpad=10)
    if y_lim:
        ax.set_ylim(y_lim[0], y_lim[1])

    ax_residual.errorbar(common_wavelengths, cov, yerr=cov_unc, color='black', fmt='.', markersize='0.9', elinewidth=1, ecolor=mean_color)
    ax_residual.set_xlabel("$\u03BB [\u03BC$m]", fontsize=16, labelpad=10)
    ax_residual.set_ylabel("Coefficient of Variation \n ($\u03C3_{backgrounds}$ / $X\u0304_{background}$)", fontsize=16, labelpad=10)
    ax_residual.grid(color='gray', linewidth=0.5, axis='y')
    ax_residual.tick_params(axis='both', labelsize=14)
    ax_residual.set_ylim(0, 0.10)
    ax_residual.grid(alpha=0.4)

    ax_hist.hist(cov, bins=len(cov), orientation='horizontal', ec=mean_color, fc=mean_color, alpha=0.3)
    ax_hist.tick_params(axis='y', labelleft=False)
    # ax_hist.axhline(y=weighted_mean_cov, color="darkblue",label="Weighted Mean COV", linestyle='--')
    ax_hist.axhline(y=np.nanmean(cov), color='lightseagreen', label="Mean COV", linestyle='--')
    ax_hist.set_xlabel("Count")
    ax_hist.legend(fontsize=6)
    ax_hist.grid(alpha=0.4)

    # Save the figure if required
    if save_figure:
        fig.savefig('./Benchmark_Field_Backgrounds.png', dpi=300, bbox_inches='tight')
        #  fig2.savefig('./msa_spatial_background_variation.png')  # Adjust the filename as needed

    if save_mb:
        output_file = create_master_bkg(x1d_files[0], common_wavelengths, mean_bkg)
        print(f"Master Background FITS file saved to {output_file}")
        return output_file, slit_names_updated
    else:
        return slit_names_updated


def plot_spectra(s2d_files, x1d_files, slit_names, scale=5, y_lim=None,
                 extraction_region=True, ystart_ystop=None, aspect='auto',
                 figsize=(15, 8), cmap='plasma', hist=True, bins=50, title=None,
                 ecolor='mediumvioletred', ycolor='r', fill_nan=False, MB=False,
                 plot_errors=False):
    """
    Plot 2-D and corresponding 1-D spectra side-by-side.

    Parameters:
    -----------
    s2d_files : list
        List of paths to the resampled 2-D spectra FITS files.
    x1d_files : list
        List of paths to the corresponding 1-D spectra FITS files.
    slit_names : list
        List of slit names (`SLTNAME` header keyword).
    scale : int, optional
        Percentage scale for colorbar range. Default is 5.
    y_lim: range
        Y-axis range for 1-D plot.
    extraction_region: bool
        Plot the [ystart, ystop] values for the 1-D extraction region?
    ystart_ystop: list of lists
        ystart and ystop values for the 1-D extraction regions (e.g., [[8.5],[13.5]]).
    aspect: int or 'auto'
        Aspect ratio of the 2-D plot axes.
    figsize:
        Size of figure.
    cmap: str
        Color map for the 2-D plot.
    hist: bool
        Plot the corresponding histogram to the 1-D plot?
    bins: int
        Number of bins for histogram.
    title: str
        Figure Title.
    ecolor: str
        1-D plot errorbar color.
    ycolor: str
        1-D Extraction region line color.
    fill_nan: bool
        Fill the NaN pixels in the 2-D spectrum with zero (only for plotting visualization)?
    MB: bool
        Is this a plot of the 1-D and 2-D master background spectra?
    plot_errors: bool
        Plot errorbars on the 1-D spectrum?

    Returns:
    -------
    None
    """

    # ---------- Setup the MB figure ----------

    if MB:
        fig = plt.figure(figsize=figsize, constrained_layout=True)
        fig.get_layout_engine().set(hspace=-100)

        gs = grd.GridSpec(len(slit_names)+1, 1, figure=fig, height_ratios=[2] + [1] * (len(slit_names)))
        ax_x1d = fig.add_subplot(gs[0])

    # Loop through all slits
    for indx, slit in enumerate(slit_names):

        # ---------- Setup the figures ----------

        if MB:
            ax = fig.add_subplot(gs[indx+1])
        else:
            fig = plt.figure(figsize=figsize, constrained_layout=True)

            # Plot histogram?
            if hist:
                gs = grd.GridSpec(2, 3, figure=fig, height_ratios=[1, 2], width_ratios=[2, 0.08, 0.1])
                ax = fig.add_subplot(gs[0, :1])
                ax_cbar = fig.add_subplot(gs[0, 1:2])
                ax_x1d = fig.add_subplot(gs[1, :1])
                ax_hist = plt.subplot(gs[1, 1:], sharey=ax_x1d)
                ax_hist.tick_params(axis='y', which='both', left=False, right=False, labelleft=False)

            else:
                gs = grd.GridSpec(2, 1, figure=fig, height_ratios=[1, 2])
                ax = fig.add_subplot(gs[0])
                ax_x1d = fig.add_subplot(gs[1, :])

        # ---------- Loop through the input files & plot ----------

        # Find the extension with the defined slit.
        for s2d_file, x1d_file in zip(s2d_files, x1d_files):
            with fits.open(s2d_file) as s2d_hdu:
                for ext, hdu in enumerate(s2d_hdu):
                    if 'SCI' in hdu.name and hdu.header['SLTNAME'] == slit:

                        # Define min/max scaling values for the 2-D plot.
                        vmin = np.nanpercentile(hdu.data, scale)
                        vmax = np.nanpercentile(hdu.data, 100-scale)

                        ax.yaxis.set_major_locator(MultipleLocator(10))

                        # Fill the NaNs with zero's just for plotting
                        data_without_nan = np.nan_to_num(hdu.data, nan=0)

                        if fill_nan:
                            img = ax.imshow(data_without_nan, aspect=aspect, vmin=vmin, vmax=vmax, origin='lower', cmap=cmap)
                        else:
                            img = ax.imshow(hdu.data, aspect=aspect, vmin=vmin, vmax=vmax, origin='lower', cmap=cmap)
                        ax.set_ylabel("Pixel Row", labelpad=15)

                        # Align the 2-D and 1-D plots based on wavelength.
                        ax.set_xticklabels([])  # Remove the tick labels.
                        a2 = ax.twiny()
                        a2.set_xlabel('Pixel Column', labelpad=15)
                        a2.set_xlim(0, hdu.data.shape[1])
                        a2.set_xticks(np.arange(0, hdu.data.shape[1], step=50))

                        if hist:
                            cbar = fig.colorbar(img, cax=ax_cbar, shrink=0.8, pad=-0.01, aspect=15)
                        else:
                            cbar = fig.colorbar(img, ax=ax, shrink=1, pad=-0.01, aspect=10)

                        cbar.ax.yaxis.get_offset_text().set(size=11, x=2)  # Set the font size for the offset text.
                        cbar.ax.yaxis.major.formatter._useMathText = True  # Enable the use of math text for the offset.
                        cbar.update_ticks()  # Update the ticks to reflect the changes.

                        if hdu.header['SRCTYPE'] == 'POINT':
                            cbar.set_label('MJy', labelpad=15)
                        else:
                            cbar.set_label('MJy/sr', labelpad=15)

            # Find the extension with the defined slit.
            with fits.open(x1d_file) as x1d_hdu:
                for ext, hdu in enumerate(x1d_hdu):
                    if ('EXTRACT1D' in hdu.name and (hdu.header['SLTNAME'] == slit or hdu.header['SLITID'] == int(slit))) or (MB and 'COMBINE1D' in hdu.name):

                        # Plot 1-D extraction region?
                        if extraction_region and not MB:

                            if ystart_ystop is not None:
                                ext_region_count = 0
                                for i in range(0, len(ystart_ystop), 2):
                                    ystart = ystart_ystop[i][0]
                                    ystop = ystart_ystop[i+1][0]

                                    ax.axhline(y=ystart, label='ystart={}'.format(ystart), c=ycolor, lw=0.8, ls='--', dashes=(10, 10))
                                    ax.axhline(y=ystop, label='ystop={}'.format(ystop), c=ycolor, lw=0.8, ls='--', dashes=(10, 10))
                                    ext_region_count += 1
                                    print(f"Slit {slit} Extraction Region {ext_region_count} | Y-START = {ystart} ; Y-STOP = {ystop}")

                            else:
                                ystart = hdu.header['EXTRYSTR']-1
                                ystop = hdu.header['EXTRYSTP']-1
                                print(f"Slit {slit}: Y-START = {ystart} ; Y-STOP = {ystop}")

                                ax.axhline(y=ystart, label='ystart={}'.format(ystart), c=ycolor, lw=0.8, ls='--', dashes=(10, 10))
                                ax.axhline(y=ystop, label='ystop={}'.format(ystop), c=ycolor, lw=0.8, ls='--', dashes=(10, 10))

                        # Define wavelength grid and ticks.
                        num_waves = len(hdu.data['WAVELENGTH'])
                        xticks = [1, 2, 3, 4, 5]
                        xtick_pos = np.interp(xticks, hdu.data['WAVELENGTH'], np.arange(num_waves))
                        xtick_labels = ['%.1f' % xtick for xtick in xticks]

                        if hdu.header['SRCTYPE'] == 'POINT':

                            ax_x1d.plot(np.arange(len(hdu.data['WAVELENGTH'])), hdu.data['FLUX'], color='k')

                            if plot_errors:
                                ax_x1d.fill_between(np.arange(len(hdu.data['WAVELENGTH'])),
                                                    hdu.data['FLUX']-hdu.data['FLUX_ERROR'],
                                                    hdu.data['FLUX']+hdu.data['FLUX_ERROR'], color=ecolor, alpha=0.3)

                            ax_x1d.set_ylabel("Flux (Jy)", labelpad=20)
                            if hist:
                                ax_hist.hist(hdu.data['FLUX'], bins=bins, ec=ecolor, fc=ecolor, alpha=0.3, orientation="horizontal")
                                ax_hist.set_xlabel("Counts")
                                ax_hist.grid(True, linestyle='--')

                        else:
                            ax_x1d.plot(np.arange(len(hdu.data['WAVELENGTH'])), hdu.data['SURF_BRIGHT'], color='k')

                            if plot_errors:
                                ax_x1d.fill_between(np.arange(len(hdu.data['WAVELENGTH'])),
                                                    hdu.data['SURF_BRIGHT']-hdu.data['SB_ERROR'],
                                                    hdu.data['SURF_BRIGHT']+hdu.data['SB_ERROR'], color=ecolor, alpha=0.3)

                            ax_x1d.set_ylabel("Surface Brightness (MJy/sr)", labelpad=20)
                            if hist:
                                ax_hist.hist(hdu.data['SURF_BRIGHT'], bins=bins, ec=ecolor, fc=ecolor, alpha=0.3, orientation="horizontal")
                                ax_hist.set_xlabel("Counts")
                                ax_hist.grid(True, linestyle='--')

                        ax_x1d.set_xlabel("$\u03BB [\u03BC$m]", labelpad=15)
                        ax_x1d.grid(True, linestyle='--')

                        # Plot ticks and limits.
                        if MB:
                            ax_x1d.set_xlim(0, num_waves)
                            ax_x1d.set_xticks(xtick_pos, [])
                            ax.set_xlim(0, num_waves)
                            ax.set_xticks(xtick_pos, xtick_labels)
                        else:
                            ax_x1d.set_xlim(0, num_waves)
                            ax_x1d.set_xticks(xtick_pos, xtick_labels)
                            ax.set_xlim(0, num_waves)
                            ax.set_xticks(xtick_pos)

                        # Titles.
                        if title:
                            ax.set_title(title, pad=20)
                        else:
                            if MB:
                                ax.set_title(os.path.basename(s2d_file) + '\n Slitlet ' + str(slit), pad=20)
                                ax_x1d.set_title(os.path.basename(x1d_file), pad=20)
                            else:
                                ax.set_title(os.path.basename(s2d_file)[:-9] + '\n Slitlet ' + str(slit), pad=20)
                                #  ax_x1d.set_title(os.path.basename(x1d_file) + '\n Slitlet ' + str(slit_name), pad=20)

                        # Set y-limits
                        if y_lim:
                            ax_x1d.set_ylim(y_lim[0], y_lim[1])

    plt.show()


def manually_define_dq_flags(rate_file_path, cal_file_path, slit_name, scale=0.2,
                             outlier_coords=None, update_dq=False, plotly=plotly_flag, cmap='RdBu'):

    """
    Plots the region on the countrate files corresponding to the specified MSA slitlet location.
    This function aids in identifying hot/bad pixels affecting spectra on the rate image.
    If outlier pixel locations are provided and update_dq = True, their DQ flags will be set to DO_NOT_USE.
    This function works best with Plotly, however, if Plotly is not installed a non-interactive plot will be output.

    Parameters:
    ----------
    rate_file_path: str
        The file path to the countrate file.
    cal_file_path: str
        The file path to the calibrated product file.
    slit_name: str
        The ID of the MSA slitlet.
    scale: float
        A scaling factor used to set the minimum and maximum values for plotting.
    outlier_coords: list
        A list of coordinate pairs [(x,y)] specifying outlier pixel locations on the rate image.
    update_dq: list
        A list of DQ flag updates corresponding to the outlier pixel locations.
    plotly: bool
        Use Plotly to output interactive plot?
    cmap: str
        Color map for the 2-D plot.

    Returns:
    -------
    None
    """

    # Open the rate FITS file.
    with fits.open(rate_file_path) as hdul_rate:
        # Extract DQ data from the rate FITS file.
        sci_data = hdul_rate['SCI'].data
        dq_data = hdul_rate['DQ'].data

    # Update the DQ flags to DO_NOT_USE.
    if update_dq:

        # Open the rate FITS file in update mode.
        with fits.open(rate_file_path, mode='update') as hdul_rate:
            # Extract DQ data from the rate FITS file.
            dq_data = hdul_rate['DQ'].data

            # Loop through the list of pixel locations and modify DQ values.
            for x, y in outlier_coords:
                dq_data[y, x] = 1  # Assuming (x, y) coordinates.

            # Update the DQ extension with the modified data.
            hdul_rate['DQ'].data = dq_data

            # Save the changes.
            hdul_rate.flush()
            print("DQ extension modified successfully.")

    # Open the calibration FITS file and find the slit.
    with fits.open(cal_file_path) as hdul_cal:
        if slit_name is not None:
            cal_hdu = None
            for hdu in hdul_cal:
                if 'SCI' in hdu.name:
                    header = hdu.header
                    if header.get('SLTNAME') == slit_name:
                        cal_hdu = hdu
                        break

            if cal_hdu is None:
                raise ValueError(f"No calibration extension found with SLTNAME '{slit_name}'")

            cal_header = cal_hdu.header

            # Extract SLTSTRT1 and SLTSTRT2 header values.
            sltstrt1 = cal_header.get('SLTSTRT1', None) - 1 # keywords are 1-based indexing
            sltstrt2 = cal_header.get('SLTSTRT2', None) - 1

            # Extract SLTSIZE1 and SLTSIZE2 header values.
            sltsize1 = cal_header.get('SLTSIZE1', None)
            sltsize2 = cal_header.get('SLTSIZE2', None)

            if sltstrt1 is None or sltstrt2 is None or sltsize1 is None or sltsize2 is None:
                raise ValueError("SLTSTRT1, SLTSTRT2, SLTSIZE1, or SLTSIZE2 not found in the calibration header")

            # Calculate full-frame coordinates for the section in the calibration data.
            cal_x_min = sltstrt1
            cal_x_max = sltstrt1 + sltsize1
            cal_y_min = sltstrt2
            cal_y_max = sltstrt2 + sltsize2

            spectrum_data = sci_data[cal_y_min:cal_y_max, cal_x_min:cal_x_max]

            # Calculate vmin and vmax based on the scale.
            vmin = np.nanpercentile(spectrum_data, scale)
            vmax = np.nanpercentile(spectrum_data, 100 - scale)

            # Create x and y coordinate arrays.
            x_coords = np.arange(spectrum_data.shape[1])
            y_coords = np.arange(spectrum_data.shape[0])

            if plotly:

                # Create hover text with location and intensity information.
                #  hover_text = [[f'X: {cal_x_min + x}, Y: {cal_y_min + y}<br>DN/s: {spectrum_data[y, x]}, DQ: #{dq_data[cal_y_min + y, cal_x_min + x]}' for x in x_coords] for y in y_coords]

                hover_text = [[f'X: {cal_x_min + x}, Y: {cal_y_min + y}<br>DN/s: {spectrum_data[y, x]}, DQ: {", ".join([flag for flag in flags if dq_data[cal_y_min + y, cal_x_min + x] & flags[flag]])}' for x in x_coords] for y in y_coords]

                # Create Plotly figure for the 2D spectrum.
                fig1 = go.Figure(data=go.Heatmap(z=spectrum_data, x=x_coords, y=y_coords, hoverinfo='text', hovertemplate='%{text}', text=hover_text,
                                                 colorscale=cmap, zmin=vmin, zmax=vmax))

                # Add red X markers for outlier pixels.
                if outlier_coords:
                    x_coords = [coord[0]-cal_x_min for coord in outlier_coords]
                    y_coords = [coord[1]-cal_y_min for coord in outlier_coords]
                    fig1.add_trace(go.Scatter(x=x_coords, y=y_coords, mode='markers', marker=dict(symbol='x', color='red'), name='Outlier Pixel'))

                # Update layout for the 2D spectrum.
                fig1.update_layout(title=f"RATE File {os.path.basename(rate_file_path)}, SLIT Name: {cal_header.get('SLTNAME', 'Unknown')}",
                                   xaxis_title='Pixel Column',
                                   yaxis_title='Pixel Row',
                                   coloraxis_colorbar=dict(title='DN/s', tickvals=[vmin, vmax],
                                                           ticktext=['Min', 'Max']))

                fig1.show()
            else:
                # Plot using Matplotlib.
                if outlier_coords:
                    num_outliers = len(outlier_coords)
                else:
                    num_outliers = 1
                num_cols = min(num_outliers, 4)  # Maximum 4 columns.
                num_rows = (num_outliers - 1) // num_cols + 1

                fig = plt.figure(figsize=(12, 6 + num_rows * 4))
                gs = grd.GridSpec(1 + num_rows, num_cols, figure=fig)

                # Plot full data in the first row.
                ax_full = plt.subplot(gs[0, :])
                im_full = ax_full.imshow(spectrum_data, origin='lower', aspect='auto',
                                         extent=[cal_x_min, cal_x_max, cal_y_min, cal_y_max],
                                         cmap='viridis', vmin=vmin, vmax=vmax, interpolation='nearest')
                ax_full.set_title(f"RATE File {os.path.basename(rate_file_path)}, SLIT Name: {cal_header.get('SLTNAME', 'Unknown')}")
                ax_full.set_xlabel('Pixel Column')
                ax_full.set_ylabel('Pixel Row')
                fig.colorbar(im_full, ax=ax_full, label='DN/s', shrink=0.5)

                # Mark outlier pixels with 'x'
                if outlier_coords:
                    for x, y in outlier_coords:
                        ax_full.scatter(x, y, marker='x', color='red')

                    # Plot zoomed-in regions in subsequent rows.
                    for idx, (x, y) in enumerate(outlier_coords):
                        row_idx = idx // num_cols + 1
                        col_idx = idx % num_cols
                        ax = plt.subplot(gs[row_idx, col_idx])

                        zoom_x_min = max((x-cal_x_min) - 10, 0)
                        zoom_x_max = min((x-cal_x_min) + 11, spectrum_data.shape[1])
                        zoom_y_min = max((y-cal_y_min) - 10, 0)
                        zoom_y_max = min((y-cal_y_min) + 11, spectrum_data.shape[0])

                        zoom_x_min_coord = max(x - 10, 0)
                        zoom_x_max_coord = min(x + 11, cal_x_max)
                        zoom_y_min_coord = max(y - 10, 0)
                        zoom_y_max_coord = min(y + 11, cal_y_max)

                        zoomed_region = spectrum_data[zoom_y_min:zoom_y_max, zoom_x_min:zoom_x_max]

                        im = ax.imshow(zoomed_region, origin='lower', cmap='viridis', extent=[zoom_x_min_coord, zoom_x_max_coord, zoom_y_min_coord, zoom_y_max_coord], vmin=vmin, vmax=vmax)
                        ax.set_title(f"Zoomed Region \n Around Pixel ({x}, {y})")
                        ax.set_xlabel('Pixel Column')
                        ax.set_ylabel('Pixel Row')
                        fig.colorbar(im, ax=ax, label='DN/s', shrink=0.3)

                    plt.tight_layout()
                    plt.show()
