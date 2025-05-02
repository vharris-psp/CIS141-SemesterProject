from backend.Blueprints.Widgets.Widget import Widget
from backend.Blueprints.Widgets.Static import Label
## This File is to declare base HTML widgets to be used in place of the textual widgets
class Container(Widget):
    """Base class for all container widgets."""
    _default_css_class = "container"
    _description = "Base container widget"
    
    def __init__(self, id: str, children: list | None = None, label: Label | str | None = None):
        
        if isinstance(label, str):
            self.label = Label(label)
        elif isinstance(label, Label):
            self.label = label
        elif label is None:
            self.label = None
        self.before = self.label   
        self.id: str = id
        if hasattr(self, 'children') and children is None:
            self.children = self.children
        else:
            self.children = children if children is not None else []
        super().__init__(id=id)
    
    
class VerticalGroup(Container):
    
    css_class = "vertical-group"
    _description = "Vertical group container widget"
    def __init__(self, id: str):
        super().__init__(id=id)
    
    
class HorizontalGroup(Container):
    css_class = "horizontal-group"
    _description = "Horizontal group container widget"
    def __init__(self, id: str):  
        super().__init__ (id=id)
    

class Collapsible(Container):
    css_class = "collapsible"
    _description = "Collapsible container widget"
    def __init__(self, id: str, collapsed_symbol='>', expanded_symbol = 'V', label_text: Label | str | None = None):
        self.collapsed_symbol = collapsed_symbol
        self.expanded_symbol = expanded_symbol
        super().__init__(id=id, label=label_text)
        
        
        
    
