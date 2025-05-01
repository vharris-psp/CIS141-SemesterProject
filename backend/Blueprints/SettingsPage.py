from flask import Blueprint, render_template, app
from backend.Blueprints.DefaultPage import DefaultPage
from backend.Blueprints.Widgets.Container import VerticalGroup
from backend.Blueprints.Widgets.CustomWidgets import CommandOutputWidget, ConfigCollapsible, DeviceSettingContainer
from backend.Blueprints.Widgets.Buttons import HeaderButton
from backend.api.helpers.ConfigHelper import ConfigHelper
class SettingsPageContent(VerticalGroup):
    _default_css_class = "settings-viewer"
    inner_html = "Settings Viewer"

    def __init__(self, id: str):
        self.children = SettingsPageContent.get_elements_from_config()         
        super().__init__(id=id)


    def get_elements_from_config():
        config_containers = []
        # Get all device configs from the ConfigHelper
        device_configs = ConfigHelper().get_all_device_configs()
        # Iterate through each type of device

        for device_type in device_configs:
            # Get all device configs for this type of device
            
            # Create the device config container for each device
            devices = {}      
            for device_name in device_configs[device_type]:
                config_container = DeviceSettingContainer(device=device_name, data=device_configs[device_type][device_name])
                devices[device_name] = config_container
            # Create a collapsible element for the device type
            config_containers.append(ConfigCollapsible(id=device_type, label_text=device_type, config_elements=devices))

                # Store the Config Elements (One Collapsible for each device type) in the children_elements list
        return config_containers
            # Return the list of collapsible elements

class SettingsPage(DefaultPage):
    
    header_buttons = []
    footer_buttons = [] 
    content = SettingsPageContent(id='settings_content')  # Placeholder for content
    
      # Placeholder for content
    label = "Settings Page"
      # Placeholder for content
    def __init__(self):
        self.app = app.current_app
        super().__init__(name='settings')
        @self.route('/settings')
        def settings():
            return render_template('settings.html', header_buttons=SettingsPage.header_buttons, footer_buttons=SettingsPage.footer_buttons, content=SettingsPage.content)
    blueprint = Blueprint('settings', __name__, template_folder='../../frontend/templates', static_folder='../../frontend/static')
    
    
    @blueprint.route('/label')
    def label(self):
        return self.label


    
