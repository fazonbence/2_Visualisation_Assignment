from bokeh.models import BooleanFilter, CDSView, ColumnDataSource, GroupFilter, CustomJSFilter




#Selects the training data
TrainingSet = GroupFilter(column_name="Dataset Name", group="training")
#Selects the test data
TrainingSet = GroupFilter(column_name="Dataset Name", group="test")

#Selects females/males
Females = GroupFilter(column_name="Sex", group="female")
Males = GroupFilter(column_name="Sex", group="male")

#Selects 1 row/patient
#Default param should be: "data_provider.medical_data.size"
UniqueIdBool =lambda length :  BooleanFilter([True if x%11==0 else False for x in range(0, length)])


#Selects the rows with the same diagnosis type as the param
DiagnosisType = lambda Type: GroupFilter(column_name="Diagnosis", group=Type);