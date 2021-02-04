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
from bokeh.models import ColumnDataSource
from bokeh.palettes import GnBu3, OrRd3
import pandas as pd
from bokeh.models import BooleanFilter, GroupFilter

import custom_filters as cf
from data import CDSView, HeartFailureProvider

def get_q2bar(data_provider: HeartFailureProvider, extra_filters) -> Figure:
    
    main_plot1 = create_bar_plot(
        data_provider,
        "Ethnic groups vs Chronic/Non-Chronic Heart Failure",
        "q2_plot",
        extra_filters=extra_filters,
    )

    return main_plot1

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

    df = pd.read_csv('medical_data_embedding.csv')
    #print(df)

    #list_Sex = df.Sex.unique()
    #print(list_Sex)


    #c_male = df.loc[df['list_Sex'].isin('male')]
    #print(c_male)
    
    AA_chronic_male = df[(df['Diagnosis']=='chronic heart failure') & (df['Ethnic or Racial Group']=='African American') & (df['Sex']=='male')].nunique()
    # print(AA_chronic_male)
    #AA_chronic_male = len(df.index)
    #print(AA_chronic_male)

    p2 = figure(
            title=title,
            y_range=data_provider.medical_data["Ethnic or Racial Group"].unique(),
            tooltips=TOOLTIPS,
            tools="save",
            toolbar_location="left",
            plot_height=height,
            plot_width=width,
            name=name,
    )
    p2.xaxis.axis_label = "Number of Patients with Chronic and Non-Chronic Disease type"
    p2.yaxis.axis_label = "Ethnic group"

    names = data_provider.medical_data.Sex.unique()
    #print(names)

   
    gender = ['male','female']

    p2.hbar_stack(gender,y='Ethnic or Racial Group',height=0.9,color=['red','green'],source=data_provider.data_ds,
            legend_label="Chronic Heart Failure")

    p2.hbar_stack(gender,y='Ethnic or Racial Group',height=0.9,color=['blue','black'],source=data_provider.data_ds,
            legend_label="Not Chronic Heart Failure")

    p2.y_range.range_padding = 0.1
    p2.ygrid.grid_line_color = None
    p2.legend.location = "top_left"
    p2.axis.minor_tick_line_color = None
    p2.outline_line_color = None

    return p2

if __name__ == "__main__":
    # execute only if run as a script
    data_provider = HeartFailureProvider("medical_data_embedding.csv")
    q2_barplot = get_q2bar(data_provider)
    output_file("bar_stacked_split.html")
    show(q2_barplot)
