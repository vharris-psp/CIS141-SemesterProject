
from backend.Blueprints.Widgets.Widget import Widget


class Input(Widget):
    """
    Input widget for text input.
    """
    _description = "Input widget"
    css_class = "input-widget"
    def __init__(self,  value: str = "", placeholder: str = "", max_length: int = None, name="Input", description: str = "Input widget", widget_type: str = "input", data: dict = None):
        self.value = value
        self.placeholder = placeholder
        self.max_length = max_length
        self.type = "input"
        super().__init__()
    
        