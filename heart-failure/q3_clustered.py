from bokeh.models import ColumnDataSource
from bokeh.plotting import Figure, figure
from bokeh.transform import dodge

from data import HeartFailureProvider


def get_q3_clustered(data_provider: HeartFailureProvider) -> Figure:
    df = data_provider.medical_data
    list_eth = df["Ethnic or Racial Group"].unique()
    count_type1 = []
    count_type2 = []
    count_type3 = []

    for group in list_eth:
        sub_type1 = df[
            (df["Disease Subtype"] == "cardiomyopathy")
            & (df["Ethnic or Racial Group"] == group)
        ]
        sub_type2 = df[
            (df["Disease Subtype"] == "ischemic cardiomyopathy")
            & (df["Ethnic or Racial Group"] == group)
        ]
        sub_type3 = df[
            (df["Disease Subtype"] == "myocardium disease")
            & (df["Ethnic or Racial Group"] == group)
        ]
        count_type1.append(len(sub_type1.index))
        count_type2.append(len(sub_type2.index))
        count_type3.append(len(sub_type3.index))

    Ethnicity = list_eth
    Subtype = ["cardiomyopathy", "ischemic cardiomyopathy", "myocardium disease"]
    data = {
        "Ethnicity": Ethnicity,
        "cardiomyopathy": count_type1,
        "ischemic cardiomyopathy": count_type2,
        "myocardium disease": count_type3,
    }
    source = ColumnDataSource(data=data)

    p = figure(
        x_range=Ethnicity,
        y_range=(0, 400),
        plot_height=500,
        title="Disease Sub-type based on Ethnic Groups",
        toolbar_location=None,
        name="q3_clustered",
    )

    p.vbar(
        x=dodge("Ethnicity", -0.25, range=p.x_range),
        top="cardiomyopathy",
        width=0.2,
        source=source,
        color="#c9d9d3",
        legend_label="cardiomyopathy",
    )
    p.vbar(
        x=dodge("Ethnicity", 0.0, range=p.x_range),
        top="ischemic cardiomyopathy",
        width=0.2,
        source=source,
        color="#718dbf",
        legend_label="ischemic cardiomyopathy",
    )
    p.vbar(
        x=dodge("Ethnicity", 0.25, range=p.x_range),
        top="myocardium disease",
        width=0.2,
        source=source,
        color="#e84d60",
        legend_label="myocardium disease",
    )

    p.xaxis.axis_label = "Ethnic group"

    p.yaxis.axis_label = "Number of Patients"
    p.x_range.range_padding = 0.1
    p.xgrid.grid_line_color = None
    p.legend.location = "top_left"
    p.legend.orientation = "horizontal"

    return p
