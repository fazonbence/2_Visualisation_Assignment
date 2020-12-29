import pandas as pd
from bokeh.models import BooleanFilter, CDSView, ColumnDataSource


class HeartFailureProvider:
    def __init__(self, medical_data_path: str) -> None:

        self.medical_data = pd.read_csv(medical_data_path)
        self.data_ds = ColumnDataSource(self.medical_data)
        # self.data_view = CDSView(filters=[], source=self.data_ds)
