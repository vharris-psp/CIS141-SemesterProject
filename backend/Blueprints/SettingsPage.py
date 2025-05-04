import time
from flask import Blueprint, Response, jsonify, render_template, app
from backend.Blueprints.DefaultPage import DefaultPage
from backend.Blueprints.Widgets.Container import VerticalGroup
from backend.Blueprints.Widgets.CustomWidgets import CommandOutputWidget, Accordion, ConfigContainer, DeviceSettingContainer
from backend.Blueprints.Widgets.Buttons import HeaderButton
from backend.api.helpers.ConfigHelper import ConfigHelper
class DeviceSettingsContent(VerticalGroup):
    """Settings page content class for the web application."""
    inner_html = "Settings Viewer"
    css_class = "settings-viewer"
    def __init__(self):
        super().__init__()



class SettingsPage(DefaultPage):
    
    header_buttons = []
    footer_buttons = [] 
    
    
      # Placeholder for content
    label = "Settings Page"
      # Placeholder for content
    def __init__(self):
        self.app = app.current_app
        self.content = DeviceSettingsContent()
        self.device_content = DeviceSettingsContent()
        super().__init__(name='settings')
        
        @self.route('/settings')
        def settings():

            return render_template('settings.html', header_buttons=SettingsPage.header_buttons, footer_buttons=SettingsPage.footer_buttons, content=self.content)
        @self.route('/settings/devices')
        def settings_devices():
            return render_template('settings.html', header_buttons=SettingsPage.header_buttons, footer_buttons=SettingsPage.footer_buttons, content=self.content)
        
        @self.route('/settings/get_device_list', methods=['GET'])
        def get_device_list():
            def generate():
                device_configs = ConfigHelper().get_all_device_configs()
                for device_type, devices in device_configs.items():
                    device_elements = {device: DeviceSettingContainer(device=device, data=device_configs[device_type][device]) for device in device_configs[device_type]}
                    chunk = Accordion(label_text=device_type, config_elements=device_elements)
                    yield chunk()
            try:
                return Response(generate(), mimetype='text/html')
        
        
                
            except Exception as e:
                app.current_app.logger.error(f"Error fetching device list: {e}")
                return jsonify({'error': 'Failed to fetch device list'}), 500
        
        
        
        
        
        @self.route('/settings/get_device_config/<device_id>', methods=['GET'])
        def get_device_config(device_id):
            try:
                
                app.current_app.logger.info(f"Fetching configuration for device ID: {device_id}")
                device_config = ConfigHelper().get_device_config(device_id)
                if not device_config:
                    raise ValueError(f"No configuration found for device ID: {device_id}")

                return jsonify({
                    'device_id': device_id,
                    'device_config': device_config
                })
            except Exception as e:
                app.logger.error(f"Error fetching device config for {device_id}: {e}")
            return jsonify({'error': f'Failed to fetch configuration for device ID: {device_id}'}), 500
        
        def render_devices_container():
            return render_template('widgets/devices_container.html')
        
        

    
