from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, CDSView, BooleanFilter
from bokeh.plotting import figure
from bokeh.models import (
    CategoricalColorMapper,
    ColumnDataSource,
    LassoSelectTool,
    WheelZoomTool,
    ZoomInTool,
    BoxZoomTool,
    ResetTool,
)
from bokeh.layouts import gridplot
import numpy as np
import pandas as pd
from bokeh.palettes import colorblind
from bokeh.plotting import Figure, figure
from data import HeartFailureProvider
import ourownfilters as oof
from bokeh.plotting import figure, output_file, show

def get_q1dot(data_provider: HeartFailureProvider):# -> Figure #for some reason it messes w the comments below

    
    TOOLTIPS = [
        ("index", "$index"),
        ("(x,y)", "($x, $y)"),
        ("filename", "@filename"),
    ]
    mycols = colorblind["Colorblind"][4]
    view_male = CDSView(source=data_provider.data_ds, filters=[oof.Females, oof.UniqueIdBool(data_provider.medical_data.size)])
    view_female = CDSView(source=data_provider.data_ds, filters=[oof.Males, oof.UniqueIdBool(data_provider.medical_data.size)])

    p1 = figure(title="Ethnic groups and time of infection ",
                y_range=data_provider.medical_data['Ethnic or Racial Group'].unique(),
                tooltips=TOOLTIPS,
                tools="save",
                toolbar_location="left"
                )
    print(data_provider.medical_data['Ethnic or Racial Group'].unique())
    p1.xaxis.axis_label = 'Age'
    p1.yaxis.axis_label = 'Ethnic group'

    #for gender in colormap.keys():
    #  genderFilteredDataFrame = plot_data[plot_data['Sex'] == gender]
    #   p1.circle(genderFilteredDataFrame['Age'], genderFilteredDataFrame['Ethnic or Racial Group'],
    #    color = colormap[gender], fill_alpha=0.2, legend_label=gender, size=10)

    p1.circle(x='Age', y='Ethnic or Racial Group',
              fill_alpha=0.2, size=10, source=data_provider.data_ds, legend_label="female", view=view_female, color=mycols[1])

    p1.circle(x='Age', y='Ethnic or Racial Group',
              fill_alpha=0.2, size=10, source=data_provider.data_ds, legend_label="male", view=view_male,color=mycols[0])
    
    p1.add_tools(LassoSelectTool())

    p1.legend.location = "top_right"
    p1.legend.click_policy = "hide"
    print("ASD")
    return p1




if __name__ == "__main__":
    # execute only if run as a script
    data_provider = HeartFailureProvider("medical_data_embedding.csv")

    q1_dotplot = get_q1dot(data_provider)
    output_file("lines.html")
    show(q1_dotplot)
