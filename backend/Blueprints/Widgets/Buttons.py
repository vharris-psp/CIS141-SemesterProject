from backend.Blueprints.Widgets.Widget import Widget

class Button(Widget): 
    css_class = "button"
    _html_tag = "button"
    _description = "Base button widget"
    def __init__(self, text: str, data: dict = None):
        self.inner_html = text
        self.other_attributes = data
        super().__init__()
            
        

    
        
class HeaderButton(Button):
    css_class = "header-button"
    _description = "Header button widget"
    def __init__(self, text: str, data: dict = None):
        super().__init__(text=text, data=data)
        
class FooterButton(Button):
    css_class = "footer-button"
    _description = "Footer button widget"
    def __init__(self, text: str, data: dict = None):
        super().__init__(text=text, data=data)

class SaveConfigButton(Button):
    css_class = "edit-button" 
    _description = "Edit config button widget"
    def __init__(self, text: str, data: dict=None):
        super().__init__(text=text, data=data)