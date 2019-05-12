import numpy as np
import plotly.graph_objs as go
from ipywidgets import VBox


class PlotArea(VBox):
    def __init__(self, **kwargs):
        self._figure = go.FigureWidget(
            layout={
                'margin':
                    {
                        'l': 50,
                        'r': 50,
                        'b': 50,
                        't': 50,
                        'pad':4
                    }
            })

        self._current_view = '2D'

        super().__init__(children=[self._figure], **kwargs)

    def render_data(self, data):
        self._spec_cube = data['new']['cube']
        self._current_view = data['new']['view']

        if self._current_view == '1D':
            spec = self._spec_cube.mean(axis=(1, 2))

            self._figure.layout = {}
            self._figure.data = []
            self._figure.add_scatter(x = spec.spectral_axis.value,
                                     y = list(spec.data))
        elif self._current_view =='2D':
            self._figure.layout = {}
            self._figure.data = []

            self._figure.add_heatmap(
                z=self._spec_cube.unmasked_data[0, :, :],
                x=np.arange(self._spec_cube.shape[1]),
                y=np.arange(self._spec_cube.shape[2]))
        elif self._current_view == '3D':
            x, y, z = np.random.multivariate_normal(np.array([0, 0, 0]),
                                                    np.eye(3), 200).transpose()

            self._figure.layout = {}
            self._figure.data = []
            self._figure.add_scatter3d(
                x=x,
                y=y,
                z=z,
                mode='markers',
                marker=dict(
                    size=12,
                    line=dict(
                        color='rgba(217, 217, 217, 0.14)',
                        width=0.5
                    ),
                    opacity=0.8
                )
            )

    def update_slice_index(self, value):
        if self._current_view == '2D':
            data = self._figure.data[0]
            data.z = self._spec_cube.unmasked_data[value, :, :]