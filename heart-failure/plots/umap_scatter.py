from typing import Tuple

from bokeh.models import (
    BoxZoomTool,
    CDSView,
    CustomJS,
    Div,
    LassoSelectTool,
    ResetTool,
    TapTool,
    WheelZoomTool,
    ZoomInTool,
)
from bokeh.palettes import colorblind
from bokeh.plotting import Figure, figure

import custom_filters as cf
from data import HeartFailureProvider


def get_initial_img(data_provider: HeartFailureProvider) -> Div:
    """Return initial Div with the first tile of the first patient.

    Parameters
    ----------
    data_provider : HeartFailureProvider
        Application data provider

    Returns
    -------
    Div
        Div with image corresponding to the selected point on the scatter plot
    """
    return Div(
        text=data_provider.data_ds.data["img_html"][0],
        width=400,
        height=400,
        name="img_div",
    )


def get_initial_img_info(data_provider: HeartFailureProvider) -> Div:
    """Return initial Div with the first patient's info.

    Parameters
    ----------
    data_provider : HeartFailureProvider
        Application data provider

    Returns
    -------
    Div
        Div with patient's info corresponding to the selected point on the scatter plot
    """
    return Div(
        text=data_provider.data_ds.data["img_info"][0],
        width=300,
        height=60,
        name="img_info_div",
    )


def get_umap(data_provider: HeartFailureProvider) -> Tuple[Figure, Div, Div]:
    """Return scatter plot with UMAP projection, and two Div for image and patient info

    Parameters
    ----------
    data_provider : HeartFailureProvider
        Application data provider

    Returns
    -------
    Figure
        Scatter plot with UMAP projection
    Div
        Div with image corresponding to the selected point on the scatter plot
    Div
        Div with patient's info corresponding to the selected point on the scatter plot
    """

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
            filters=[cf.training_set, cf.diagnosis_type(label)],
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
            selection_line_color="black",
            selection_line_alpha=1,
            selection_line_width=0.7,
        )

        view_test = CDSView(
            source=data_provider.data_ds,
            filters=[cf.test_set, cf.diagnosis_type(label)],
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
            selection_line_color="black",
            selection_line_alpha=1,
            selection_line_width=0.7,
        )

    umap_scatter.add_tools(LassoSelectTool())
    umap_scatter.add_tools(WheelZoomTool())
    umap_scatter.add_tools(ZoomInTool())
    umap_scatter.add_tools(ResetTool())
    umap_scatter.add_tools(BoxZoomTool())
    umap_scatter.add_tools(TapTool())

    umap_scatter.legend.location = "top_left"
    umap_scatter.legend.click_policy = "hide"

    img = get_initial_img(data_provider)
    img_info = get_initial_img_info(data_provider)

    # show tile on selection of a point
    data_provider.data_ds.selected.js_on_change(
        "indices",
        CustomJS(
            args=dict(datasource=data_provider.data_ds, img=img, img_info=img_info),
            code="""
                var inds = cb_obj.indices;
                if (inds.length > 0){
                    var d1 = datasource.data;
                    img.text = d1['img_html'][inds[0]];
                    img_info.text = d1['img_info'][inds[0]];
                }
                else {
                    img.text = '';
                    img_info.text = '';
                }
                img.change.emit();
                img_info.change.emit();
                """,
        ),
    )

    return umap_scatter, img, img_info
