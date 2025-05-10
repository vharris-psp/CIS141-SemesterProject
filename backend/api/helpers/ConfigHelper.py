
from enum import Enum
from json import dump, load, JSONDecodeError
from io import open
from os import stat
from typing import Any, Dict
from backend.api.helpers.Helper import Helper


__SUGGESTIONS__ = {}
class InvalidConfigException(Exception):
    def __init__(self, message):
        super().__init__(message)
class InvalidBackupConfigException(Exception):
    def __init__(self, message):
        super().__init__(message)
class ConfigHelper(Helper):
    class _default_file(Enum):
        ___CONF__ = 'backend/api/config/conf.json'
        __CONF_BACKUP__ = 'backend/api/config/conf.bk'
        __DEVICE_CONFIG__ = 'backend/api/config/deviceconf.json'
        # These files still need to be migrated / ported
        __MAC_SOURCE__ = 'scripts/SWITCHES/Data/ap_source.csv'
        __ERROR_LOG__ = 'scripts/Logs/ap_errors.txt'
        __UNNAMED__ = 'Output/unnamed.txt'
        __SN_SHEET__ = 'Data/source_sn.csv'
        __MASTER_CSV__ = 'Data/MASTER.csv'
        __MASTER_JSON__ = 'Data/MASTER.json'
        __PROPOSED_NAMES__ = 'Data/proposed.csv'
        __PROPOSED_REBOOTS__ = 'Data/proposed_reboots.csv'
        __CONFLICTS__ = 'Data/conflicts.csv'
        __CAPWAP_DATA__ = 'Data/capwap_data.csv'
        __CLIENT_SUMMARY__ = 'Data/client_summary.csv'
        __SCRIPTS_DIRECTORY__ = 'scripts'
        __MAIN_STYLESHEET__ = 'styles/styles.css'
        __INPUT_SUGGESTIONS__ = 'config/suggestions.json'
        __NETMIKO_SESSION_LOG__ = 'scripts/Logs/netmiko.log'

    def get_file(file: _default_file):
        return file
    _instance = None
    _device_config: Dict[str, Any] = {}
    def _config_is_valid(self):
        if not self._device_config:
            return False
        if not self._device_config.get('devices'):
            return False
        # TODO: This should check all possible default connection settings. Commented out because this is now specific to the default device type
        #if not self._device_config.get('default_connection_settings'):
        #    return False
        if not self._device_config.get('building_code_map'):
            return False
        return True
    
    def __init__(self):
        self.load_config_file()
        self.devices = self._device_config.get('devices')
        self.connection_defaults = self._device_config.get('device_types').get('default').get('default_connection_settings')
        super().__init__()
            
    def __del__(self):
        self.write_config()
        self.write_suggestions()
        print(f"Deleting instance of {self.__class__.__name__}")
    
    @classmethod 
    def load_backup_config(cls):
        """Restore the config from the backup file"""
        try:
            with open(cls._default_file.__CONF_BACKUP__, 'r') as backup_file:
                cls._device_config = load(backup_file) 
        except FileNotFoundError:
            raise FileNotFoundError("Backup config file not found.")
        except JSONDecodeError as e:
            raise InvalidBackupConfigException(f"Backup config file is not valid JSON: {e}")
        
    @classmethod
    def load_config_file(cls, file: _default_file = _default_file.__DEVICE_CONFIG__):
        """Load config from the given file or fallback to the backup"""
        try:
            with open(file, 'r') as config_file:
                cls._device_config = load(config_file)
                if not cls._config_is_valid(cls):
                    raise InvalidConfigException("Config file is invalid.")    
        except (InvalidConfigException, FileNotFoundError, JSONDecodeError) as e:
            try:
                cls.load_backup_config()
            except InvalidBackupConfigException:
                raise InvalidBackupConfigException(f"Backup config file is invalid. {e}")
        except Exception as e:
            raise e
    def write_config(self, file: _default_file = _default_file.__DEVICE_CONFIG__):
        with open(file, 'w') as config_file:
            dump(self._device_config, config_file, indent=4)  # Writing as pretty JSON
        
            
    def get_config(self) -> dict:
        return self._device_config
    
    def _load_suggestions(self):
        try: 
            with open(self._default_file.__INPUT_SUGGESTIONS__, 'r') as file:
                if len(file.readlines()) > 1: 
                    return load(file)
        except FileNotFoundError as e: 
            return {}
    def get_suggestions(self, type: str):
        global __SUGGESTIONS__
        if __SUGGESTIONS__ and type not in __SUGGESTIONS__:
            __SUGGESTIONS__[type] = []
            return __SUGGESTIONS__[type]
        else:
            return {}
        
        

    def write_suggestions(self):
        global __SUGGESTIONS__
        suggestion_data = __SUGGESTIONS__
        with open(self._default_file.__INPUT_SUGGESTIONS__, 'w') as file:
            dump(suggestion_data, file, indent=4)    
    def update_selected_switches(self, selected_switches: dict): 
        for switch in self._device_config['switch_info']:
            print(switch)
    
    
    def get_all_device_configs(self) -> dict:
        def merge_connection_settings(device, device_type, config):
            connection_settings = {}
            for setting in self.connection_defaults:
                if setting in config:
                    connection_settings[setting] = config[setting]
                else:
                    connection_settings[setting] = self.connection_defaults[setting]
            return connection_settings
        device_map = self._device_config['devices']
        for device_type in device_map:
            for device in device_map[device_type]:
                device_map[device_type][device]['connection_settings'] = merge_connection_settings(device=device, device_type=device_type, config=device_map[device_type][device])
        return device_map
    
    def get_all_devices(self, filter=None) -> dict:
        devices = None
        try:
            if not filter:
                devices = self._device_config['devices']
    
            else:
                devices =  self._device_config['devices'][filter]

            return devices
        except KeyError as e: 
            self.notify(f'Device Config Error: {filter} type found')

    def wlc_list(self) -> dict:
        try:
            wlcs = self._device_config['wlc_info']
            return wlcs
        except KeyError as e:
            self.app.notify(f"Config Key Error: {e}")
    def get_wlc_connection_settings(self, wlc: str | None = None) -> dict:
        return self._device_config['wlc_info']
    def set_selected_switches(self, connections: list):
        for switch in self._device_config['switch_info']: 
            if connections[switch]:
                self._device_config['switch_info'][switch]['selected'] = True
            else: 
                self._device_config['switch_info'][switch]['selected'] = False
    def building_map(self) -> dict: 
        try:
            switches = self._device_config['building_code_map']
            return switches
        except KeyError as e:
           self.app.notify(f"Config Key Error: {e}")
    def building_ip_codes(self) -> dict:
        try:
            ip_codes = self._device_config['building_ip_codes']
            return ip_codes
        except KeyError as e:
            self.app.notify(f"Config Key Error: {e}")
    def get_current_devices_config(self) -> dict:
        try:
            return {
                "devices" : self._device_config.get('devices', {}),
                "device_types" : self._device_config.get('device_types', {}),
                "device_groups" : self._device_config.get('device_groups', {}),
            }
        except KeyError as e:
          print(f"Config Key Error: {e}")

    def validate_field_input(self, field_type, value): 
        if True:
            return True
        else:
            return False 
            
        
    def save_device_config(self, device:str, config:dict) -> list[dict]:
        
            
        pending_updates = {}
        device_config = self._device_config.get('devices').get(device)
        device_fields = self.get_device_fields(device)
        successful_updates = {}
        failed_updates = {}

        # First, we validate the input values to ensure they are the expected types
        for field in config: 
            if field in device_fields: 
                if self.validate_field_input(device_fields[field]['type'], config[field]):
                    # Only Make these checks if the field already exists in the device config.  
                    if field in device_config:
                        if config[field] == device_config[field]:
                            
                            pending_updates[field] = config[field]
                            continue

                        elif config[field] == '':
                            print(f"Field {field} is empty, skipping update.")
                            failed_updates[field] = f'Unaable to save {field} Empty field'
                            continue
                    pending_updates[field] = config[field]
                else: 
                    print(f"Invalid field input for {field}: {config[field]}")
                    failed_updates[field] = 'Invalid field input, expected type: ' + device_fields[field]['type'] + ' but got: ' + str(type(config[field])+ '(' + (config[field])) + ')'
                    continue
            else:
                failed_updates[field] = f'Field {field} not found in device config'
                continue
        
        for field in pending_updates:
            self._device_config['devices'][device][field] = pending_updates[field]
            
            successful_updates[field] = 'Updated'
        self.commit()
        return successful_updates, failed_updates
            
    def commit(self):
        try:
            self.write_config()
            print("Config changes committed successfully.")
        except Exception as e:
            print(f"Error committing config changes: {e}")


    
    def get_device_fields(self, device: str) -> dict:
        try:
            fields = self._device_config.get('device_fields')
            current_config = self._device_config.get('devices').get(device)
            for field in fields: 
                if field in current_config:
                    fields[field]['value'] = current_config[field]  

            return fields
                
            

            
        except KeyError as e:
            print(f"Config Key Error: {e}")
        

        
    





 
