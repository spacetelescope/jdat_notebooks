from astropy.io import fits
from astropy.wcs import WCS
from ipywidgets import Button, HBox, Layout, Text, ToggleButtons
from spectral_cube import SpectralCube
from traitlets import Dict


class MenuBar(HBox):
    file_loaded = Dict()

    def __init__(self, **kwargs):
        self._load_textfield = Text(
            description="File Path",
            disabled=False,
            value="/Users/nearl/Downloads/manga-7495-12704-LOGCUBE.fits")

        self._load_button = Button(
            description="Load",
            disabled=False,
            layout=Layout(width='100px'))

        self._view_mode_buttons = ToggleButtons(
            options=['1D', '2D', '3D'],
            description="View Mode",
            disabled=False,
            style={'button_width': '50px'},
        )

        self._view_mode_buttons.value = '2D'

        super().__init__(children=[self._load_textfield, self._load_button,
                                   self._view_mode_buttons], **kwargs)

        self.setup_connections()

    def setup_connections(self):
        self._load_button.on_click(self._load_data_file)

    def _load_data_file(self, change):
        path = self._load_textfield.value

        with fits.open(path) as hdulist:
            spectral_cube = SpectralCube(data=hdulist[1].data,
                                         wcs=WCS(hdulist[1].header))

        self.file_loaded = {'cube': spectral_cube,
                            'view': self._view_mode_buttons.value}

