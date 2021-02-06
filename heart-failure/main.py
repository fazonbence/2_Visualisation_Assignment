import os

from bokeh.plotting import curdoc

from clustered import get_clustered
from control_panel import get_control_panel
from data import HeartFailureProvider
from dotplot import get_dot
from stackedbar import get_bar
from umap_scatter import get_umap

data_provider = HeartFailureProvider(
    "medical_data_embedding.csv", os.path.join("heart-failure", "static", "tiles_flat")
)

control_panel = get_control_panel(data_provider)

umap_scatter, img, img_info = get_umap(data_provider)
dot1, dot2, dot3 = get_dot(data_provider)
stackedbar = get_bar(data_provider)
clustered_plot = get_clustered(data_provider)


curdoc().add_root(umap_scatter)
curdoc().add_root(img)
curdoc().add_root(img_info)
curdoc().add_root(dot1)
curdoc().add_root(stackedbar)
curdoc().add_root(dot2)
curdoc().add_root(dot3)
curdoc().add_root(control_panel)
curdoc().add_root(clustered_plot)
