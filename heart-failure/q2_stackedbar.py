from bokeh.io import show
from bokeh.palettes import colorblind
from bokeh.plotting import Figure, figure

from data import HeartFailureProvider


def get_q2bar(data_provider: HeartFailureProvider) -> Figure:

    list_eth = data_provider.medical_data["Ethnic or Racial Group"].unique()

    mycols = colorblind["Colorblind"][8]

    gender = ["male", "female"]

    p = figure(
        y_range=list_eth,
        plot_height=250,
        title="Ethnic groups vs Chronic/Non-Chronic Heart Failure",
        toolbar_location=None,
        name="q2_plot",
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
    p.ygrid.grid_line_color = None
    p.legend.location = "top_right"
    p.axis.minor_tick_line_color = None
    p.outline_line_color = None

    return p


if __name__ == "__main__":
    # execute only if run as a script
    data_provider = HeartFailureProvider("medical_data_embedding.csv")
    q2_stackedbar = get_q2bar(data_provider, [])
    show(q2_stackedbar)
