import os

import pandas as pd
from bokeh.models import ColumnDataSource


class HeartFailureProvider:
    def __init__(
        self,
        medical_data_path: str,
        imgs_folder: str = os.path.join("heart-failure", "static", "tiles_flat"),
    ) -> None:

        self.medical_data = pd.read_csv(medical_data_path)
        self.filenames = self.medical_data["filename"].tolist()
        self.patient_ids = self.medical_data["Patient Id"].tolist()
        self.tile_ids = [f.split("_")[3] for f in self.filenames]

        img_fmt = '<img src="{}/{}" ' 'alt="div_image" width="300" height="300">'

        img_info = [
            f"Patient ID: {p_id}, Tile ID: {t_id}"
            for p_id, t_id in zip(self.patient_ids, self.tile_ids)
        ]
        self.medical_data["img_html"] = [
            img_fmt.format(imgs_folder, x) for x in self.filenames
        ]
        self.medical_data["img_info"] = img_info
        self.counts_chronic = pd.DataFrame(
            self.medical_data[self.medical_data["Diagnosis"] == "chronic heart failure"]
            .groupby(["Ethnic or Racial Group", "Sex"])
            .count()
        )["filename"].unstack()
        self.counts_not_chronic = (
            pd.DataFrame(
                self.medical_data[
                    self.medical_data["Diagnosis"] == "not chronic heart failure"
                ]
                .groupby(["Ethnic or Racial Group", "Sex"])
                .count()
            )["filename"].unstack()
            * -1
        )

        self.data_ds = ColumnDataSource(self.medical_data)
        self.counts_chronic_ds = ColumnDataSource(self.counts_chronic)
        self.counts_not_chronic_ds = ColumnDataSource(self.counts_not_chronic)
