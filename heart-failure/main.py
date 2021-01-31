import os

from bokeh.plotting import curdoc

from control_panel import get_control_panel
from data import HeartFailureProvider
from q1_dotplot import get_q1dot
from q2_barplot import get_q2bar
from umap_scatter import get_umap

data_provider = HeartFailureProvider(
    "medical_data_embedding.csv", os.path.join("heart-failure", "static", "tiles_flat")
)

control_panel, filters = get_control_panel(data_provider)

umap_scatter, img, img_info = get_umap(data_provider, filters)
main_plot, plot1, plot2 = get_q1dot(data_provider, filters)
main_plot1 = get_q2bar(data_provider, filters)


curdoc().add_root(umap_scatter)
curdoc().add_root(img)
curdoc().add_root(img_info)
curdoc().add_root(main_plot)
curdoc().add_root(main_plot1)
curdoc().add_root(plot1)
curdoc().add_root(plot2)
curdoc().add_root(control_panel)
