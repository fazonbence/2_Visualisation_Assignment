from bokeh.models import ColumnDataSource
from bokeh.plotting import Figure, figure
from bokeh.transform import dodge

from data import HeartFailureProvider


def get_q3_clustered(data_provider: HeartFailureProvider) -> Figure:
    df = data_provider.medical_data
    list_eth = df["Ethnic or Racial Group"].unique()

    p = figure(
        x_range=list_eth,
        title="Disease Sub-type based on Ethnic Groups",
        toolbar_location=None,
        name="q3_clustered",
    )

    p.vbar(
        x=dodge("Ethnic or Racial Group", -0.15, range=p.x_range),
        top="cardiomyopathy",
        width=0.2,
        source=data_provider.counts_subtypes_ds,
        color="#c9d9d3",
        legend_label="cardiomyopathy",
    )
    p.vbar(
        x=dodge("Ethnic or Racial Group", 0.15, range=p.x_range),
        top="ischemic cardiomyopathy",
        width=0.2,
        source=data_provider.counts_subtypes_ds,
        color="#718dbf",
        legend_label="ischemic cardiomyopathy",
    )

    p.xaxis.axis_label = "Ethnic group"

    p.yaxis.axis_label = "Number of Patients"
    p.x_range.range_padding = 0.1
    p.xgrid.grid_line_color = None
    p.legend.location = "top_left"
    p.legend.orientation = "horizontal"

    return p
