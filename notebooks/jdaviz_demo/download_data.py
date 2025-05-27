import os
from pathlib import Path

import requests
from astroquery.mast import Observations

LOCAL_DATA_PATH = Path(__file__).parent / "data"


print(f"Downloading data to: {LOCAL_DATA_PATH}")

directory = Path(LOCAL_DATA_PATH)
directory.mkdir(parents=True, exist_ok=True)

uri_list = [
    "mast:JWST/product/jw01227-c1002_t005_nircam_clear-f335m_i2d.fits",
    "mast:JWST/product/jw01227-c1002_t005_nircam_clear-f277w_i2d.fits",
    "mast:JWST/product/jw01227-c1002_t005_nircam_clear-f444w_i2d.fits",
    "mast:JWST/product/jw01328-o018_t010_nirspec_g235h-f170lp_s3d.fits",
    "mast:HLSP/jades/dr3/goods-n/spectra/clear-prism/goods-n-mediumhst/hlsp_jades_jwst_nirspec_goods-n-mediumhst-00000604_clear-prism_v1.0_x1d.fits",
    "mast:HLSP/jades/dr3/goods-n/spectra/clear-prism/goods-n-mediumhst/hlsp_jades_jwst_nirspec_goods-n-mediumhst-00000755_clear-prism_v1.0_x1d.fits",
    "mast:HLSP/jades/dr3/goods-n/spectra/clear-prism/goods-n-mediumhst/hlsp_jades_jwst_nirspec_goods-n-mediumhst-00000755_clear-prism_v1.0_s2d.fits",
    "mast:HLSP/jades/dr3/goods-n/spectra/clear-prism/goods-n-mediumhst/hlsp_jades_jwst_nirspec_goods-n-mediumhst-00000604_clear-prism_v1.0_s2d.fits",
    "mast:HLSP/jades/dr3/goods-n/spectra/clear-prism/goods-n-mediumhst/hlsp_jades_jwst_nirspec_goods-n-mediumhst-00000804_clear-prism_v1.0_s2d.fits",
]

for file in uri_list:
    result = Observations.download_file(file, cache=True,
                                        local_path=LOCAL_DATA_PATH)
    print(result)


print("All files downloaded!")
