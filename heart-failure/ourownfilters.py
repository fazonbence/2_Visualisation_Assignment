from bokeh.models import BooleanFilter, CDSView, ColumnDataSource, GroupFilter




#Selects the training data
TrainingSet = GroupFilter(column_name="Dataset Name", group="training")
#Selects the test data
TrainingSet = GroupFilter(column_name="Dataset Name", group="test")


#Selects the rows with the same diagnosis type as the param
DiagnosisType = lambda Type: GroupFilter(column_name="Diagnosis", group=Type);