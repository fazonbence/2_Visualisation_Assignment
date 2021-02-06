from bokeh.models import ResetTool, ZoomInTool
from bokeh.palettes import colorblind
from bokeh.plotting import Figure, figure
from bokeh.transform import dodge

from data import HeartFailureProvider


def get_q3_clustered(data_provider: HeartFailureProvider) -> Figure:
    list_eth = data_provider.medical_data["Ethnic or Racial Group"].unique()

    mycols = colorblind["Colorblind"][3]

    p = figure(
        x_range=list_eth,
        title="Ethnic Groups and Disease Subtypes",
        toolbar_location="left",
        name="q3_clustered",
    )

    p.vbar(
        x=dodge("Ethnic or Racial Group", -0.15, range=p.x_range),
        top="cardiomyopathy",
        width=0.2,
        source=data_provider.counts_subtypes_ds,
        color=mycols[0],
        legend_label="cardiomyopathy",
    )
    p.vbar(
        x=dodge("Ethnic or Racial Group", 0.15, range=p.x_range),
        top="ischemic cardiomyopathy",
        width=0.2,
        source=data_provider.counts_subtypes_ds,
        color=mycols[1],
        legend_label="ischemic cardiomyopathy",
    )

    p.xaxis.axis_label = "Ethnic group"

    p.yaxis.axis_label = "Number of Patients"
    p.x_range.range_padding = 0.1
    p.xgrid.grid_line_color = None
    p.legend.location = "top_left"
    p.legend.orientation = "horizontal"
    p.legend.click_policy = "hide"

    p.add_tools(ZoomInTool())
    p.add_tools(ResetTool())

    return p
