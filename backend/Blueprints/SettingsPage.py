from flask import Blueprint, jsonify, render_template, app
from backend.Blueprints.DefaultPage import DefaultPage
from backend.Blueprints.Widgets.Container import VerticalGroup
from backend.Blueprints.Widgets.CustomWidgets import CommandOutputWidget, ConfigCollapsible, DeviceSettingContainer
from backend.Blueprints.Widgets.Buttons import HeaderButton
from backend.api.helpers.ConfigHelper import ConfigHelper
class SettingsPageContent(VerticalGroup):
    _default_css_class = "settings-viewer"
    inner_html = "Settings Viewer"

    def __init__(self, id: str):
        self.device_config_collapsible = ConfigCollapsible(id='device_config', label_text='Device Config')
        self.children = [self.device_config_collapsible]
        super().__init__(id=id)



class SettingsPage(DefaultPage):
    
    header_buttons = []
    footer_buttons = [] 
    
    
      # Placeholder for content
    label = "Settings Page"
      # Placeholder for content
    def __init__(self):
        self.app = app.current_app
        self.content = SettingsPageContent(id='settings_viewer')
        super().__init__(name='settings')
        
        @self.route('/settings')
        def settings():
            return render_template('settings.html', header_buttons=SettingsPage.header_buttons, footer_buttons=SettingsPage.footer_buttons, content=self.content)
        @self.route('/settings/get_device_info', methods=['GET'])
        def get_device_configs():
            try:
                device_configs = ConfigHelper().get_all_device_configs()
                if not device_configs:
                    raise ValueError("No device configurations found.")

                device_containers = [
                    DeviceSettingContainer(
                    device_id=device_id, 
                    device_name=device_data.get('host', 'Unknown Device')
                    ).rendered_html()
                    for device_id, device_data in device_configs.get('devices', {}).items()
                ]
                return jsonify({'html': ''.join(device_containers)})
            except Exception as e:
                app.logger.error(f"Error fetching device configs: {e}")
            return jsonify({'error': 'Failed to fetch device configurations'}), 500
            
        


    
