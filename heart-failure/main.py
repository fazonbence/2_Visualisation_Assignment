from bokeh.plotting import curdoc

from data import HeartFailureProvider
from umap_scatter import get_umap

data_provider = HeartFailureProvider("medical_data_embedding.csv")

data_scr = data_provider.data_ds

umap_scatter = get_umap(data_provider)

curdoc().add_root(umap_scatter)
