from backend.Blueprints.Widgets.Widget import Widget
## This File is to declare base HTML widgets to be used in place of the textual widgets
class VerticalGroup(Widget):
    def __init__(self, id: str, children: list):
        self.id = id
        self.children = children
        self.html = self.generate_html()
    
    def generate_html(self):
        # Generate HTML for a vertical group of widgets
        html = f'<div id="{self.id}" class="vertical-group">'
        for child in self.children:
            html += child.html
        html += '</div>'
        return html
class HorizontalGroup(Widget):
    def __init__(self, id: str, children: list):
        self.id = id
        self.children = children
        self.html = self.generate_html()
    
    def generate_html(self):
        # Generate HTML for a horizontal group of widgets
        html = f'<div id="{self.id}" class="horizontal-group">'
        for child in self.children:
            html += child.html
        html += '</div>'
        return html
