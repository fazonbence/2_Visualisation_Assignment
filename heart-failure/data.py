import os

import pandas as pd
from bokeh.models import BooleanFilter, CDSView, ColumnDataSource
import custom_filters as cf


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

        self.data_ds = ColumnDataSource(self.medical_data) 

   