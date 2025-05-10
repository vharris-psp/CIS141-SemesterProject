
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
    
class PasswordInput(Input):
    """
    Password input widget for password input.
    """
    _description = "Password input widget"
    css_class = "password-input-widget"
    _html_tag = "input"
    def __init__(self,  value: str = "", placeholder: str = "", max_length: int = None, data: dict = None):
        self.other_attributes = data if data else {}
        self.other_attributes = {'value': value, 'placeholder': placeholder, 'maxlength': max_length} if max_length else {'value': value, 'placeholder': placeholder, 'type': 'password'}  
        super().__init__()
class Number(Input):
    """
    Number input widget for number input.
    """
    _description = "Number input widget"
    css_class = "number-input-widget"
    _html_tag = "input"
    def __init__(self,  value: str = "", placeholder: str = "", max_length: int = None, data: dict = None):
        self.other_attributes = data if data else {}
        self.other_attributes = {'value': value, 'placeholder': placeholder, 'maxlength': max_length} if max_length else {'value': value, 'placeholder': placeholder}  
        super().__init__()
class Email(Input):
    pass
    #TODO: Implement when needed
class Select(Input):
    """
    Select input widget for select input.
    """
    class SelectOption(Widget):
        """
        Select option widget for select input.
        """
        _description = "Select option widget"
        _html_tag = "option"
        css_class = "select-option-widget"
        def __init__(self, option: str):
            self.inner_html = option['value']
            self.other_attributes = {'data-value': option['value']}
            super().__init__()

        
        
    _description = "Select input widget"
    css_class = "select-input-widget"
    _html_tag = "select"
    def __init__(self,  value: str = "", placeholder: str = "", max_length: int = None, data: dict = None):
        self.other_attributes = data if data else {}
        self.other_attributes = {'value': value, 'placeholder': placeholder, 'maxlength': max_length} if max_length else {'value': value, 'placeholder': placeholder}
        if data.get('options'):
            self.children = [self.SelectOption(option) for option in data['options']]
        super().__init__()