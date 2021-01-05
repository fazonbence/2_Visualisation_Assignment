import numpy as np
import pandas as pd
from bokeh.io import output_file, show
from bokeh.layouts import column, gridplot, row
from bokeh.models import (BooleanFilter, BoxZoomTool, CategoricalColorMapper,
                          CDSView, ColumnDataSource, LassoSelectTool,
                          ResetTool, WheelZoomTool, ZoomInTool)
from bokeh.palettes import colorblind
from bokeh.plotting import Figure, figure, output_file, show

import ourownfilters as oof
from data import HeartFailureProvider


def get_q1dot(data_provider: HeartFailureProvider):# -> Figure #for some reason it messes w the comments below   
    
    mainPlot=Create_DotPlot(data_provider,"Ethnic groups and time of infection", 'main')
    Plot1 = Create_DotPlot(data_provider,"Ethnic groups and time of infection\n with cardiomyopathy", 'plot1', 250,500,[oof.DiseaseSubtype_cardiomyopathy]) 
    Plot2 = Create_DotPlot(data_provider,"Ethnic groups and time of infection\n with ischemic cardiomyopathy", 'plot2',250,500,[oof.DiseaseSubtype_ischemiccardiomyopathy]) 
    #Plot3 = Create_DotPlot([oof.DiseaseSubtype_myocardiumdisease]) 

    return mainPlot, Plot1, Plot2


def Create_DotPlot(data_provider: HeartFailureProvider,title, name,height=500,width=600 ,extraFilters =[]):
    TOOLTIPS = [
        ("index", "$index"),
        ("(x,y)", "($x, $y)"),
        ("filename", "@filename"),
    ]
    mycols = colorblind["Colorblind"][4]
    view_male = CDSView(source=data_provider.data_ds, filters=[oof.Females, oof.UniqueIdBool(data_provider.medical_data.size), oof.Diagnosis_Sick]+extraFilters)
    view_female = CDSView(source=data_provider.data_ds, filters=[oof.Males, oof.UniqueIdBool(data_provider.medical_data.size), oof.Diagnosis_Sick]+extraFilters)
    view_remaining_male = CDSView(source=data_provider.data_ds, filters=[oof.Males,oof.Inverse_UniqueIdBool(data_provider.medical_data.size), oof.Diagnosis_Sick]+extraFilters)
    view_remaining_female = CDSView(source=data_provider.data_ds, filters=[oof.Females,oof.Inverse_UniqueIdBool(data_provider.medical_data.size), oof.Diagnosis_Sick]+extraFilters)

    p1 = figure(title=title,
                y_range=data_provider.medical_data['Ethnic or Racial Group'].unique(),
                tooltips=TOOLTIPS,
                tools="save",
                toolbar_location="left",
                plot_height=height,
                plot_width=width,
                name=name,
                )
    print(data_provider.medical_data['Ethnic or Racial Group'].unique())
    p1.xaxis.axis_label = 'Age'
    p1.yaxis.axis_label = 'Ethnic group'


    p1.circle(x='Age', y='Ethnic or Racial Group',
              fill_alpha=0.2, size=10, source=data_provider.data_ds, legend_label="female", view=view_female, color=mycols[1])

    p1.circle(x='Age', y='Ethnic or Racial Group',
              fill_alpha=0.2, size=10, source=data_provider.data_ds, legend_label="male", view=view_male,color=mycols[0])

    p1.circle(x='Age', y='Ethnic or Racial Group',
              fill_alpha=0.2, size=10, source=data_provider.data_ds, legend_label="female", view=view_remaining_female,color='rgba(0, 0, 0, 0)')
    p1.circle(x='Age', y='Ethnic or Racial Group',
              fill_alpha=0.2, size=10, source=data_provider.data_ds, legend_label="male", view=view_remaining_male,color='rgba(0, 0, 0, 0)')
    
    p1.add_tools(LassoSelectTool())

    p1.legend.location = "top_left"
    p1.legend.click_policy = "hide"
    return p1



if __name__ == "__main__":
    # execute only if run as a script
    data_provider = HeartFailureProvider("medical_data_embedding.csv")
    q1_dotplot = get_q1dot(data_provider)
    output_file("lines.html")
    show(q1_dotplot)
