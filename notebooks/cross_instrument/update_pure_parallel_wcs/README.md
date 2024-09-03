# Pure_Parallels

A Python script that can be used to correct the WCS of pure parallel exposures. 

## Available Scripts

### `update_parallel_wcs.py`

Update CRVAL1 and CRVAL2 header keywords (which indicate the sky coordinates (RA and Dec) of the reference pixel) of Pure Parallel data. 

Run as follows:
```
python update_parallel_wcs.py fitsfile <verbosity>
```
where `fitsfile` is the input FITS file. The typical file that is input to this script is a file that was run through Stage 1 of the JWST calibration pipeline, i.e., a `_rate.fits` or `_rateints.fits` file. After the script has been run on the input file(s), one can then (re-)run Stage 2 of the JWST calibration pipeline (`calwebb_image2` and/or `calwebb_spec2`) on those files, which will now result in correct WCSes in the data headers (and corrected locations of spectral extractions in case of pure parallel WFSS data).

By default, `update_parallel_wcs.py` displays the input and output values of the CRVAL1/2 keywords when the script is run. One can avoid this by setting the optional parameter <verbosity> to anything other than `True`.

The script keeps track of its executions using a log file called "pure_parallel_wcs_logfile" in the current directory.


## Dependencies

The script mentioned above has external dependencies. It requires the packages astropy, mastquery, numpy, and pysiaf to be installed. The script assumes that an environment with the packages mentioned above has been installed on your machine and that you have loaded into that environment.

## Notebooks

### `NIRISS_correct_pure_parallel_WCS.ipynb`

This notebook illustrates the impact of the use of the `update_parallel_wcs.py` script.
