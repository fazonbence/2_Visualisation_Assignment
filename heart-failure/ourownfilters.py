from bokeh.models import BooleanFilter, CDSView, ColumnDataSource, GroupFilter





TrainingSet = GroupFilter(column_name="Dataset Name", group="training")
DiagnosisType = lambda T: GroupFilter(column_name="Diagnosis", group=T);