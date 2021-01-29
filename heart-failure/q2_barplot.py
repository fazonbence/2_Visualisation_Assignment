from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource
from bokeh.models import ColumnDataSource, CDSView, BooleanFilter, Title
from bokeh.palettes import GnBu3, OrRd3
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

def get_q2bar(data_provider: HeartFailureProvider, extra_filters) -> Figure:
    
    main_plot = create_bar_plot(
        data_provider,
        "Healthy/Non-healthy patients among races",
        "main",
        extra_filters=extra_filters,
    )

    def create_bar_plot(
    data_provider: HeartFailureProvider,
    title: str,
    name: str,
    height: int = 500,
    width: int = 600,
    extra_filters: List[Filter] = None,
):
    if extra_filters is None:
        extra_filters = []

    TOOLTIPS = [
        ("index", "$index"),
        ("(x,y)", "($x, $y)"),
        ("filename", "@filename"),
    ]
    
           p1 = figure(
           y_range=data_provider.medical_data['Ethnic or Racial Group'].unique(), 
           tooltips=TOOLTIPS,
           tools="save",
           toolbar_location="left",
           plot_height=height, 
           plot_width=width 
           title="Healthy/Non-healthy by Races",
           toolbar_location=None,
           name=name,
           )
           p1.xaxis.axis_label = "Age"
           p1.yaxis.axis_label = "Ethnic group"


   p1 = figure(
        title=title,
        y_range=data_provider.medical_data["Ethnic or Racial Group"].unique(),
        tooltips=TOOLTIPS,
        tools="save",
        toolbar_location="left",
        plot_height=height,
        plot_width=width,
        name=name,
    )
    p1.xaxis.axis_label = "Number of patients"
    p1.yaxis.axis_label = "Ethnic group"
        
p1.hbar_stack(years, y='fruits', height=0.9, color=GnBu3, source=ColumnDataSource(exports),
             legend_label=["%s exports" % x for x in years])

p1.hbar_stack(years, y='fruits', height=0.9, color=OrRd3, source=ColumnDataSource(imports),
             legend_label=["%s imports" % x for x in years])

p1.y_range.range_padding = 0.1
p1.ygrid.grid_line_color = None
p1.legend.location = "top_left"
p1.axis.minor_tick_line_color = None
p1.outline_line_color = None

show(p)