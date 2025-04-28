from backend.Blueprints.Widgets.Widget import Widget

class Button(Widget): 
    def __init__(self, label, id, **kwargs):
        self.label = label
        self.id = id
        self.onclick = kwargs.get('onclick', None)
        self.classes = kwargs.get('classes', None)
        self.html = self.generate_html()

    def generate_html(self):
        return '<button class="{}" id="{}">{}</button>'.format(
            self.classes or '', self.id, self.label
        )
        
class HeaderButton(Button):
    def __init__(self, label, id, **kwargs):
        kwargs['classes'] = 'header-button'
        super().__init__(label=label, id=id, **kwargs)
        
class FooterButton(Button):
    def __init__(self, label, id, **kwargs):
        kwargs['classes'] = 'footer-button'
        super().__init__(label=label, id=id, **kwargs)