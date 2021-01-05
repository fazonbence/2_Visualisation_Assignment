import os

from bokeh.layouts import gridplot
from bokeh.plotting import curdoc, output_file, show

from data import HeartFailureProvider
from q1_dotplot import get_q1dot
from umap_scatter import get_umap

data_provider = HeartFailureProvider(
    "medical_data_embedding.csv", os.path.join("heart-failure", "static", "tiles_flat")
)

umap_scatter, img, img_info = get_umap(data_provider)
mainPlot, Plot1, Plot2 = get_q1dot(data_provider)

# output to static HTML file
# output_file("lines.html")
# show(final_plot)


curdoc().add_root(umap_scatter)
curdoc().add_root(img)
curdoc().add_root(img_info)
curdoc().add_root(mainPlot)
curdoc().add_root(Plot1)
curdoc().add_root(Plot2)
