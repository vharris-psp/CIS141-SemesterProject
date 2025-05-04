from backend.Blueprints.Widgets.Widget import Widget
from backend.Blueprints.Widgets.Static import Label
## This File is to declare base HTML widgets to be used in place of the textual widgets
class Container(Widget):
    """Base class for all container widgets."""
    _default_css_class = "container"
    _description = "Base container widget"
    
    def __init__(self, children: list | None = None, label: Label | str | None = None):
        # This must be called first so the id can be used in the label
        

        if isinstance(label, str):
            self.label = Label(label_text=label, label_for=self)
        elif isinstance(label, Label):
            self.label = label
        elif label is None:
            self.label = None
        self.before = self.label   
        
        if hasattr(self, 'children') and children is None:
            self.children = self.children
        else:
            self.children = children if children is not None else []
        super().__init__()
    
    
class VerticalGroup(Container):
    
    css_class = "vertical-group"
    _description = "Vertical group container widget"
    def __init__(self):
        super().__init__()
    
    
class HorizontalGroup(Container):
    css_class = "horizontal-group"
    _description = "Horizontal group container widget"
    def __init__(self):  
        super().__init__()
    

class Collapsible(Container):
    css_class = "accordion"
    _description = "Collapsible container widget"
    def __init__(self, collapsed_symbol='>', expanded_symbol = 'V', label_text: Label | str | None = None):
        self.inner_html = f"<h3>{label_text}</h3>"
        self.collapsed_symbol = collapsed_symbol
        self.expanded_symbol = expanded_symbol
        super().__init__()
class Wrapper(Container):
    css_class = "wrapper"
    _description = "Wrapper container widget"
    def __init__(self, children: list | None = None, label: Label | str | None = None, classes: str | None = None):
        self.css_class = classes if classes is not None else self.css_class 
        self.children = children if children is not None else []
        super().__init__()
        
    
