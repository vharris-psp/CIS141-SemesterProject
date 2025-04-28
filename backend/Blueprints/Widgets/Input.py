
from backend.Blueprints.Widgets.Widget import Widget


class Input(Widget):
    """
    Input widget for text input.
    """

    def __init__(self, id: str,  value: str = "", placeholder: str = "", max_length: int = None, name="Input", description: str = "Input widget", widget_type: str = "input", data: dict = None):
        
        self.type = "input"
        super().__init__(id=id)