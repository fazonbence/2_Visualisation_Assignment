import os

from bokeh.layouts import gridplot
from bokeh.models import CustomJS, Div
from bokeh.plotting import curdoc, figure, output_file, show

from data import HeartFailureProvider
from q1_dotplot import get_q1dot
from umap_scatter import get_umap

data_provider = HeartFailureProvider(
    "medical_data_embedding.csv", os.path.join("heart-failure", "static", "tiles_flat")
)

umap_scatter, img, img_info = get_umap(data_provider)
# q1_dotplot = get_umap(data_provider)
q1_dotplot = get_q1dot(data_provider)

final_plot = gridplot([[umap_scatter, q1_dotplot, img, img_info]])

# curdoc().add_root(final_plot)
# output to static HTML file
output_file("lines.html")
show(final_plot)
# curdoc().add_root(umap_scatter)


# curdoc().add_root(umap_scatter)
# curdoc().add_root(img)
# curdoc().add_root(img_info)
