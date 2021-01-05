from typing import List

from bokeh.io import output_file, show
from bokeh.models import (
    BoxZoomTool,
    CDSView,
    LassoSelectTool,
    ResetTool,
    TapTool,
    WheelZoomTool,
    ZoomInTool,
)
from bokeh.models.filters import Filter
from bokeh.palettes import colorblind
from bokeh.plotting import Figure, figure, output_file, show

import custom_filters as cf
from data import CDSView, HeartFailureProvider


def get_q1dot(data_provider: HeartFailureProvider) -> Figure:

    main_plot = create_dot_plot(
        data_provider, "Ethnic groups and time of infection", "main"
    )
    plot1 = create_dot_plot(
        data_provider,
        "Ethnic groups and time of infection\n with cardiomyopathy",
        "plot1",
        250,
        500,
        [cf.disease_subtype_cardiomyopathy],
    )
    plot2 = create_dot_plot(
        data_provider,
        "Ethnic groups and time of infection\n with ischemic cardiomyopathy",
        "plot2",
        250,
        500,
        [cf.disease_subtype_ischemiccardiomyopathy],
    )

    return main_plot, plot1, plot2


def create_dot_plot(
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
    mycols = colorblind["Colorblind"][4]
    view_male = CDSView(
        source=data_provider.data_ds,
        filters=[
            cf.females,
            cf.unique_id_bool(data_provider.medical_data.size),
            cf.diagnosis_sick,
        ]
        + extra_filters,
    )
    view_female = CDSView(
        source=data_provider.data_ds,
        filters=[
            cf.males,
            cf.unique_id_bool(data_provider.medical_data.size),
            cf.diagnosis_sick,
        ]
        + extra_filters,
    )
    view_remaining_male = CDSView(
        source=data_provider.data_ds,
        filters=[
            cf.males,
            cf.inverse_unique_id_bool(data_provider.medical_data.size),
            cf.diagnosis_sick,
        ]
        + extra_filters,
    )
    view_remaining_female = CDSView(
        source=data_provider.data_ds,
        filters=[
            cf.females,
            cf.inverse_unique_id_bool(data_provider.medical_data.size),
            cf.diagnosis_sick,
        ]
        + extra_filters,
    )

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
    p1.xaxis.axis_label = "Age"
    p1.yaxis.axis_label = "Ethnic group"

    p1.circle(
        x="Age",
        y="Ethnic or Racial Group",
        fill_alpha=0.2,
        size=10,
        source=data_provider.data_ds,
        legend_label="female",
        view=view_female,
        color=mycols[1],
        selection_line_color="black",
        selection_line_alpha=1,
        selection_line_width=2,
    )

    p1.circle(
        x="Age",
        y="Ethnic or Racial Group",
        fill_alpha=0.2,
        size=10,
        source=data_provider.data_ds,
        legend_label="male",
        view=view_male,
        color=mycols[0],
        selection_line_color="black",
        selection_line_alpha=1,
        selection_line_width=2,
    )

    p1.circle(
        x="Age",
        y="Ethnic or Racial Group",
        fill_alpha=0.2,
        size=10,
        source=data_provider.data_ds,
        legend_label="female",
        view=view_remaining_female,
        color="rgba(0, 0, 0, 0)",
        selection_line_color="black",
        selection_line_alpha=1,
        selection_line_width=2,
    )
    p1.circle(
        x="Age",
        y="Ethnic or Racial Group",
        fill_alpha=0.2,
        size=10,
        source=data_provider.data_ds,
        legend_label="male",
        view=view_remaining_male,
        color="rgba(0, 0, 0, 0)",
        selection_line_color="black",
        selection_line_alpha=1,
        selection_line_width=2,
    )

    p1.add_tools(LassoSelectTool())
    p1.add_tools(WheelZoomTool())
    p1.add_tools(ZoomInTool())
    p1.add_tools(ResetTool())
    p1.add_tools(BoxZoomTool())
    p1.add_tools(TapTool())

    p1.legend.location = "top_left"
    p1.legend.click_policy = "hide"
    return p1


if __name__ == "__main__":
    # execute only if run as a script
    data_provider = HeartFailureProvider("medical_data_embedding.csv")
    q1_dotplot = get_q1dot(data_provider)
    output_file("lines.html")
    show(q1_dotplot)
