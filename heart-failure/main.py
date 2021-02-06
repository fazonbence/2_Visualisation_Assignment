import os

from bokeh.plotting import curdoc

from control_panel import get_control_panel
from data import HeartFailureProvider
from q1_dotplot import get_q1dot
from q2_stackedbar import get_q2bar
from q3_clustered import get_q3_clustered
from umap_scatter import get_umap

data_provider = HeartFailureProvider(
    "medical_data_embedding.csv", os.path.join("heart-failure", "static", "tiles_flat")
)

control_panel = get_control_panel(data_provider)

umap_scatter, img, img_info = get_umap(data_provider)
main_plot, plot1, plot2 = get_q1dot(data_provider)
q2_plot = get_q2bar(data_provider)
q3_plot = get_q3_clustered(data_provider)


curdoc().add_root(umap_scatter)
curdoc().add_root(img)
curdoc().add_root(img_info)
curdoc().add_root(main_plot)
curdoc().add_root(q2_plot)
curdoc().add_root(plot1)
curdoc().add_root(plot2)
curdoc().add_root(control_panel)
curdoc().add_root(q3_plot)
