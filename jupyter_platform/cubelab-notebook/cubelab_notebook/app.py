from ipywidgets import (Button, GridBox, Layout)

from .widgets.menu_bar import MenuBar
from .widgets.plot_area import PlotArea
from .widgets.side_bar import SideBar


class Application(GridBox):

    def __init__(self, **kwargs):
        self._plot_area = PlotArea(
            description="Plot Area",
            layout=Layout(width='auto', grid_area='plot_area'))
        self._menu_bar = MenuBar(
            description="Menu Bar",
            layout=Layout(width='auto', grid_area='menu_bar'))
        self._side_bar = SideBar(
            description="Side Bar",
            layout=Layout(widget='auto', grid_area='side_bar'))
        self._footer = Button(
            description="Footer",
            layout=Layout(width='auto', grid_area='footer'))

        self._layout = Layout(
            width='100%',
            grid_template_rows='auto auto auto',
            grid_template_columns='33% 33% 33%',
            grid_template_areas='''
            "menu_bar menu_bar menu_bar"
            "plot_area plot_area side_bar"
            "footer footer footer"
            ''')

        super(Application, self).__init__(children=[self._menu_bar,
                                                    self._plot_area,
                                                    self._side_bar,
                                                    self._footer],
                                          layout=self._layout, **kwargs)

        self.setup_connections()

    def setup_connections(self):
        self._menu_bar.observe(self.render_plot, names='file_loaded')
        self._menu_bar.observe(self.update_side_bar, names='file_loaded')
        self._side_bar.observe(self.update_slice_index, names='slice_index')

    def render_plot(self, change):
        self._plot_area.render_data(change)

    def update_side_bar(self, change):
        self._side_bar.update(change)

    def update_slice_index(self, change):
        self._plot_area.update_slice_index(change['new'])
