from backend.Blueprints.Widgets.Widget import Widget


class Static(Widget):
    """A static widget that displays a label and a button."""
    _default_css_class = "static-widget"
    _description = "Static widget"
    _html_tag = "p"

    def __init__(self,text: str = "", ):
        self.inner_html = text
        super().__init__()





class Label(Static):
    """A static label widget."""
    css_class = "static-label"
    _description = "Static label widget"
    _html_tag = "label"
    def __init__(self, label_text: str, label_for: Widget = None, inside_widget: bool = True):
        self.inside_widget = inside_widget
        if label_for:
            self.other_attributes = {'for': label_for.id()} if label_for else {}
        super().__init__(text=label_text)

class WarningLabel(Label):
    """A static label widget for warnings."""
    css_class = "warning-label"
    _description = "Warning label widget"
    _html_tag = "label"
    def __init__(self, label_text: str, label_for: Widget = None, inside_widget: bool = True):
        self.inside_widget = inside_widget
        if label_for:
            self.other_attributes = {'for': label_for.id()} if label_for else {}
        super().__init__(label_text=label_text, label_for=label_for, inside_widget=inside_widget)

class AccordionLabel(Label):
    """A static label widget for accordion."""
    css_class = "accordion-label"
    _description = "Accordion label widget"
    _html_tag = "h3"
    def __init__(self, label_text: str, label_for: Widget = None, inside_widget: bool = True):
        self.inside_widget = inside_widget
        if label_for:
            self.other_attributes = {'for': label_for.id()} if label_for else {}
        super().__init__(label_text=label_text, label_for=label_for, inside_widget=inside_widget)