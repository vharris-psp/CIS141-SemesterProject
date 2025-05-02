from flask import Blueprint, render_template, send_from_directory
from backend.Blueprints.DefaultPage import DefaultPage

class HomePage(DefaultPage):
    """Home page class for the web application."""
    label = "Home Page"
    header_buttons = []
    footer_buttons = []
    content = None  # Placeholder for content

    # Removed now that Page inherits from blueprint
    #blueprint = Blueprint('home', __name__, template_folder='../../frontend/templates', static_folder='../../frontend/static')
    def __init__(self):
        self.name = 'home'
        super().__init__(name=self.name)
        @self.route('/')
        def index():
            return render_template('index.html', header_buttons=HomePage.header_buttons, footer_buttons=HomePage.footer_buttons, content=HomePage.content)

        @self.route('/home')
        def home():
            return render_template('index.html', header_buttons=HomePage.header_buttons, footer_buttons=HomePage.footer_buttons, content=HomePage.content)


def serve_static(path):
    """Serve static files from the frontend static folder."""
    return send_from_directory(HomePage.blueprint.static_folder, path)


