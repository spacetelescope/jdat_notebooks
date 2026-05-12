import os
import itertools
from collections import defaultdict

import numpy as np
from astropy.io import fits
from astropy.stats import sigma_clip
from astroquery.mast import Observations

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from astropy.visualization import ImageNormalize, ManualInterval, LogStretch
from astropy.visualization import LinearStretch, AsinhStretch, simple_norm

from jwst import datamodels
from jwst.associations import asn_from_list as afl
from jwst.associations.lib.rules_level3_base import DMS_Level3_Base

# Helper function to download JWST files from MAST.
def download_jwst_files(filenames,
                        download_dir,
                        mast_dir='mast:jwst/product'):
    """
    Helper function to download JWST files from MAST.

    Parameters:
    ----------
    filenames: list of str
        List of filenames to download.
    download_dir: str
        Directory where the files will be downloaded.
    mast_dir: str
        MAST directory containing JWST products.

    Returns:
    -------
    downloaded_files: list of str
        List of downloaded file paths.
    """
    # Download data.
    downloaded_files = []
    os.makedirs(download_dir, exist_ok=True)
    for filename in filenames:
        filename = os.path.basename(filename)
        mast_path = os.path.join(mast_dir, filename)
        local_path = os.path.join(download_dir, filename)
        if os.path.exists(local_path):
            print(local_path, 'EXISTS')
        else:
            # Can let this command check if local file exists.
            # However, it will delete it if it's there
            # and the wrong size (e.g., reprocessed).
            Observations.download_file(mast_path, local_path=local_path)
        downloaded_files.append(local_path)

    return downloaded_files

def add_fs_target(shutter_table,
                  source_table,
                  visit_rate_file,
                  slit_name,
                  ra, dec,
                  stellarity=1.0,
                  new_source_id=None):
    """
    Add a fixed-slit target to the MSA metadata file in the SHUTTER_INFO and SOURCE_INFO tables.
    Assumes the source is centered in the slit.

    Parameters
    ----------
    shutter_table : astropy.table.Table
        Table from the SHUTTER_INFO extension.
    source_table : astropy.table.Table
        Table from the SOURCE_INFO extension.
    visit_rate_file : str
        Path to a rate file from the visit.
    slit_name : str
        Fixed slit name.
    ra : float
        Source RA.
    dec : float
        Source DEC.
    stellarity : float, optional
        Source stellarity value. Use 1.0 for a point source and 0.0 for
        an extended source. Default is 1.0.
    new_source_id : int, optional
        Source ID to use. If not provided, the next available source ID
        is assigned.

    Returns
    -------
    new_slit_id : int
        Newly assigned slitlet ID.
    new_source_id : int
        Source ID used for the new source.
    shutter_table : astropy.table.Table
        Updated SHUTTER_INFO table.
    source_table : astropy.table.Table
        Updated SOURCE_INFO table.
    """

    # Read visit-specific metadata from the rate file header.
    header = fits.getheader(visit_rate_file)
    msa_meta_id = header['MSAMETID']
    program = header['PROGRAM']
    n_dithers = header['NUMDTHPT']
    
    # Create a fixed slit column in the table if it doesn't exist.
    if 'fixed_slit' not in shutter_table.colnames:
        shutter_table['fixed_slit'] = [''] * len(shutter_table)

    # Check if this fixed slit already exists for this visit.
    existing = (
        (shutter_table['fixed_slit'] == slit_name) &
        (shutter_table['msa_metadata_id'] == msa_meta_id)
    )

    if np.any(existing):
        print(f"{slit_name} already exists for msa_metadata_id={msa_meta_id}. Skipping.")
        existing_slit_id = shutter_table['slitlet_id'][existing][0]
        existing_source_id = shutter_table['source_id'][existing][0]
        return existing_slit_id, existing_source_id, shutter_table, source_table

    # Use the next available source ID if one is not provided.
    if new_source_id is None:
        new_source_id = np.max(source_table['source_id']) + 1
    
    # Use the next available slitlet ID.
    new_slit_id = np.max(shutter_table['slitlet_id']) + 1

    # Add one shutter row for each dither point.
    for dither in range(1, n_dithers+1):
        shutter_table.add_row({
            'dither_point_index': dither,
            'msa_metadata_id': msa_meta_id,
            'background': 'N',
            'estimated_source_in_shutter_x': 0.5,
            'estimated_source_in_shutter_y': 0.5,
            'primary_source': 'Y',
            'shutter_column': 0,
            'shutter_quadrant': 0,
            'shutter_row': 0,
            'shutter_state': 'OPEN',
            'slitlet_id': new_slit_id,
            'source_id': new_source_id,
            'fixed_slit': slit_name
        })

    # Add the source row.
    if new_source_id not in source_table['source_id']:
        source_table.add_row({
            'program': program,
            'source_id': new_source_id,
            'source_name': f'{program}_{new_source_id}',
            'alias': f'{new_source_id}',
            'ra': ra,
            'dec': dec,
            'preimage_id': 'None',
            'stellarity': stellarity
        })

    return new_slit_id, new_source_id, shutter_table, source_table

def writel3asn(scifiles, dir='./'):
    """
    Create a Level 3 association file.

    Parameters
    ----------
    scifiles : list of str
        List of all science exposure files.
    dir : str, optional 
        Save directory.
    
    Returns
    -------
    None.
    """
    # Filter based on GRATING/FILTER.
    grouped = defaultdict(lambda: {'sci': [], 'bg': []})

    for f in scifiles:
        k = (fits.getval(f, 'PROGRAM'), fits.getval(f, 'OBSERVTN'), fits.getval(f, 'FILTER'), fits.getval(f, 'GRATING'))
        grouped[k]['sci'].append(f)

    # Make ASN for each FILTER/GRATING.
    for (pid, obs, filt, grat), files in grouped.items():
        name = f"Program{pid}_{obs}_{filt}_{grat}".lower()
        asnfile = os.path.join(dir, f"{name}_l3asn.json")
        filenames = [os.path.basename(f) for f in files['sci']]
        asn = afl.asn_from_list(filenames, rule=DMS_Level3_Base, product_name=name)

        with open(asnfile, 'w') as f:
            f.write(asn.dump()[1])
    print("Level 3 ASN creation complete!")

def display_spectra(spectra,
                    compare_x1d=None,
                    compare_mast=None,
                    integration=None,
                    extname='data',
                    source_id=None,
                    source_unit='FLUX',
                    expand_wavelength_gap=True,
                    plot_resample=True,
                    plot_errors=False,
                    cmap='viridis',
                    bad_color=(1, 0.7, 0.7),
                    aspect='auto',
                    vmin=None,
                    vmax=None,
                    scale='asinh',
                    title_prefix=None,
                    title_path=False,
                    y_limits=None,
                    is_stage3=False):

    """
    Display 2D and 1D spectra (Stage 2/3).

    Parameters
    ----------
    spectra : list of str
        A list of data products (e.g., CAL, S2D, X1D files).
    compare_x1d : list of str, optional
        A list of 1D spectra for comparison (X1D files).
    compare_mast : list of str, optional
        A list of 1D spectra from MAST for comparison (X1D files).
    integration : {None, 'min', int}, optional
        Specifies the integration to use for multi-integration data.
        If 'min', the minimum value across all integrations is used.
        If an integer, the specific integration index is used (default 0).
     extname : str, optional
        The name of the data extension to extract ('data', 'dq', etc.).
    source_id : int or none, optional
        Identifier for the source/slit to be displayed. Default is None.
    source_unit : str, optional
        Override data source units ('POINT' == 'FLUX' or 'EXTENDED' = 'SURF_BRIGHT').
    expand_wavelength_gap : bool, optional
        If True, expands gaps in the wavelength data for better visualization.
    plot_resample : bool, optional
        If True, plots resampled (S2D) data products;
        otherwise, plots calibrated (CAL) data. Default is True.
    plot_errors : bool, optional
        If True, plots the error bands for the 1D spectra. Default is False.
    cmap : str, optional
        Colormap to use for displaying the images. Default is 'viridis'.
    bad_color : tuple of float, optional
        Color to use for bad pixels. Default is light red (1, 0.7, 0.7).
    aspect : str, optional
        Aspect ratio of the plot. Default is 'auto'.
    vmin : float, optional
        Minimum value for color scaling. If None, determined from the data.
    vmax : float, optional
        Maximum value for color scaling. If None, determined from the data.
    scale : {'linear', 'log', 'asinh'}, optional
        Scale to use for the image normalization. Default is 'asinh'.
    title_prefix : str, optional
        Optional prefix for the plot title.
    title_path : bool, optional
        If True, uses the full file path for the title;
        otherwise, uses the basename. Default is False.
    y_limits : tuple of float, optional
        Limits for the y-axis of the 1D spectrum plot.
        If None, limits are determined from the data.
    is_stage3 : bool, optional
        Plot stage 3 products? Default is False.

    Returns
    -------
    None.
    """

    # ---------------------------------Check Inputs---------------------------------
    spectra = [spectra] if isinstance(spectra, str) else spectra
    compare_x1d = [compare_x1d] if isinstance(compare_x1d, str) else compare_x1d
    compare_mast = [compare_mast] if isinstance(compare_mast, str) else compare_mast

    # Assign a default source_id if one was not supplied.
    if source_id is None:
        ftype = "cal"
        if plot_resample:
            ftype = "s2d"
        for file in spectra:
            if ftype in file:
                source_id = datamodels.open(file)[0].slits[0].source_id
                break

    # Plot stage 3 products?
    if is_stage3:

        # Stage 3 products: plot files if source_id is in filename OR SLTNAME in header
        def filter_prod(products, source_id):
            """Filter products based on filename OR header SLTNAME."""
            filtered = []
            for f in products:
                header = fits.getheader(f, ext=1)
                sltname = header.get('SLTNAME', '').lower() if header else ''
                if str(source_id).lower() in os.path.basename(f).lower() or sltname == str(source_id).lower():
                    filtered.append(f)
            return filtered

        spectra = filter_prod(spectra, source_id)
        compare_x1d = filter_prod(compare_x1d, source_id) if compare_x1d else None
        compare_mast = filter_prod(compare_mast, source_id) if compare_mast else None

    ftypes = {ftype: [f for f in spectra
                      if ftype in f] for ftype in ["cal", "s2d", "x1d"]}
    products = sorted(ftypes['s2d']) if plot_resample else sorted(ftypes['cal'])
    if not products:
        raise ValueError("No valid data products found for plotting.")

    # --------------------------------Set up figures-------------------------------
    total_plots = len(products) + bool(ftypes['x1d'])
    height_ratios = [1] * len(products) + ([3] if bool(ftypes['x1d']) else [])
    fig, axes = plt.subplots(total_plots, 1, figsize=(15, 5 * total_plots),
                             sharex=False, height_ratios=height_ratios)
    fig.subplots_adjust(hspace=0.2, wspace=0.2)
    ax2d, ax1d = (axes[:-1], axes[-1]) if bool(ftypes['x1d']) else (axes, None)

    cmap = plt.get_cmap(cmap)  # Set up colormap and bad pixel color.
    cmap.set_bad(bad_color, 1.0)
    colors = plt.get_cmap('tab10').colors
    color_cycle = itertools.cycle(colors)

    # ---------------------------------Plot spectra--------------------------------
    for i, product in enumerate(products):
        model = datamodels.open(product)  # Open files as JWST datamodels.

        # Extract the correct 2D source spectrum if there are multiple.
        slit_m = model
        if 'slits' in model:
            slits = model.slits
            slit_m = next((s for s in slits
                           if getattr(s, 'name', None) == source_id), None)
            slit_m = slit_m or next((s for s in model.slits
                                     if s.source_id == source_id), None)
            if not slit_m:
                print(f"'{source_id}' not found/invalid.")
                print(f"Available source_ids: {[s.source_id for s in slits][:5]}")
                break

        # Check if 'fixed_slit' exists, otherwise fall back to 'slitlet_id'
        slit_name = (f"SLIT: {getattr(slit_m, 'name', None) or slit_m.slitlet_id}, "
                     f"SOURCE: {getattr(slit_m, 'source_id', '')}")

        # -----------------------Extract the 2D/3D data----------------------
        data_2d = getattr(slit_m, extname)
        if data_2d.ndim == 3:  # Handle multi-integration data.
            if integration == 'min':
                data_2d = np.nanmin(data_2d, axis=0)
            elif isinstance(integration, int) and 0 <= integration < data_2d.shape[0]:
                data_2d = data_2d[integration]
            else:
                raise ValueError(f"Invalid integration '{integration}' for 3D data.")

        # -----------Convert from pixels to wavelength (x-axis)--------------
        wcsobj = slit_m.meta.wcs  # Obtaining the WCS object from the meta data.
        y, x = np.mgrid[:slit_m.data.shape[0], :slit_m.data.shape[1]]
        # Coordinate transform from detector space (pixels) to sky (RA, DEC).
        det2sky = wcsobj.get_transform('detector', 'world')
        ra, dec, s2dwave = det2sky(x, y)  # RA/Dec, wavelength (microns) for each pixel.
        s2dwaves = s2dwave[0, :]  # Single row since this is the rectified spectrum.
        x_arr = np.arange(0, slit_m.data.shape[1], int(len(slit_m.data[1]) / 4))
        wav = np.round(s2dwaves[x_arr], 2)  # Populating the wavelength array.
        ax2d[i].set_xticks(x_arr, wav)

        # ---------------------------Scale the data-------------------------
        sigma_clipped_data = sigma_clip(np.ma.masked_invalid(data_2d), sigma=5, maxiters=3)
        vmin = np.nanmin(sigma_clipped_data) if vmin is None else vmin
        vmax = np.nanmax(sigma_clipped_data) if vmax is None else vmax
        stretch_map = {'log': LogStretch(), 'linear': LinearStretch(),
                       'asinh': AsinhStretch()}
        if scale in stretch_map:
            norm = ImageNormalize(sigma_clipped_data,
                                  interval=ManualInterval(vmin=vmin, vmax=vmax),
                                  stretch=stretch_map[scale])
        else:
            norm = simple_norm(sigma_clipped_data, vmin=vmin, vmax=vmax)

        # -------------------------Plot 1D Spectra-------------------------
        for k, (prods_1d, prefix) in enumerate([(sorted(ftypes['x1d']),
                                                 f'{title_prefix} '),
                                                (compare_x1d, 'RE-EXTRACTION '),
                                                (compare_mast, 'MAST ')]):
            if prods_1d:
                model_1d = datamodels.open(prods_1d[i])
                specs = model_1d.spec
                spec = next((s for s in specs if
                             getattr(s, 'name', None) == source_id), None)
                spec = spec or next((s for s in specs
                                     if s.source_id == source_id), None)

                if spec:
                    tab = spec.spec_table
                    wave = tab.WAVELENGTH
                    flux = tab.FLUX if source_unit == 'FLUX' else tab.SURF_BRIGHT
                    errs = tab.FLUX_ERROR if source_unit == 'FLUX' else tab.SB_ERROR

                    # Expand the array to visualize the wavelength gap.
                    if expand_wavelength_gap:
                        dx1d_wave = wave[1:] - wave[:-1]
                        igap = np.argmax(dx1d_wave)
                        dx_replace = (dx1d_wave[igap - 1] + dx1d_wave[igap + 1]) / 2.
                        nfill = int(np.round(np.nanmax(dx1d_wave) / dx_replace))

                        if nfill > 1:
                            print(nfill)
                            print(f"Expanding wavelength gap {wave[igap]:.2f} "
                                  f"-- {wave[igap + 1]:.2f} μm")

                            wave_fill = np.mgrid[wave[igap]:wave[igap + 1]:(nfill + 1) * 1j]
                            wave = np.concatenate([wave[:igap + 1],
                                                   wave_fill[1:-1],
                                                   wave[igap + 1:]])

                            if prefix != 'RE-EXTRACTION ':
                                num_rows, num_waves = data_2d.shape
                                fill_2d = np.zeros(shape=(num_rows, nfill - 1)) * np.nan
                                data_2d = np.concatenate([data_2d[:, :igap + 1],
                                                          fill_2d, data_2d[:, igap + 1:]],
                                                         axis=1)

                            fill = np.zeros(shape=(nfill - 1)) * np.nan
                            flux = np.concatenate([flux[:igap + 1], fill, flux[igap + 1:]])
                            errs = np.concatenate([errs[:igap + 1], fill, errs[igap + 1:]])
                    else:
                        nfill = 0

                    # ----------------Construct legends and annotations-----------------
                    detector = slit_m.meta.instrument.detector
                    ffilter = slit_m.meta.instrument.filter
                    grating = slit_m.meta.instrument.grating
                    dither = model.meta.dither.position_number
                    label_2d = f'{grating}/{ffilter}'
                    label_1d = f'{detector} ({grating}/{ffilter})'
                    if not is_stage3:
                        label_2d = f'Dither/Nod {dither} ({label_2d})'
                        label_1d = (f'{prefix} Dither/Nod {dither} {label_1d}')
                    else:
                        label_1d = f'{prefix}{label_1d}'
                    ax2d[i].annotate(label_2d, xy=(1, 1), xycoords='axes fraction',
                                     xytext=(-10, -10), textcoords='offset points',
                                     bbox=dict(boxstyle="round,pad=0.3",
                                               edgecolor='white',
                                               facecolor='white', alpha=0.8),
                                     fontsize=12, ha='right', va='top')

                    title_2d = (f"{title_prefix + ' ' if title_prefix else ''}"
                                f"{model.meta.filename} | {slit_name}")
                    if integration:
                        title_2d = title_2d.replace('.fits', f'[{integration}].fits')
                    ax2d[i].set_title(title_2d, fontsize=14)
                    if not bool(ftypes['x1d']):
                        ax2d[i].set_xlabel("Wavelength (μm)", fontsize=12)
                    ax2d[i].set_ylabel("Pixel Row", fontsize=12)
                    # ax2d[i].legend(fontsize=12)

                    # ------------------------------------------------------------------

                    num_waves = len(wave)
                    color = next(color_cycle)
                    ax1d.step(wave, flux, lw=1, label=label_1d, color=color)
                    if plot_errors:
                        ax1d.fill_between(np.arange(num_waves), flux - errs,
                                          flux + errs, color='grey', alpha=0.3)
                    ax1d.legend(fontsize=12)
                    ax1d.set_title(f"{title_prefix + ' ' if title_prefix else ''}"
                                   f"Extracted 1D Spectra | {slit_name}", fontsize=14)
                    ax1d.set_ylabel("Flux (Jy)" if source_unit == 'FLUX'
                                    else "Surface Brightness (MJy/sr)", fontsize=12)
                    ax1d.set_xlabel("Wavelength (μm)", fontsize=12)

                    ax1d.set_ylim(y_limits or (np.nanpercentile(flux, 1),
                                               np.nanpercentile(flux, 99.5)))

                    # --------------------Plot the 2D spectra & colorbar---------------
                    plt.subplots_adjust(left=0.05, right=0.85)
                    if k == 0:
                        im = ax2d[i].imshow(data_2d, origin='lower',
                                            cmap=cmap, norm=norm,
                                            aspect=aspect, interpolation='nearest')
                        units = slit_m.meta.bunit_data
                        cbar_ax = fig.add_axes([ax2d[i].get_position().x1 + 0.02,
                                                ax2d[i].get_position().y0, 0.02,
                                                ax2d[i].get_position().height])
                        cbar = fig.colorbar(im, cax=cbar_ax)
                        cbar.set_label(units, fontsize=12)

                    # ----------------------Add extraction region---------------------
                    ystart, ystop, xstart, xstop = (spec.extraction_ystart - 1,
                                                    spec.extraction_ystop - 1,
                                                    spec.extraction_xstart - 1,
                                                    spec.extraction_xstop - 1)
                    extract_width = ystop - ystart + 1
                    box = Rectangle((xstart, ystart), xstop - xstart + nfill,
                                    extract_width, fc='None', ec=color,
                                    lw=2, label=prefix)
                    ax2d[i].add_patch(box)
                    ax2d[i].legend()
