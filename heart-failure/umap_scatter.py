from bokeh.models import (
    BoxZoomTool,
    CDSView,
    GroupFilter,
    LassoSelectTool,
    ResetTool,
    WheelZoomTool,
    ZoomInTool,
)
from bokeh.palettes import colorblind
from bokeh.plotting import Figure, figure

from data import HeartFailureProvider


def get_umap(data_provider: HeartFailureProvider) -> Figure:
    TOOLTIPS = [
        ("index", "$index"),
        ("(x,y)", "($x, $y)"),
        ("filename", "@filename"),
    ]

    mycols = colorblind["Colorblind"][4]

    umap_scatter = figure(
        plot_width=600,
        plot_height=600,
        tooltips=TOOLTIPS,
        tools="save",
        toolbar_location="left",
        name="umap",
    )

    umap_scatter.title.align = "center"
    umap_scatter.title.text_color = "black"
    umap_scatter.title.text_font_size = "25px"

    size = 6

    labels = ["chronic heart failure", "not chronic heart failure"]

    for col, label in zip(mycols, labels):

        view_train = CDSView(
            source=data_provider.data_ds,
            filters=[
                GroupFilter(column_name="Dataset Name", group="training"),
                GroupFilter(column_name="Diagnosis", group=label),
            ],
        )

        umap_scatter.circle(
            x="x",
            y="y",
            size=size,
            source=data_provider.data_ds,
            view=view_train,
            color=col,
            alpha=0.8,
            legend_label=str(label) + " train",
        )

        view_test = CDSView(
            source=data_provider.data_ds,
            filters=[
                GroupFilter(column_name="Dataset Name", group="test"),
                GroupFilter(column_name="Diagnosis", group=label),
            ],
        )

        umap_scatter.triangle(
            x="x",
            y="y",
            size=size,
            source=data_provider.data_ds,
            view=view_test,
            color=col,
            alpha=0.8,
            legend_label=str(label) + " test",
        )

    umap_scatter.add_tools(LassoSelectTool())
    umap_scatter.add_tools(WheelZoomTool())
    umap_scatter.add_tools(ZoomInTool())
    umap_scatter.add_tools(ResetTool())
    umap_scatter.add_tools(BoxZoomTool())

    umap_scatter.legend.label_text_font_size = "20pt"
    umap_scatter.yaxis.major_label_text_font_size = "15pt"
    umap_scatter.xaxis.major_label_text_font_size = "15pt"
    umap_scatter.legend.location = "top_left"
    umap_scatter.legend.click_policy = "hide"

    return umap_scatter
