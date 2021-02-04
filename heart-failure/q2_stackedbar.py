import pandas as pd
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource
from bokeh.palettes import GnBu3, OrRd3
from bokeh.plotting import figure
from bokeh.core.enums import HatchPatternAbbreviation
from bokeh.palettes import Spectral11
from bokeh.palettes import colorblind

 
df = pd.read_csv('medical_data_embedding.csv')
    #print(df)

    #list_Sex = df.Sex.unique()
    #print(list_Sex)


    #c_male = df.loc[df['list_Sex'].isin('male')]
    #print(c_male)

list_eth = df['Ethnic or Racial Group'].unique()
#print (list_eth)

count_ch_m = [ ]
count_ch_f = [ ]
count_nch_m =[ ]
count_nch_f=[ ]
for group in list_eth:

    AA_chronic_male = df[(df['Diagnosis']=='chronic heart failure') & (df['Ethnic or Racial Group']==group) & (df['Sex']=='male')]
    AA_non_chronic_male = df[(df['Diagnosis']=='not chronic heart failure') & (df['Ethnic or Racial Group']==group) & (df['Sex']=='male')]
    AA_chronic_female = df[(df['Diagnosis']=='chronic heart failure') & (df['Ethnic or Racial Group']==group) & (df['Sex']=='female')]
    AA_non_chronic_female = df[(df['Diagnosis']=='not chronic heart failure') & (df['Ethnic or Racial Group']==group) & (df['Sex']=='female')]
    count_ch_m.append(len(AA_chronic_male.index))
    count_ch_f.append(len(AA_chronic_female.index))
    count_nch_m.append(-1*len(AA_non_chronic_male.index))
    count_nch_f.append(-1*len(AA_non_chronic_female.index))

#string_list = [f"'{count_ch_m}'" for count_ch_m in a.split(',')]
#separator = ','
#string_with_apostrophe = separator.join(string_list)
#print(string_with_apostrophe)

#print('chronic_male','"%s"' %count_ch_m)
#chronic_female, nonchronic_male, nonchrnic female=',f('"{count_ch_m}"'),count_ch_f,count_nch_m,count_nch_f)

mycols = colorblind["Colorblind"][8]

output_file("bar_stacked_split.html")

#pats = list(HatchPatternAbbreviation)
#print(pats)
Ethnicity = ['Unknown racial group','African American','Caucasian','Hispanic','Race not stated']
gender = ["male", "female"]

Chronic = {'Ethnicity' : Ethnicity,
           'male'   : count_ch_m,
           'female' : count_ch_f}

NonChronic = {'Ethnicity' : Ethnicity,
           'male'   : count_nch_m,
           'female' : count_nch_f}


p = figure(y_range=Ethnicity, plot_height=350, x_range=(-1000,1000), title="Chronic and Non-Chronic patients",
           toolbar_location=None)

p.hbar_stack(gender, y='Ethnicity', height=0.9,color=[mycols[0],mycols[4]],source=ColumnDataSource(Chronic),
             legend_label=["%s Chronic" % x for x in gender])

p.hbar_stack(gender, y='Ethnicity', height=0.9,color=[mycols[1],mycols[2]],source=ColumnDataSource(NonChronic),
                legend_label=["%s NonChronic" % x for x in gender])

p.y_range.range_padding = 0.1
p.ygrid.grid_line_color = None
p.legend.location = "top_left"
p.axis.minor_tick_line_color = None
p.outline_line_color = None

show(p)