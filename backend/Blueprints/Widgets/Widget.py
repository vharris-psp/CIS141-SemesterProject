class Widget:
    _default_css_class = "widget"
    def __init__(self, id, name: str, description: str, widget_type: str, data: dict = None):
        self.name = name
        self.id = id
        self.description = description
        self.widget_type = widget_type
        self.data = data
        self.html: str = None # Placeholder for HTML representation
        # Generate HTML should always be called after initializing the widget
        self.generate_html()

    def generate_html(self):
        # This method should be overridden in subclasses to generate specific HTML
        raise NotImplementedError("Subclasses should implement this method.")
    