from ipywidgets import VBox, Accordion, Label, IntSlider
from traitlets import Int


class SideBar(VBox):
    slice_index = Int()

    def __init__(self, **kwargs):

        self._stats_view = StatsView()
        self._tools = Tools()

        self._side_bar = Accordion(children=[self._stats_view, self._tools])
        self._side_bar.set_title(0, 'Statistics')
        self._side_bar.set_title(1, 'Tools')

        super().__init__(children=[self._side_bar], **kwargs)

        self.setup_connections()

    def setup_connections(self):
        self._tools.observe(self._set_slice_index, names='slice_index')

    def _set_slice_index(self, change):
        self.slice_index = change['new']

    def update(self, change):
        spec_cube = change['new']['cube']
        view = change['new']['view']

        self._stats_view.data_points = spec_cube.size
        self._stats_view.data_shape = spec_cube.shape


class StatsView(VBox):
    def __init__(self, **kwargs):
        self._data_points = Label(value="Points: ")
        self._data_shape = Label(value="Shape: ")

        super().__init__(children=[self._data_points, self._data_shape], **kwargs)

    @property
    def data_points(self):
        return self._data_points.value

    @data_points.setter
    def data_points(self, value):
        self._data_points.value = "Points: {}".format(value)

    @property
    def data_shape(self):
        return self._data_shape.value

    @data_shape.setter
    def data_shape(self, value):
        self._data_shape.value = "Shape: {}".format(value)


class Tools(VBox):
    slice_index = Int()

    def __init__(self, **kwargs):
        self._slider = IntSlider(description="Slice")
        self._slider.observe(self.on_slider_value_changed, names='value')

        super().__init__(children=[self._slider], **kwargs)

    def on_slider_value_changed(self, change):
        self.slice_index = change['new']