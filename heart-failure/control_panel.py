from bokeh.io import show
from bokeh.models import CheckboxButtonGroup, CustomJS, CustomJSFilter


def _get_sex_checkbox_and_filter(data_provider):
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


def get_control_panel(data_provider):

    filters = []

    sex_checkbox, sex_filter = _get_sex_checkbox_and_filter(data_provider)

    filters.append(sex_filter)

    return sex_checkbox, filters
