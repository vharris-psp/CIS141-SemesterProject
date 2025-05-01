from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS

from backend.Blueprints.HomePage import HomePage
from backend.Blueprints.SettingsPage import SettingsPage
from backend.Blueprints.SwitchCommandPage import SwitchCommandScreen
from backend.Blueprints.QuickCommandPage import QuickCommandsPage
from backend.api.config_loader import load_config, save_config


##### CODE PORTED FROM PREVIOUS PROJECT #####
from backend.api.helpers.ConfigHelper import ConfigHelper
from backend.api.helpers.ConnectionHelper import ConnectionHelper
import os
import importlib
import pkgutil
from backend.Blueprints import Widgets


# Set up Flask with correct folders
app = Flask(__name__, 
            static_folder='./frontend/static', 
            template_folder='./frontend/templates')
CORS(app, resources={r"/*": {"origins": "*"}})



# Register blueprints
blueprints = [
    HomePage(),
    SettingsPage(),
    SwitchCommandScreen(),
    QuickCommandsPage(),

]
for blueprint in blueprints:
    app.register_blueprint(blueprint)


print(app.url_map)
# This method verifies that widgets.css contains all the CSS classes defined in the widgets
# classes. It checks for the presence of the CSS class names in the CSS file.
def validate_widget_css():
    # Path to the widgets.css file
    css_file_path = './frontend/static/css/widgets.css'
    
    if not os.path.exists(css_file_path):
        print("Error: widgets.css file not found.")
        return False
    
    with open(css_file_path, 'r') as css_file:
        css_content = css_file.read()
    
    # List of widget class objects to validate
    widget_classes = []
    widgets_path = os.path.join(os.path.dirname(__file__), 'backend', 'Blueprints', 'Widgets')

    for _, module_name, _ in pkgutil.iter_modules([widgets_path]):
        module = importlib.import_module(f'backend.Blueprints.Widgets.{module_name}')
        print(f"Loaded module: {module_name}")
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, type):  # Check if the attribute is a class
                if hasattr(attr, '_default_css_class') or hasattr(attr, 'css_class'):
                    widget_classes.append([c for c in [attr._default_css_class, attr.css_class] if c is not None][0])
            
    missing_classes = [cls for cls in widget_classes if f'.{cls}' not in css_content]
    
    if missing_classes:
        print("\033[93mThe following widget classes are missing in widgets.css:\033[0m")
        for cls in missing_classes:
            print(f"\033[95m- {cls}\033[0m")
        return False
    
    
    print("All widget classes have corresponding CSS selectors.")
    return True


config_helper = ConfigHelper()
connection_helper = ConnectionHelper()

# Validate widget CSS before running the app
if validate_widget_css():
    if __name__ == '__main__':
        app.run(debug=True)
else:
    print("Application cannot start due to missing CSS selectors.")