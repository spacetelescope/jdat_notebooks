from mirage.reference_files import downloader
download_path = os.environ['MIRAGE_DATA']
downloader.download_reffiles(download_path, instrument='all', dark_type='linearized', skip_darks=False, skip_cosmic_rays=False, skip_psfs=False, skip_grism=False)
