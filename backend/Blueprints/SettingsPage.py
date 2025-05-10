import time
from flask import Blueprint, Response, jsonify, render_template, app, request
from backend.Blueprints.DefaultPage import DefaultPage
from backend.Blueprints.Widgets import Input, Static
from backend.Blueprints.Widgets.Container import HorizontalGroup, VerticalGroup, Wrapper
from backend.Blueprints.Widgets.CustomWidgets import CommandOutputWidget, Accordion
from backend.Blueprints.Widgets.Buttons import HeaderButton, SaveConfigButton, Button
from backend.api.helpers.ConfigHelper import ConfigHelper




class SettingsPage(DefaultPage):
    
    header_buttons = []
    footer_buttons = [] 
    

    class ConfigInputContainer(Wrapper):
        css_class = "config-input-container"
        _html_tag = "div"
        def __init__(self, setting: str, field_dict: dict, current_value: str):
            ''' 
            'type' = 'text' | 'number' | 'select' | 'checkbox'
            'label' = 'Device Name'
            'placeholder' = 'Enter the device name'
            'required' = True | False
            'dynamic' = False | False
            '''
            input = None
            self.other_attributes = {'data-setting': setting}
            field_type = field_dict.get('type')
            match field_type:
                case 'text':
                    input = Input.Input(value=current_value, placeholder=field_dict.get('placeholder'), data={'data-setting': setting})
                case 'password':
                    input = Input.PasswordInput(value=current_value, placeholder=field_dict.get('placeholder'), data={'data-setting': setting})
                case 'number':
                    input = Input.Input(value=current_value, placeholder=field_dict.get('placeholder'), data={'data-setting': setting})
                case 'select':
                    options = field_dict.get('options', [])
                    input = Input.Select(value=current_value, placeholder=field_dict.get('placeholder'), data={'data-setting': setting, 'options': options})
                    
                case _:
                    input = Input.Input(value=current_value, placeholder='')
            self.children =[Static.Label(label_text=field_dict['label'], label_for=input), input, Static.WarningLabel(label_text='')]
            super().__init__()
            
    class ConfigContainer(VerticalGroup):
        css_class = "config-container"
        def __init__(self, data: dict):
            self.data = data   
            super().__init__()
    class DeviceSettingContainer(ConfigContainer):
        _description = "Device Setting Container"
        css_class = "container device-setting-container"    
        def __init__(self, device: str, fields: dict):
            self.device = device
            self.data = fields
            self.other_attributes = {'data-device': device}
            # This duplicates label and causes problems TODO: FIX THIS
            #self.label = Static.Label(label_text=f'Configuration for: {device}', label_for=self)
            #TODO: Make the current values work
            self.save_button =  SaveConfigButton(text='Save', data={'data-device': device})
            self.children = [SettingsPage.ConfigInputContainer(setting=setting, field_dict=value, current_value=fields[setting].get('value', '')) for setting, value in fields.items()]
            self.children.append(self.save_button)
            super().__init__(data=fields)
    class DeviceTypeContainer(Accordion):
        css_class = "device-type-container"
        def __init__(self, device_type: str, device_elements: dict):
            self.device_type = device_type
            self.device_elements = device_elements
            # This duplicates label and causes problems TODO: FIX THIS
            # self.label = Static.Label(label_text=device_type, label_for=self)
            super().__init__(label_text=f'Device Type: {device_type} ( {len(device_elements)} Devices)', config_elements=device_elements)

    class DeviceGroupContainer(Accordion):
        css_class = "device-group-container"
        def __init__(self, group: str, child_elements: dict | list):
            self.group = group
            if isinstance(child_elements, dict):
                self.device_elements = child_elements 
            if isinstance(child_elements, list):
                message = f"Warning: in {self.__class__.__name__} for {self.group} - Device elements must currently be a dictionary or list."
                self.log_warning(message)
                raise NotImplementedError(message)
            self.device_elements = child_elements
            
            
            super().__init__(label_text=f'Device Group: {group}', config_elements=child_elements)
    class DeviceSettingsContent(VerticalGroup):
        """Settings page content class for the web application."""
        inner_html = "Settings Viewer"
        css_class = "settings-viewer content"

        def __init__(self):
            super().__init__()

    

                

    
      # Placeholder for content
    label = "Settings Page"
      # Placeholder for content
    def __init__(self):
        self.content = SettingsPage.DeviceSettingsContent()
        self.device_content = SettingsPage.DeviceSettingsContent()
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
                ##  Load the devices in the following format: 
                # devices[device_group][device_type][device_id]
                sorted_devices = {}
                configuration_file = ConfigHelper().get_current_devices_config()
                device_list, device_groups, device_types = {}, {}, {}
                try: 
                    device_list = configuration_file.get('devices', {})
                    device_groups = configuration_file.get('device_groups', {})
                    device_types = configuration_file.get('device_types', {})
                    for group in device_groups:
                        sorted_devices[group] = {}
                        for device_type in device_types:
                            sorted_devices[group][device_type] = {}
                except KeyError as e:
                    self.log_warning(e)

                # Iterate through the devices and sort them into the correct group and type
                for devices, config in device_list.items(): 
                    try:  
                        device_group = config.get('groups', 'default')
                        device_type = config.get('device_types', 'default')
                        if device_group not in device_groups or device_type not in device_types:
                            raise KeyError(f"Device group '{device_group}' or type '{device_type}' not found in configuration.")
                        try: 
                            sorted_devices[device_group][device_type][devices] = config

                        except Exception as e:
                            self.log_warning(e)
                    except KeyError as e:
                        self.log_warning(e)
                    except Exception as e:
                        self.log_warning(e)
                # Iterate through the sorted devices and yeild the group containers and elements
                devices = {}
                device_type_containers = {}
                device_fields = {}
                for device_group, device_type in sorted_devices.items():
                    
                    device_type_containers = {}
                    try:
                        
                        # Iterate through the device types
                        for device_type, devices in device_type.items():
                            # Iterate through the devices / configs
                            for device, config in devices.items():
                                field_dict = ConfigHelper().get_device_fields(device)
                                devices[device] = SettingsPage.DeviceSettingContainer(device=device, fields=field_dict)
                                device_fields[device] = field_dict
                            #devices = {device: SettingsPage.DeviceSettingContainer(device=device, fields=device_fields) for device, config in devices.items()}
                        
                            device_type_containers[device_type] = SettingsPage.DeviceTypeContainer(device_type=device_type, device_elements=devices)    
                        
                            
                    except KeyError as e:
                        self.log_warning(e)
                    except Exception as e:
                        self.log_warning(e)
                
                    yield [SettingsPage.DeviceGroupContainer(group=device_group, child_elements=device_type_containers)(), device_fields]
                




                    
      
            return jsonify(list(generate()))
                        
                    # try:
                    #     group_element = SettingsPage.DeviceGroupContainer(group=group, child_elements=device_types)

                        
                                         
                    
                    
                    
                    
                    
                    #     for device_type, device_configs in device_types.items():
                    #         try:
                    #             device_type_elements = { 
                    #                 # Create a dictionary of device configuration elements for all devices
                    #                 device : SettingsPage.DeviceSettingContainer(device=device, data=config)
                    #                 for device, config in device_configs.items()
                    #             }
                    #             # Create a dictionary of type containers to store the devices in.
                    #             device_type_container = SettingsPage.DeviceTypeContainer(
                    #                 device_type=device_type, device_elements=device_type_elements
                    #             )
                    #             group_elements[device_type] = device_type_container
                    #         except Warning as e:
                    #             self.log_warning(f"Warning: {e} in {self.__class__.__name__} for type: '{group}'")
                    #     yield SettingsPage.DeviceGroupContainer(group=group, child_elements=group_elements)()
                    # except Warning as e:
                    #     self.log_warning(f"Warning: {e} in {self.__class__.__name__} for group: '{group}'")
                        # Handle the warning as needed
                    # Since device_types do not store any config items yet, we can just use the keys -- Using a dict for now so I can store information there later. 
                

                #for device_type, devices in device_configs.items():
                    


                    #device_elements = {device: SettingsPage.DeviceSettingsContent.SettingContainer(device=device, data=device_configs[device_type][device]) for device in device_configs[device_type]}
                    #chunk = Accordion(label_text=device_type, config_elements=device_elements)
                #    yield chunk()
                # try:
                    # return Response(generate(), mimetype='text/html')
        # 
        # 
                # 
                # except Exception as e:
                    # self.log_error(f"Error fetching device list: {e}")
                    # return jsonify({'error': 'Failed to fetch device list'}), 500

        
        
        
        
        @self.route('/settings/get_device_config/<device_id>', methods=['GET'])
        def get_device_config(device_id):
            try:
                
                self.log_info(f"Fetching configuration for device ID: {device_id}")
                device_config = ConfigHelper().get_device_config(device_id)
                if not device_config:
                    raise ValueError(f"No configuration found for device ID: {device_id}")

                return jsonify({
                    'device_id': device_id,
                    'device_config': device_config
                })
            except Exception as e:
                app.current_app.logger.error(f"Error fetching device config for {device_id}: {e}")
            return jsonify({'error': f'Failed to fetch configuration for device ID: {device_id}'}), 500
        
        def render_devices_container():
            return render_template('widgets/devices_container.html')
        
        @self.route('/settings/save_device_config/<device_id>', methods=['PUT'])
        def save_device_config(device_id):
            try:
                
                if not request.is_json:
                    raise ValueError("Request must be JSON")
                new_config = request.json
                
                if not new_config:
                    raise ValueError("Configuration data or changes not provided")
                
                successful_changes, failed_changes = ConfigHelper().save_device_config(device_id, new_config)
                return jsonify({
                    'device_id': device_id,
                    'successful_changes': successful_changes,
                    'failed_changes': failed_changes
                })
                
                    
                        
                        
                
            except Exception as e:
                app.current_app.logger.error(f"Error saving device config for {device_id}: {e}")
            return jsonify({'error': f'Failed to save configuration for device ID: {device_id}'}), 500
            
            
            
            
            
            
            
            
            
            
            

    
