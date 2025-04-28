class Widget:
    def __init__(self, name: str, description: str, widget_type: str, data: dict):
        self.name = name
        self.description = description
        self.widget_type = widget_type
        self.data = data
        self.html = self.generate_html()
    def generate_html(self):
        # This method should be overridden in subclasses to generate specific HTML
        raise NotImplementedError("Subclasses should implement this method.")
    