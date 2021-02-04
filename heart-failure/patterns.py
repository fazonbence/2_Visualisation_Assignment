from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.core.enums import HatchPattern
from bokeh.palettes import Spectral11

output_file("bar_basic.html")

pats = list(HatchPattern)
tops = [4,6,5,7,3,4,5,4,7,6,4]
numbers = [12]* 11
numbers[0] = 5
numbers[1] = 17
numbers[3] = 6
numbers[4] = 7
numbers[5] = 20
numbers[-2] = 8
numbers[-1] = 27

p = figure(x_range=pats, plot_height=350, plot_width=800, title="Hatch Patterns",
           toolbar_location=None, tools="")

p.vbar(x=pats, top=tops, width=0.9, alpha=0.6, fill_color=Spectral11, line_color="grey",
       hatch_pattern=pats, hatch_color="black", hatch_number=numbers, hatch_weight=0.5, hatch_alpha=0.5)

p.xgrid.grid_line_color = None
p.y_range.start = 0
p.xaxis.major_label_text_font_size = "18pt"

show(p)