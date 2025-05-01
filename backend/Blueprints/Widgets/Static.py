from backend.Blueprints.Widgets.Widget import Widget


class Static(Widget):
    """A static widget that displays a label and a button."""
    _default_css_class = "static-widget"
    _description = "Static widget"
    _html_tag = "p"

    def __init__(self, id: str, text: str = "", ):
        self.inner_html = text
        super().__init__(id=id)





class Label(Static):
    """A static label widget."""
    css_class = "static-label"
    _description = "Static label widget"
    def __init__(self, id: str = None, label_text: str = ""):
    
        super().__init__(id=id, text=label_text)
    