from backend.Blueprints.Widgets.Widget import Widget


class Static(Widget):
    """A static widget that displays a label and a button."""
    _default_css_class = "static-widget"
    description = "Static widget"

    def __init__(self, id: str, name: str = "Static Widget", widget_type: str = "static", data: dict = None):
        super().__init__(id=id, name=name, description=self.description, widget_type=widget_type, data=data)




class Label(Static):
    """A static label widget."""
    _default_css_class = "static-label"
    
    def __init__(self, label: str, id: str = None):
        self.label = label
        if not id:
            id = label.replace(" ", "_").lower() + "_label"
        super().__init__(label, id)
    
    
        
    def generate_html(self):
        # Generate HTML for a label widget
        html = f'<label id="{self.id}" class="{self._default_css_class}">{self.label}</label>'
        return html