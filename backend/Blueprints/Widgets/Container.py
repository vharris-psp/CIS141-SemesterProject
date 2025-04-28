from backend.Blueprints.Widgets.Widget import Widget
## This File is to declare base HTML widgets to be used in place of the textual widgets
class Container(Widget):
    """Base class for all container widgets."""
    _default_css_class = "container"
    def __init__(self, id: str, children: list, description: str = "Base container widget"):
        self.id: str = id
        self.children: list = children
        self.description: str = description
        super().__init__(name="Container", description=description, widget_type="container", data={})
        self.html = self.generate_html()
    def generate_html(self):
        # Generate HTML for a container widget
        html = f'<div id="{self.id}" class="{self._default_css_class}">'
        
        if self.children:
            for child in self.children:
                html += child.html
        html += '</div>'
        return html
    
class VerticalGroup(Container):
    _default_css_class = "vertical-group"
    def __init__(self, id: str, children: list | None = None):
        super().__init__(id=id, description="Vertical group container widget", children=children)
    def generate_html(self):
        raise NotImplementedError(f"VerticalGroup ({self.__class__.__name__}) does not have a custom HTML generation method. Use the default one.")
    
class HorizontalGroup(Container):
    _default_css_class = "horizontal-group"
    def __init__(self, id: str, children: list | None = None):
        super().__init__ (id=id, description="Horizontal group container widget", children=children)
    def generate_html(self):
        raise NotImplementedError("HorizontalGroup ({self.__class__.__name__}) does not have a custom HTML generation method. Use the default one.")

class Collapsible(Container):
    _default_css_class = "collapsible"
    def __init__(self, id: str, children: list, collapsed_symbol='>', expanded_symbol = 'V', header = ''):
        self.collapsed_symbol = collapsed_symbol
        self.expanded_symbol = expanded_symbol
        self.header = header
        super().__init__(id=id, description="Collapsible container widget", children=children)

    def generate_html(self):
        # Generate HTML for a collapsible container widget with an arrow dropdown
        html = f'''
        <div id="{self.id}" class="{self._default_css_class}">
            <button class="collapsible-button" onclick="$('#{self.id} .collapsible-content').toggle();">
            <span class="arrow">{self.header} - {self.collapsed_symbol} </span> <!-- Down arrow -->
            </button>
            <div class="collapsible-content" style="display: none;">
        '''
        if self.children:
            for child in self.children:
                html += child.html
        html += '''
            </div>
        </div>
        '''
        return html
        
        
    
