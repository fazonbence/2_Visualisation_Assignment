from bokeh.plotting import curdoc

from data import HeartFailureProvider
from umap_scatter import get_umap
from q1_dotplot import get_q1dot
from bokeh.layouts import gridplot
from bokeh.plotting import figure, output_file, show

data_provider = HeartFailureProvider("medical_data_embedding.csv")

umap_scatter = get_umap(data_provider)
#q1_dotplot = get_umap(data_provider)
q1_dotplot = get_q1dot(data_provider)

final_plot=gridplot([[umap_scatter, q1_dotplot]])

#curdoc().add_root(final_plot)
# output to static HTML file
output_file("lines.html")
show(final_plot)
#curdoc().add_root(umap_scatter)
