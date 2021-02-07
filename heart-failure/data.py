import os

import pandas as pd
from bokeh.models import ColumnDataSource


class HeartFailureProvider:
    def __init__(
        self,
        medical_data_path: str,
        imgs_folder: str = os.path.join("heart-failure", "static", "tiles_flat"),
    ) -> None:
        """Container of shared data sources.

        Parameters
        ----------
        medical_data_path : str
            Path of the data CSV file
        imgs_folder : str, optional
            Folder where the tiles are stored, by default 
            "heart-failure/static/tiles_flat"
        """

        self.medical_data = pd.read_csv(medical_data_path)
        self.filenames = self.medical_data["filename"].tolist()
        self.patient_ids = self.medical_data["Patient Id"].tolist()
        self.tile_ids = [f.split("_")[3] for f in self.filenames]

        img_fmt = '<img src="{}/{}" ' 'alt="div_image" width="400" height="400">'

        img_info = [
            f"<b>Patient ID</b>: {row['Patient Id']}, <b>Tile ID</b>: {row['filename'].split('_')[3]}"
            f"</br></br><b>Diagnosis</b>: {row['Diagnosis']}</br></br><b>Disease Subtype</b>: {row['Disease Subtype']}"
            f"</br></br><b>Sex</b>: {row['Sex']}</br></br><b>Ethnic or Racial Group</b>: {row['Ethnic or Racial Group']}"
            for _, row in self.medical_data.iterrows()
        ]
        self.medical_data["img_html"] = [
            img_fmt.format(imgs_folder, x) for x in self.filenames
        ]
        self.medical_data["img_info"] = img_info
        self.counts_chronic = (
            pd.DataFrame(
                self.medical_data[
                    self.medical_data["Diagnosis"] == "chronic heart failure"
                ]
                .groupby(["Ethnic or Racial Group", "Sex"])
                .count()
            )["filename"].unstack()
            / 11
        )
        self.counts_not_chronic = (
            pd.DataFrame(
                self.medical_data[
                    self.medical_data["Diagnosis"] == "not chronic heart failure"
                ]
                .groupby(["Ethnic or Racial Group", "Sex"])
                .count()
            )["filename"].unstack()
            * -1
            / 11
        )

        self.counts_subtypes = (
            pd.DataFrame(
                self.medical_data.groupby(
                    ["Ethnic or Racial Group", "Disease Subtype"]
                ).count()
            )["filename"].unstack()
            / 11
        )

        self.data_ds = ColumnDataSource(self.medical_data)
        self.counts_chronic_ds = ColumnDataSource(self.counts_chronic)
        self.counts_not_chronic_ds = ColumnDataSource(self.counts_not_chronic)
        self.counts_subtypes_ds = ColumnDataSource(self.counts_subtypes)
        self.data_ds.selected.indices = []
