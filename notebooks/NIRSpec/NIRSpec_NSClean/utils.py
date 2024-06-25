import os
import numpy as np
import requests

# ------ Plotting/Stats Imports ------
from matplotlib import pyplot as plt
from astropy.stats import sigma_clip
from astropy.io import fits


def get_jwst_file(name, mast_api_token=None, save_directory=".", redownload=False):
    """
    Retrieve a JWST data file from MAST archive and save it to a specified directory.

    Parameters:
    ----------
    name: str
        File name.
    mast_api_token: str
        MAST authorization token. Get your MAST Token Here: https://auth.mast.stsci.edu/token.
    save_directory: str
        Save directory path.
    redownload: bool
        Redownload the data even if it exsits already?
    """
    mast_url = "https://mast.stsci.edu/api/v0.1/Download/file"
    params = dict(uri=f"mast:JWST/product/{name}")

    if mast_api_token:
        headers = dict(Authorization=f"token {mast_api_token}")
    else:
        headers = {}

    file_path = os.path.join(save_directory, name)

    # Check if the file already exists in the save directory.
    if os.path.exists(file_path) and not redownload:
        print(f"The file {name} already exists in the directory. Skipping download.")
        return

    r = requests.get(mast_url, params=params, headers=headers, stream=True)
    r.raise_for_status()

    with open(file_path, "wb") as fobj:
        for chunk in r.iter_content(chunk_size=1024000):
            fobj.write(chunk)


# Define a helper function for plotting the dark areas (the mask).
def plot_dark_data(
    rate_file,
    mask_file,
    cmap="viridis",
    scale=0.2,
    slice_index=1,
    axis=0,
    aspect="auto",
    layout="rows",
):
    """
    Plot the dark areas on the detector, masking out the illuminated areas.
    This function can take 2D (_rate.fits) and 3D (_rateints.fits) files as input.

    Parameters:
    ----------
    rate_file: str
        File path to the FITS file containing countrate data.
    mask_file: str
        File path to the FITS file containing mask data.
    slice_index: int
        Index of the slice to be plotted, 2D data default is 1.
    axis: int (0-2)
        Axis along which the slice will be taken
        (0 for x-axis, 1 for y-axis, 2 for z-axis).
    aspect: int or 'auto'
        Plot's aspect ratio.
    cmap: str
        Color map.
    layout: str
        Layout subplots in rows or columns?
    scale: float
        Scaling factor applied to determine the intensity range for visualization.
    """

    # Make a matplotlib figure.
    if layout == "rows":
        fig, ax = plt.subplots(3, 1, figsize=(10, 5))
    else:
        fig, ax = plt.subplots(1, 3, figsize=(20, 5))
    plt.suptitle(f"Dark Areas for {os.path.basename(rate_file)}", fontsize=15)

    # Open the mask and science data.
    with fits.open(mask_file) as hdulist:
        mask = hdulist[1].data

    with fits.open(rate_file) as hdulist:
        sci = hdulist["SCI"].data

        # Determine if countrate data is 2D or 3D.
        if len(sci.shape) == 3:
            dim = 3
        else:
            dim = 2

    # Get data limits from the dark data.
    masked_sci = sci.copy()
    masked_sci[mask == 0] = 0
    vmin = np.nanpercentile(masked_sci, scale)
    vmax = np.nanpercentile(masked_sci, 100 - scale)

    # Plot the science image with limits from the dark data.
    sci[np.isnan(sci)] = 0

    # If the countrate data is 3D, determine the integration (slice) to plot.
    if dim == 3:
        sci = np.take(sci, slice_index, axis=axis)
        mask = np.take(mask, slice_index, axis=axis)
        masked_sci = np.take(masked_sci, slice_index, axis=axis)

        ax[0].set_title("Original Rate Data: Integration [{},:,:]".format(slice_index))
        ax[1].set_title(
            "Illuminated Pixel Mask: Integration [{},:,:]".format(slice_index)
        )
        ax[2].set_title(
            "Dark Data (Illuminated Pixels Masked): Integration [{},:,:]".format(
                slice_index
            )
        )

    else:
        sci = sci
        ax[0].set_title("Original Rate Data")
        ax[1].set_title("Illuminated Pixel Mask")
        ax[2].set_title("Dark Data (Illuminated Pixels Masked)")

    # Plot the science image with limits from the dark data.
    ax[0].set_ylabel("Pixel Row", fontsize=12)
    ax[0].set_xlabel("Pixel Column", fontsize=12)
    im1 = ax[0].imshow(
        sci, cmap=cmap, origin="lower", aspect=aspect, vmin=vmin, vmax=vmax
    )
    cbar1 = fig.colorbar(im1, ax=ax[0], pad=0.05, shrink=0.7, label="DN/s")

    # Plot the mask: values are 1 or 0.
    ax[1].set_ylabel("Pixel Row", fontsize=12)
    ax[1].set_xlabel("Pixel Column", fontsize=12)
    im2 = ax[1].imshow(mask, cmap=cmap, aspect=aspect, origin="lower", vmin=0, vmax=1)
    cbar2 = fig.colorbar(im2, ax=ax[1], pad=0.05, shrink=0.7, ticks=[0, 1])
    cbar2.set_ticklabels(["Illuminated Pixel Masked", "Un-Illuminated Pixel"])

    # Plot the dark data with the same limits as the science data.
    ax[2].set_ylabel("Pixel Row", fontsize=12)
    ax[2].set_xlabel("Pixel Column", fontsize=12)
    im3 = ax[2].imshow(
        masked_sci, cmap=cmap, aspect=aspect, origin="lower", vmin=vmin, vmax=vmax
    )
    cbar3 = fig.colorbar(im3, ax=ax[2], pad=0.05, shrink=0.7, label="DN/s")

    if layout == "rows":  # Adjust the multiplier as needed.
        cbar1.ax.figure.set_size_inches(cbar1.ax.figure.get_size_inches() * 1.2)
        cbar2.ax.figure.set_size_inches(cbar2.ax.figure.get_size_inches() * 1.2)
        cbar3.ax.figure.set_size_inches(cbar3.ax.figure.get_size_inches() * 1.2)

    fig.tight_layout()  # Adjusted tight_layout for better suptitle spacing.


# Define a helper function for plotting the cleaned data.
def plot_cleaned_data(
    rate_file,
    cleaned_file,
    slice_index=1,
    aspect="auto",
    cmap="viridis",
    scale=0.2,
    layout="rows",
):
    """
    Plot the 2D cleaned rate data (or 2D slice from a 3D cleaned data cube)
    and compare against the original data (not applying NSClean).

    Parameters:
    ----------
    rate_file: str
        File path to the FITS file containing original countrate data.
    cleaned_file: str
        File path to the FITS file containing cleaned countrate data.
    slice_index: int
        Index of the slice to be plotted, 2D data default is 1.
    aspect: int or 'auto'
        Plot's aspect ratio.
    cmap: str
        Color map.
    layout: str
        Layout subplots in rows or columns?
    scale: float
        Scaling factor applied to determine the intensity range for visualization.
    """

    # Make a matplotlib figure.
    if layout == "rows":
        fig, ax = plt.subplots(4, 1, figsize=(10, 12))
    else:
        fig, ax = plt.subplots(2, 2, figsize=(12, 10))
        ax = ax.flatten()
    plt.suptitle(
        f"Cleaned Data (1/f noise removed) for {os.path.basename(rate_file)}",
        fontsize=15,
        y=1,
    )

    # Open the original and cleaned data.
    with fits.open(rate_file) as hdulist:
        original = hdulist["SCI"].data

    with fits.open(cleaned_file) as hdulist:
        cleaned = hdulist["SCI"].data
        # Determine if rate data is 2D or 3D.
        if len(cleaned.shape) == 3:
            dim = 3
        else:
            dim = 2

    # Define image limits from the original data.
    vmin = np.nanpercentile(original, scale)
    vmax = np.nanpercentile(original, 100 - scale)

    original[np.isnan(original)] = 0
    cleaned[np.isnan(cleaned)] = 0

    # If the rate data is 3D, determine the integration (slice) to plot.
    if dim == 3:
        original = original[slice_index, :, :]
        cleaned = cleaned[slice_index, :, :]
        ax[0].set_title(
            "Original Rate Data: Integration [{},:,:]".format(slice_index), fontsize=15
        )
        ax[1].set_title(
            "Cleaned Rate Data: Integration [{},:,:]".format(slice_index), fontsize=15
        )

    else:
        ax[0].set_title("Original Rate Data", fontsize=12)
        ax[1].set_title("Cleaned Rate Data", fontsize=12)

    # Plot the original rate data.
    ax[0].set_xlabel("Pixel Column", fontsize=10)
    ax[0].set_ylabel("Pixel Row", fontsize=10)
    fig.colorbar(
        ax[0].imshow(
            original, cmap=cmap, origin="lower", aspect=aspect, vmin=vmin, vmax=vmax
        ),
        ax=ax[0],
        pad=0.05,
        shrink=0.7,
        label="DN/s",
    )

    # Plot the cleaned data with the same image limits.
    ax[1].set_xlabel("Pixel Column", fontsize=10)
    ax[1].set_ylabel("Pixel Row", fontsize=10)
    fig.colorbar(
        ax[1].imshow(
            cleaned, cmap=cmap, origin="lower", aspect=aspect, vmin=vmin, vmax=vmax
        ),
        ax=ax[1],
        pad=0.05,
        shrink=0.7,
        label="DN/s",
    )

    # Plot the relative difference between the original and cleaned data.
    diff = (original - cleaned) / original
    diff[~np.isfinite(diff)] = 0
    vmin_diff = np.nanpercentile(diff, scale)
    vmax_diff = np.nanpercentile(diff, 100 - scale)
    ax[2].set_title("Relative Difference (Original - Cleaned Rate Data)", fontsize=12)
    ax[2].set_xlabel("Pixel Column", fontsize=10)
    ax[2].set_ylabel("Pixel Row", fontsize=10)
    fig.colorbar(
        ax[2].imshow(
            diff,
            cmap=cmap,
            origin="lower",
            aspect=aspect,
            vmin=vmin_diff,
            vmax=vmax_diff,
        ),
        ax=ax[2],
        pad=0.05,
        shrink=0.7,
        label="DN/s",
    )

    # Plot the relative difference again,
    # this time hiding the outliers so that low-level
    # background changes can be seen.
    hide_outliers = np.ma.filled(sigma_clip(diff, masked=True), fill_value=0)
    vmin_outliers = np.nanpercentile(hide_outliers, scale)
    vmax_outliers = np.nanpercentile(hide_outliers, 100 - scale)
    ax[3].set_title(
        "Relative Difference (Original - Cleaned Rate Data) \n with Outliers Hidden",
        fontsize=12,
    )
    ax[3].set_xlabel("Pixel Column", fontsize=10)
    ax[3].set_ylabel("Pixel Row", fontsize=10)
    fig.colorbar(
        ax[3].imshow(
            hide_outliers,
            cmap=cmap,
            origin="lower",
            aspect=aspect,
            vmin=vmin_outliers,
            vmax=vmax_outliers,
        ),
        ax=ax[3],
        pad=0.05,
        shrink=0.7,
        label="DN/s",
    )

    fig.tight_layout()


# Define a helper function for plotting the 1D spectra.
def plot_spectra(
    spec_list,
    ext_num=1,
    scale_percent=2.0,
    wavelength_range=None,
    flux_range=None,
    xlim_low=None,
):
    """
    Plot the cleaned extracted 1D spectrum and compare against
    the original (not applying NSClean) extracted 1D spectrum.

    Parameters:
    ----------
    spec_list: list
        List of paths to the FITS files containing original/cleaned 1D extracted data.
    scale_percent: float
        Scaling factor applied to determine the intensity range for visualization.
    ext_num: int
        Index/extension of the slice to be plotted.
        The EXTVER header value. The default is 1 for 2D data.
    wavelength_range: dict
        Wavelength range (x-axis) {'nrs1': [3.6, 3.65], 'nrs2': [1.65, 1.75]}.
    flux_range: dict
        Flux range (y-axis) {'nrs1': [1, 2], 'nrs2': [1, 2]}.
    xlim_low: int
        Define a lower wavelength end for the 1D spectrum. Helpful for BOTS data.
    """

    if wavelength_range is None:
        wavelength_range = {}

    # Open the FITS files.
    original_hdul = fits.open(spec_list[0])
    cleaned_hdul = fits.open(spec_list[1])
    if len(spec_list) == 3:
        alternate_hdul = fits.open(spec_list[2])
    elif len(spec_list) == 4:
        alternate_hdul = fits.open(spec_list[2])
        handmod_hdul = fits.open(spec_list[3])
    else:
        alternate_hdul = None
        handmod_hdul = None

    # Find the spectral extension (EXTRACT1D).
    for extnum in range(len(original_hdul)):
        hdu = original_hdul[extnum]
        if hdu.name != "EXTRACT1D":
            continue
        slit_name = hdu.header["SLTNAME"]

        if hdu.header["EXTVER"] == ext_num:

            # Plot the original and cleaned spectra together.
            fig, ax = plt.subplots(1, 2, figsize=(10, 5))
            plt.suptitle(
                f"Compare 1D Spectra for {os.path.basename(spec_list[0])};"
                f"EXP_TYPE/Slit = {slit_name}",
                fontsize=15,
            )

            if "nrs1" in spec_list[0] and xlim_low is not None:
                xlim_low = xlim_low
            else:
                xlim_low = 0

            ax[0].step(
                hdu.data["WAVELENGTH"][xlim_low:],
                hdu.data["FLUX"][xlim_low:],
                linewidth=1,
                label="Original",
            )
            ax[0].step(
                cleaned_hdul[extnum].data["WAVELENGTH"][xlim_low:],
                cleaned_hdul[extnum].data["FLUX"][xlim_low:],
                linewidth=1,
                label="Cleaned",
            )
            ax[0].set_xlabel(f"Wavelength ({hdu.header['TUNIT1']})", fontsize=12)
            ax[0].set_ylabel(f"Flux ({hdu.header['TUNIT2']})", fontsize=12)
            ax[0].set_title("1D Extracted Spectra", fontsize=12)

            # Plot the difference between the spectra as a ratio.
            diff = (
                cleaned_hdul[extnum].data["FLUX"][xlim_low:]
                / hdu.data["FLUX"][xlim_low:]
            )
            ax[1].step(
                hdu.data["WAVELENGTH"][xlim_low:],
                diff,
                linewidth=1,
                label="Cleaned/Original",
            )
            ax[1].set_xlabel(f"Wavelength ({hdu.header['TUNIT1']})", fontsize=12)
            ax[1].set_ylabel("Cleaned/Original", fontsize=12)
            ax[1].set_title("Difference After Cleaning", fontsize=12)
            # print("Average Difference  = {}".format(np.nanmean(diff)))

            # If available, also plot the alternate spectra.
            if alternate_hdul is not None:
                ax[0].step(
                    alternate_hdul[extnum].data["WAVELENGTH"][xlim_low:],
                    alternate_hdul[extnum].data["FLUX"][xlim_low:],
                    linewidth=1,
                    label="Cleaned (alternate mask)",
                )
                diff2 = (
                    alternate_hdul[extnum].data["FLUX"][xlim_low:]
                    / hdu.data["FLUX"][xlim_low:]
                )
                ax[1].step(
                    hdu.data["WAVELENGTH"][xlim_low:],
                    diff2,
                    linewidth=1,
                    label="Cleaned (alternate mask)/Original",
                )
            if handmod_hdul is not None:

                ax[0].step(
                    handmod_hdul[extnum].data["WAVELENGTH"][xlim_low:],
                    handmod_hdul[extnum].data["FLUX"][xlim_low:],
                    linewidth=1,
                    label="Cleaned (hand-modified mask)",
                    color="Purple"
                )
                diff3 = (
                    handmod_hdul[extnum].data["FLUX"][xlim_low:]
                    / hdu.data["FLUX"][xlim_low:]
                )
                ax[1].step(
                    hdu.data["WAVELENGTH"][xlim_low:],
                    diff3,
                    linewidth=1,
                    label="Cleaned (hand-modified mask)/Original",
                )

            # Set the y-range of the plot if needed.
            if flux_range is not None:
                for key, y_range in flux_range.items():
                    if key.lower() in spec_list[0].lower() and y_range is not None:
                        if len(y_range) == 2:
                            ax[0].set_ylim(y_range)
                            ax[1].set_ylim(
                                [
                                    np.nanpercentile(diff, scale_percent),
                                    np.nanpercentile(diff, 100 - scale_percent),
                                ]
                            )
                            # ax[1].set_ylim(0.5, 1.5)

                        else:
                            all_flux = [
                                hdu.data["FLUX"],
                                cleaned_hdul[extnum].data["FLUX"],
                            ]
                            y_range_ax0 = [
                                np.nanpercentile(all_flux[0], scale_percent),
                                np.nanpercentile(all_flux[0], 100 - scale_percent),
                            ]
                            ax[0].set_ylim(y_range_ax0)
                            # ax[1].set_ylim(0.5, 1.5)

                            ax[1].set_ylim(
                                [
                                    np.nanpercentile(diff, scale_percent),
                                    np.nanpercentile(diff, 100 - scale_percent),
                                ]
                            )

            else:
                all_flux = [hdu.data["FLUX"], cleaned_hdul[extnum].data["FLUX"]]
                y_range_ax0 = [
                    np.nanpercentile(all_flux[0], scale_percent),
                    np.nanpercentile(all_flux[0], 100 - scale_percent),
                ]
                ax[0].set_ylim(y_range_ax0)
                # ax[1].set_ylim(0.5, 1.5)

                ax[1].set_ylim(
                    [
                        np.nanpercentile(diff, scale_percent),
                        np.nanpercentile(diff, 100 - scale_percent),
                    ]
                )

            # Set the x-range of the plot if needed.
            for key in wavelength_range:
                if key in spec_list[0] and wavelength_range[key] is not None:
                    ax[0].set_xlim(wavelength_range[key])
                    ax[1].set_xlim(wavelength_range[key])

            fig.tight_layout()

            ax[0].legend()
            ax[1].legend()

    original_hdul.close()
    cleaned_hdul.close()
    if alternate_hdul is not None:
        alternate_hdul.close()
        handmod_hdul.close()
