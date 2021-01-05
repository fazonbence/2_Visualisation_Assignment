from typing import List, Tuple

from bokeh.layouts import column, row
from bokeh.models import CheckboxButtonGroup, CustomJS, CustomJSFilter, Div
from bokeh.models.filters import Filter

from data import HeartFailureProvider


def _get_sex_checkbox_and_filter(
    data_provider: HeartFailureProvider,
) -> Tuple[CheckboxButtonGroup, Filter]:
    sex_checkbox = CheckboxButtonGroup(
        labels=["Male", "Female"], active=[0, 1], name="control_panel_sex"
    )

    sex_filter = CustomJSFilter(
        args=dict(checkbox=sex_checkbox),
        code="""
            const indices = []
            var dict = {
                "male": 0,
                "female": 1
            }
            for (var i = 0; i < source.get_length(); i++) {
                var currentSex = source.data['Sex'][i]
                if (checkbox.active.includes(dict[currentSex])) {
                    indices.push(i)
                }
            }
            return indices
        """,
    )

    sex_checkbox.js_on_click(
        CustomJS(
            args=dict(source=data_provider.data_ds),
            code="""
            console.log('checkbox_button_group: active=' + this.active, this.toString())
            source.change.emit()
            """,
        )
    )

    return sex_checkbox, sex_filter


def _get_diagnosis_checkbox_and_filter(
    data_provider: HeartFailureProvider,
) -> Tuple[CheckboxButtonGroup, Filter]:
    diagnosis_checkbox = CheckboxButtonGroup(
        labels=["Chronic heart failure", "Not chronic heart failure"],
        active=[0, 1],
        name="control_panel_diagnosis",
    )

    diagnosis_filter = CustomJSFilter(
        args=dict(checkbox=diagnosis_checkbox),
        code="""
            const indices = []
            var dict = {
                "chronic heart failure": 0,
                "not chronic heart failure": 1
            }
            for (var i = 0; i < source.get_length(); i++) {
                var currentDiagnosis = source.data['Diagnosis'][i]
                if (checkbox.active.includes(dict[currentDiagnosis])) {
                    indices.push(i)
                }
            }
            return indices
        """,
    )

    diagnosis_checkbox.js_on_click(
        CustomJS(
            args=dict(source=data_provider.data_ds),
            code="""
            console.log('checkbox_button_group: active=' + this.active, this.toString())
            source.change.emit()
            """,
        )
    )

    return diagnosis_checkbox, diagnosis_filter


def _get_ethnicity_checkbox_and_filter(
    data_provider: HeartFailureProvider,
) -> Tuple[CheckboxButtonGroup, Filter]:
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

    ethnicity_filter = CustomJSFilter(
        args=dict(checkbox=ethnicity_checkbox),
        code="""
            const indices = []
            var dict = {
                "African American": 0,
                "Caucasian": 1,
                "Hispanic": 2,
                "Unknown racial group": 3,
                "Race not stated": 4,
            }
            for (var i = 0; i < source.get_length(); i++) {
                var currentEthnicity = source.data['Ethnic or Racial Group'][i]
                if (checkbox.active.includes(dict[currentEthnicity])) {
                    indices.push(i)
                }
            }
            return indices
        """,
    )

    ethnicity_checkbox.js_on_click(
        CustomJS(
            args=dict(source=data_provider.data_ds),
            code="""
            console.log('checkbox_button_group: active=' + this.active, this.toString())
            source.change.emit()
            """,
        )
    )

    return ethnicity_checkbox, ethnicity_filter


def get_control_panel(
    data_provider: HeartFailureProvider,
) -> Tuple[CheckboxButtonGroup, List[Filter]]:

    sex_checkbox, sex_filter = _get_sex_checkbox_and_filter(data_provider)
    diagnosis_checkbox, diagnosis_filter = _get_diagnosis_checkbox_and_filter(
        data_provider
    )
    ethnicity_checkbox, ethnicity_filter = _get_ethnicity_checkbox_and_filter(
        data_provider
    )

    checkbox_column = column(
        Div(text="Sex"),
        sex_checkbox,
        Div(text="Diagnosis"),
        diagnosis_checkbox,
        Div(text="Ethnic or Racial Group"),
        ethnicity_checkbox,
        name="control_panel",
    )

    filters = [sex_filter, diagnosis_filter, ethnicity_filter]

    return checkbox_column, filters
