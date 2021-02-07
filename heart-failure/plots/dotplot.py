from typing import List, Tuple

from bokeh.models import (
    BoxZoomTool,
    CDSView,
    HoverTool,
    LassoSelectTool,
    ResetTool,
    TapTool,
    Title,
    WheelZoomTool,
    ZoomInTool,
)
from bokeh.models.filters import Filter
from bokeh.palettes import colorblind
from bokeh.plotting import Figure, figure

import custom_filters as cf
from data import HeartFailureProvider


def get_dot(data_provider: HeartFailureProvider,) -> Tuple[Figure, Figure, Figure]:
    """Return three dot plots of ethnic groups and age of transplant.

    Parameters
    ----------
    data_provider : HeartFailureProvider
        Application data provider

    Returns
    -------
    Figure
        Dot plot of ethnic groups and age of transplant, considering all subtypes
    Figure
        Dot plot of ethnic groups and age of transplant, considering only patients with
        cardiomyopathy
    Figure
        Dot plot of ethnic groups and age of transplant, considering only patients with
        ischemic cardiomyopathy
    """

    main_plot = create_dot_plot(
        data_provider, "Ethnic groups and age of transplant", "dot1",
    )
    plot1 = create_dot_plot(
        data_provider,
        "Ethnic groups and age of transplant\nwith cardiomyopathy",
        "dot2",
        250,
        500,
        [cf.disease_subtype_cardiomyopathy],
    )
    plot2 = create_dot_plot(
        data_provider,
        "Ethnic groups and age of transplant\nwith ischemic cardiomyopathy",
        "dot3",
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
) -> Figure:
    """Return dot plot with given title, name, height, width and extra_filters applied.

    Parameters
    ----------
    data_provider : HeartFailureProvider
        Application data provider
    title : str
        Title of the plot
    name : str
        Name of the plot. Needed for HTML template
    height : int, optional
        Height of the plot, by default 500
    width : int, optional
        Width of the plot, by default 600
    extra_filters : List[Filter], optional
        Filters that may be applied to filter the data source, by default None.

    Returns
    -------
    Figure
        Dot plot
    """
    if extra_filters is None:
        extra_filters = []

    TOOLTIPS = [
        ("Patient Id", "@{Patient Id}"),
        ("Age", "@Age"),
        ("Disease Subtype", "@{Disease Subtype}"),
        ("Filename", "@filename"),
    ]
    mycols = colorblind["Colorblind"][4]
    view_male = CDSView(
        source=data_provider.data_ds,
        filters=[
            cf.males,
            cf.unique_id_bool(data_provider.medical_data.size),
            cf.diagnosis_sick,
        ]
        + extra_filters,
    )

    view_female = CDSView(
        source=data_provider.data_ds,
        filters=[
            cf.females,
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
    hover = HoverTool(names=["circle_female", "circle_male"])
    p1 = figure(
        y_range=data_provider.medical_data["Ethnic or Racial Group"].unique(),
        tooltips=TOOLTIPS,
        tools=["save", hover],
        toolbar_location="left",
        plot_height=height,
        plot_width=width,
        name=name,
    )
    if len(title.split("\n")) > 1:
        p1.add_layout(
            Title(text=title.split("\n")[1], text_font_style="italic"), "above"
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
        name="circle_female",
        view=view_female,
        color=mycols[1],
        selection_line_color="black",
        selection_line_alpha=1,
        selection_line_width=0.7,
    )

    p1.circle(
        x="Age",
        y="Ethnic or Racial Group",
        fill_alpha=0.2,
        size=10,
        source=data_provider.data_ds,
        name="circle_male",
        legend_label="male",
        view=view_male,
        color=mycols[0],
        selection_line_color="black",
        selection_line_alpha=1,
        selection_line_width=0.7,
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
        selection_line_width=0.7,
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
        selection_line_width=0.7,
    )

    p1.add_tools(LassoSelectTool())
    p1.add_tools(WheelZoomTool())
    p1.add_tools(ZoomInTool())
    p1.add_tools(ResetTool())
    p1.add_tools(BoxZoomTool())
    p1.add_tools(TapTool())

    p1.legend.location = "top_left"
    p1.legend.orientation = "horizontal"
    p1.legend.click_policy = "hide"

    p1.add_layout(Title(text=title.split("\n")[0],), "above")
    return p1
