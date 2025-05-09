
from backend.Blueprints.Widgets.Widget import Widget


class Input(Widget):
    """
    Input widget for text input.
    """
    _description = "Input widget"
    css_class = "input-widget"
    _html_tag = "input"
    def __init__(self,  value: str = "", placeholder: str = "", max_length: int = None, data: dict = None):
        self.other_attributes = data if data else {}
        self.other_attributes = {'value': value, 'placeholder': placeholder, 'maxlength': max_length} if max_length else {'value': value, 'placeholder': placeholder}
        
        
        super().__init__()
    
        