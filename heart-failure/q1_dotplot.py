from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, CDSView, BooleanFilter
from bokeh.plotting import figure
from bokeh.models import (
    CategoricalColorMapper,
    ColumnDataSource,
    LassoSelectTool,
    WheelZoomTool,
    ZoomInTool,
    BoxZoomTool,
    ResetTool,
)
from bokeh.layouts import gridplot
import numpy as np
import pandas as pd
from data import HeartFailureProvider


def get_q1dot(data_provider: HeartFailureProvider) -> Figure:
    #flag import data correctly
    %store -r
    medical_data.head()