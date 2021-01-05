from bokeh.io import show
from bokeh.models import CheckboxButtonGroup, CustomJS, CustomJSFilter


def get_control_panel(data_provider):

    filters = []

    LABELS = ["Male", "Female"]
    checkbox_button_group = CheckboxButtonGroup(
        labels=LABELS, active=[0, 1], name="control_panel"
    )

    sex_filter = CustomJSFilter(
        args=dict(checkbox=checkbox_button_group),
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

    filters.append(sex_filter)

    checkbox_button_group.js_on_click(
        CustomJS(
            args=dict(source=data_provider.data_ds),
            code="""
            console.log('checkbox_button_group: active=' + this.active, this.toString())
            source.change.emit()
            """,
        )
    )

    return checkbox_button_group, filters
