
from backend.Blueprints.Widgets.Widget import Widget


class Input(Widget):
    """
    Input widget for text input.
    """
    _description = "Input widget"
    css_class = "input-widget"
    def __init__(self, id: str,  value: str = "", placeholder: str = "", max_length: int = None, name="Input", description: str = "Input widget", widget_type: str = "input", data: dict = None):
        self.value = value
        self.placeholder = placeholder
        self.max_length = max_length
        self.type = "input"
        super().__init__(id=id)
    def generate_html(self):
        
        # Generate HTML for an input widget
        html = f'<input type="{self.type}" id="{self.id}" class="{self._default_css_class}"'
        if self.value:
            html += f' value="{self.value}"'
        if self.placeholder:
            html += f' placeholder="{self.placeholder}"'
        if self.max_length:
            html += f' maxlength="{self.max_length}"'
        html += '>'
        return html
        