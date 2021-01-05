import os

from bokeh.layouts import gridplot
from bokeh.plotting import curdoc, output_file, show

from control_panel import get_control_panel
from data import HeartFailureProvider
from q1_dotplot import get_q1dot
from umap_scatter import get_umap

data_provider = HeartFailureProvider(
    "medical_data_embedding.csv", os.path.join("heart-failure", "static", "tiles_flat")
)

control_panel, filters = get_control_panel(data_provider)

umap_scatter, img, img_info = get_umap(data_provider, filters)
main_plot, plot1, plot2 = get_q1dot(data_provider, filters)

plots = [umap_scatter, main_plot, plot1, plot2]


# output to static HTML file
# output_file("lines.html")
# show(final_plot)


curdoc().add_root(umap_scatter)
curdoc().add_root(img)
curdoc().add_root(img_info)
curdoc().add_root(main_plot)
curdoc().add_root(plot1)
curdoc().add_root(plot2)
curdoc().add_root(control_panel)
