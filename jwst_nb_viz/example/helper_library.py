"""
To store parts of the notebook that should be "hidden" from the user.
"""

import numpy as np

import specutils

import glue_jupyter as gj
from glue import core as gcore

import ipywidgets


class SpectrumLineFinder:
    def __init__(self, spec, rest_lines):
        spec_data = gcore.Data(wl=spec.wavelength, flux=spec.flux, unc=spec.uncertainty.array)
        self.app = app = gj.jglue(spec_data)

        self.regions = {}  # populated with spectral regions by frecord

        line_selection = ipywidgets.Dropdown(options=rest_lines.keys(), description='Line:')
        record_button = ipywidgets.Button(description='Record line')
        result_text = ipywidgets.Text(disabled=True, value='No line recorded')


        record_box = ipywidgets.HBox([line_selection, record_button, result_text])


        z_text = ipywidgets.FloatText(description='z guess:', value=0)
        jump_button = ipywidgets.Button(description='Jump to line')
        line_width_text = ipywidgets.FloatText(description='width(Ang):', value=100)

        jump_box = ipywidgets.HBox([z_text, jump_button, line_width_text])


        def frecord(widget):
            wls_selected = spec_data['wl'][spec_data.subsets[0].to_index_list()]

            reg = specutils.SpectralRegion(np.min(wls_selected)*spec.wavelength.unit,
                                           np.max(wls_selected)*spec.wavelength.unit)
            result_text.value = 'Recorded {}: {} to {}'.format(line_selection.value, reg.lower, reg.upper)
            self.regions[line_selection.value] = reg

            z_text.value = specutils.analysis.centroid(spec, reg)/rest_lines[line_selection.value]-1
        record_button.on_click(frecord)


        self.plot_to_jump = None
        def fjump(widget):
            if self.plot_to_jump is None:
                return
            rest_linecen = rest_lines[line_selection.value]
            linecen = rest_linecen*(1+z_text.value)
            self.plot_to_jump.state.x_min = linecen.value + line_width_text.value/2
            self.plot_to_jump.state.x_max = linecen.value - line_width_text.value/2
        jump_button.on_click(fjump)

        self.action_vbox = ipywidgets.VBox([record_box, jump_box])

    def show(self):
        specplot = self.app.scatter2d('wl', 'flux')
        self.plot_to_jump = specplot

        # note that the line below *might* not work on some versions of
        # glupyter. If so, either manually do the brushing, or use this:
        # specplot.button_action.value = 'brush x'
        specplot.widget_button_interact.value = specplot.interact_brush_x
        specplot.state.x_min = 7050
        specplot.state.x_max = 7250

        return self.action_vbox

    def get_regions(self):
        return self.regions.copy()
