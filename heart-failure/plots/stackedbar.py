from bokeh.palettes import colorblind
from bokeh.plotting import Figure, figure

from data import HeartFailureProvider


def get_bar(data_provider: HeartFailureProvider) -> Figure:
    """Return stacked bar plot of ethnic groups and Chronic/Non-Chronic Heart Failure

    Parameters
    ----------
    data_provider : HeartFailureProvider
        Application data provider

    Returns
    -------
    Figure
        Stacked bar plot
    """

    list_eth = data_provider.medical_data["Ethnic or Racial Group"].unique()

    mycols = colorblind["Colorblind"][5]

    gender = ["male", "female"]

    p = figure(
        y_range=list_eth,
        plot_height=250,
        title="Ethnic groups vs Chronic/Non-Chronic Heart Failure",
        toolbar_location="left",
        name="stacked",
    )

    p.hbar_stack(
        gender,
        y="Ethnic or Racial Group",
        height=0.6,
        color=[mycols[0], mycols[4]],
        source=data_provider.counts_chronic_ds,
        legend_label=["%s - chronic heart failure" % x for x in gender],
    )

    p.hbar_stack(
        gender,
        y="Ethnic or Racial Group",
        height=0.6,
        color=[mycols[1], mycols[2]],
        source=data_provider.counts_not_chronic_ds,
        legend_label=["%s - not chronic heart failure" % x for x in gender],
    )

    p.y_range.range_padding = 0.1
    p.xaxis.axis_label = "Number of Patients"
    p.ygrid.grid_line_color = None
    p.legend.location = "top_right"
    p.axis.minor_tick_line_color = None
    p.outline_line_color = None
    p.legend.click_policy = "hide"

    return p
