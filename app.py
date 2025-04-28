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


# Set up Flask with correct folders
app = Flask(__name__, 
            static_folder='./frontend/static', 
            template_folder='./frontend/templates')
CORS(app, resources={r"/*": {"origins": "*"}})



# Register blueprints
blueprints = [
    HomePage.blueprint,
    SettingsPage.blueprint,
    SwitchCommandScreen.blueprint,
    QuickCommandsPage.blueprint,
]
for blueprint in blueprints:
    app.register_blueprint(blueprint)



print(app.url_map)

config_helper = ConfigHelper()
connection_helper = ConnectionHelper()
if __name__ == '__main__':
    app.run(debug=True)