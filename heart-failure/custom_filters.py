from bokeh.models import BooleanFilter, GroupFilter

# Selects the training data
training_set = GroupFilter(column_name="Dataset Name", group="training")

# Selects the test data
test_set = GroupFilter(column_name="Dataset Name", group="test")

# Selects females/males
females = GroupFilter(column_name="Sex", group="female")
males = GroupFilter(column_name="Sex", group="male")
gender = GroupFilter(column_name="Sex")
not_null_gender = lambda data:   BooleanFilter(
    [True if x["Sex"] =="male" or x["Sex"]=="female"  else False for i,x in data.iterrows()]
)


# Selects African American/Hispanic/Caucasian/Unknown Racial group ("Race not stated" has been excluded)
AA = GroupFilter(column_name="Ethnic or Racial Group", group="African American")
Hisp = GroupFilter(column_name="Ethnic or Racial Group", group="Hispanic")
Caucasians = GroupFilter(column_name="Ethnic or Racial Group", group="Caucasian")
Unknown = GroupFilter(column_name="Ethnic or Racial Group", group="Unknown Racial Group")

# Selects 1 row/patient
# Default param should be: "data_provider.medical_data.size"
unique_id_bool = lambda length: BooleanFilter(
    [True if x % 11 == 0 else False for x in range(0, length)]
)

# Selects the remaining 10 row/patient
# For linking purposes only!
# Default param should be: "data_provider.medical_data.size"
inverse_unique_id_bool = lambda length: BooleanFilter(
    [False if x % 11 == 0 else True for x in range(0, length)]
)


# Selects the rows with the same diagnosis type as the param
diagnosis_type = lambda type_: GroupFilter(column_name="Diagnosis", group=type_)

diagnosis_sick = GroupFilter(column_name="Diagnosis", group="chronic heart failure")

diagnosis_notsick = GroupFilter(column_name="Diagnosis", group="not chronic heart failure")



# Selects the correct Disease Subtype
disease_subtype_cardiomyopathy = GroupFilter(
    column_name="Disease Subtype", group="cardiomyopathy"
)
disease_subtype_ischemiccardiomyopathy = GroupFilter(
    column_name="Disease Subtype", group="ischemic cardiomyopathy"
)
disease_subtype_myocardiumdisease = GroupFilter(
    column_name="Disease Subtype", group="myocardium disease"
)
