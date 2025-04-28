import json 
import os



def load_config(filename):
    config_path = os.path.join(os.path.dirname(__file__), 'config', filename)
    with open(config_path, 'r') as f:
        return json.load(f)
    
def save_config(filename, data):
    config_path = os.path.join(os.path.dirname(__file__), 'config', filename)
    with open(config_path, 'w') as f:
        json.dump(data, f, indent=4)



def building_codes():
    codes = json.loads("config/backendconf.json")
    return codes['building_ip_codes']
