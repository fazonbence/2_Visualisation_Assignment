from functools import partial
from typing import List, Tuple

import pandas as pd
from bokeh.layouts import Row, column, row
from bokeh.models import CheckboxButtonGroup, CustomJS, Div
from bokeh.models.filters import Filter

from data import HeartFailureProvider


def _get_sex_checkbox(data_provider: HeartFailureProvider,) -> CheckboxButtonGroup:
    sex_checkbox = CheckboxButtonGroup(
        labels=["Male", "Female"], active=[0, 1], name="control_panel_sex"
    )

    sex_checkbox.js_on_click(
        CustomJS(
            args=dict(source=data_provider.data_ds),
            code="""
            console.log('checkbox_button_group SEX: active=' + this.active, this.toString())
            source.change.emit()
            """,
        )
    )
    return sex_checkbox


def _get_diagnosis_checkbox(
    data_provider: HeartFailureProvider,
) -> CheckboxButtonGroup:
    diagnosis_checkbox = CheckboxButtonGroup(
        labels=["Chronic heart failure", "Not chronic heart failure"],
        active=[0, 1],
        name="control_panel_diagnosis",
    )

    diagnosis_checkbox.js_on_click(
        CustomJS(
            args=dict(source=data_provider.data_ds),
            code="""
            console.log('checkbox_button_group DIAGNOSIS: active=' + this.active, this.toString())
            source.change.emit()
            """,
        )
    )

    return diagnosis_checkbox


def _get_ethnicity_checkbox(
    data_provider: HeartFailureProvider,
) -> CheckboxButtonGroup:
    ethnicity_checkbox = CheckboxButtonGroup(
        labels=[
            "African American",
            "Caucasian",
            "Hispanic",
            "Unknown racial group",
            "Race not stated",
        ],
        active=[0, 1, 2, 3, 4],
        name="control_panel_ethnic",
    )

    ethnicity_checkbox.js_on_click(
        CustomJS(
            args=dict(source=data_provider.data_ds),
            code="""
            console.log('checkbox_button_group ETH: active=' + this.active, this.toString())
            source.change.emit()
            """,
        )
    )

    return ethnicity_checkbox


def _ds_callback(data_provider, attr, old, new) -> None:

    if new == []:
        medical_data = data_provider.medical_data
    else:
        medical_data = data_provider.medical_data.iloc[new]

    counts_chronic = (
        pd.DataFrame(
            medical_data[medical_data["Diagnosis"] == "chronic heart failure"]
            .groupby(["Ethnic or Racial Group", "Sex"])
            .count()
        )["filename"].unstack()
        / 11
    )
    counts_not_chronic = (
        pd.DataFrame(
            medical_data[medical_data["Diagnosis"] == "not chronic heart failure"]
            .groupby(["Ethnic or Racial Group", "Sex"])
            .count()
        )["filename"].unstack()
        / -11
    )
    counts_subtypes = (
        pd.DataFrame(
            medical_data.groupby(["Ethnic or Racial Group", "Disease Subtype"]).count()
        )["filename"].unstack()
        / 11
    )

    data_provider.counts_chronic_ds.data = counts_chronic
    data_provider.counts_not_chronic_ds.data = counts_not_chronic
    data_provider.counts_subtypes_ds.data = counts_subtypes


def _update_selection_callback(
    sex_checkbox, diagnosis_checkbox, ethnicity_checkbox, data_provider, attr, old, new
) -> None:
    indices = []
    eth_d = {
        "African American": 0,
        "Caucasian": 1,
        "Hispanic": 2,
        "Unknown racial group": 3,
        "Race not stated": 4,
    }

    diag_d = {
        "chronic heart failure": 0,
        "not chronic heart failure": 1,
        "heart tissue pathology": -1,
    }
    sex_d = {"male": 0, "female": 1}

    for i, row in data_provider.medical_data.iterrows():
        current_eth = row["Ethnic or Racial Group"]
        current_sex = row["Sex"]
        current_diag = row["Diagnosis"]
        if (
            eth_d[current_eth] in ethnicity_checkbox.active
            and diag_d[current_diag] in diagnosis_checkbox.active
            and sex_d[current_sex] in sex_checkbox.active
        ):
            indices.append(i)

    data_provider.data_ds.selected.indices = indices


def get_control_panel(data_provider: HeartFailureProvider) -> Row:
    """Return layout of checkboxes to control data filtering.

    Parameters
    ----------
    data_provider : HeartFailureProvider
        Application data provider

    Returns
    -------
    Row
        Layout of checkboxes
    """

    sex_checkbox = _get_sex_checkbox(data_provider)
    diagnosis_checkbox = _get_diagnosis_checkbox(data_provider)
    ethnicity_checkbox = _get_ethnicity_checkbox(data_provider)

    checkbox_column = row(
        column(Div(text="Sex"), sex_checkbox),
        column(Div(text="Diagnosis"), diagnosis_checkbox),
        column(Div()),
        column(Div()),
        column(Div(text="Ethnic or Racial Group"), ethnicity_checkbox),
        name="control_panel",
    )

    data_provider.data_ds.selected.on_change(
        "indices", partial(_ds_callback, data_provider)
    )
    sex_checkbox.on_change(
        "active",
        partial(
            _update_selection_callback,
            sex_checkbox,
            diagnosis_checkbox,
            ethnicity_checkbox,
            data_provider,
        ),
    )
    diagnosis_checkbox.on_change(
        "active",
        partial(
            _update_selection_callback,
            sex_checkbox,
            diagnosis_checkbox,
            ethnicity_checkbox,
            data_provider,
        ),
    )
    ethnicity_checkbox.on_change(
        "active",
        partial(
            _update_selection_callback,
            sex_checkbox,
            diagnosis_checkbox,
            ethnicity_checkbox,
            data_provider,
        ),
    )

    return checkbox_column
