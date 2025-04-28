from enum import Enum
import re
from backend.api.config_loader import building_codes
import inspect

# Folder Settings
class regex_str(Enum):
    no_space = r'!.+$'
class patterns(Enum):
    not_hex = r'[^0-9A-Fa-f]'
    hex = r'[0-9A-Fa-f]'
    show = r'^\s*show'
    include = r'^\s*include'
# Maps WLC Fields to regex rules - Building,Room,Asset,Mac,SN,CAPWAP_NAME
def is_in_building_list(value):
    is_in_list = value in building_codes.values()
    if not is_in_list:
        raise ValueError(f"Invalid building code: {value}")
    return is_in_list
def get_compiled_pattern(pattern: patterns):
    compiled_pattern = re.compile(pattern.value)
    return compiled_pattern
## ALL RULES MUST BE A BOOL METHOD OR REGEX STRING
regex_dicts = {
    'mac' : {
        'MAC' : [r'[0-9A-F]{12}'],
        'mac' : [r'[0-9a-f]{12}'],
        'MAC_DASH_2' : [r'([0-9A-F]{2}-){5}[0-9A-F]{2}'],
        'MAC_SPACE_2' : [r'([0-9A-F]{2} ){5}[0-9A-F]{2}'],
        'MAC_COLON_2' : [r'([0-9A-F]{2}:){5}[0-9A-F]{2}'],
        'MAC_PERIOD_4' : [r'([0-9A-F]{4}\.){2}[0-9A-F]{4}'],
        'mac_dash_2' : [r'([0-9a-f]{2}-){5}[0-9a-f]{2}'],
        'mac_space_2' : [r'([0-9a-f]{2} ){5}[0-9a-f]{2}'],
        'mac_colon_2' : [r'([0-9a-f]{2}:){5}[0-9a-f]{2}'],
        'mac_period_4' : [r'([0-9a-f]{4}\.){2}[0-9a-f]{4}'],
        'any': [(
            r'([0-9A-F]{12}|'                     # MAC: 12 uppercase hex characters
            r'[0-9a-f]{12}|'                      # mac: 12 lowercase hex characters
            r'([0-9A-F]{2}-){5}[0-9A-F]{2}|'      # MAC_DASH_2: Uppercase, dash-separated
            r'([0-9A-F]{2} ){5}[0-9A-F]{2}|'      # MAC_SPACE_2: Uppercase, space-separated
            r'([0-9A-F]{2}:){5}[0-9A-F]{2}|'      # MAC_COLON_2: Uppercase, colon-separated
            r'([0-9A-F]{4}\.){2}[0-9A-F]{4}|'     # MAC_PERIOD_4: Uppercase, period-separated
            r'([0-9a-f]{2}-){5}[0-9a-f]{2}|'      # mac_dash_2: Lowercase, dash-separated
            r'([0-9a-f]{2} ){5}[0-9a-f]{2}|'      # mac_space_2: Lowercase, space-separated
            r'([0-9a-f]{2}:){5}[0-9a-f]{2}|'      # mac_colon_2: Lowercase, colon-separated
            r'([0-9a-f]{4}\.){2}[0-9a-f]{4})'     # mac_period_4: Lowercase, period-separated
        ),]
    },
    'sn' : {
        'SN_UPPER' : [r'FJ[0-9A-Z]{9}',],
        'sn_lower' : [r'fj[0-9a-z]{9}',],
        'any': [r'[Ff][Jj][0-9A-Za-z]{9}']
    },
    'building' : {
        '2CHAR' : [is_in_building_list,],
        'any': [r'[A-Z]{2}',],
    },
    'string' : {
        'any': [r'!.*$',]
    },
    'room' : {
        '3DIGITorSTR' : [r'[0-9]{3}|[A-Z]{3,}[0-9]?|[0-9]{3}H',],
        'any': [r'[0-9]{3}|[A-Z]{3}',]
    },
    'asset' : {
        '6DIGIT' : [r'[0-9]{6}',],
        'any': [r'[0-9]{6}'],
    },
## ALL RULES MUST BE A BOOL METHOD OR REGEX STRING
}
device_regex_maps = {
    'WLC' : {
        'Mac': ['mac','MAC'],
        'SN': ['sn', 'SN_UPPER'],
        'Building': ['building', '2CHAR'],
        'Asset': ['asset', '6DIGIT'],
        'Room': ['room', '3DIGITorSTR'],
        'CAPWAP_NAME': ['string', 'any'],
    }
}
        
def check_pattern(regex_type: Enum, string: str) -> bool:
    if isinstance(regex_type, list):
        return any(re.search(pattern.value, string) for pattern in regex_type)
    return bool(re.search(regex_type.value, string))
def get_re_type(value):
    for regex_dict in regex_dicts:
        reg_pattern = regex_dicts[regex_dict]['MAC']
        if re.match(pattern=reg_pattern, string=value):
            return regex_dict
            

def valid_replacement(old, new, match_all=True) -> bool:
    patterns = regex_dicts[get_re_type(old)]
    
    if not match_all:
        
        for reg in patterns:
            if re.match(pattern=reg, string=old) and re.match(pattern=reg, string=new):
                print(f"{old} and {new} match pattern {reg}")
                return True
        
        
        return False
    
    else:
        # Ensure new value matches all patterns matched by the old value      
        for reg in patterns:
            old_matches = bool(re.fullmatch(pattern=patterns[reg], string=old))
            new_matches = bool(re.fullmatch(pattern=patterns[reg], string=new))
            
            if old_matches == new_matches:
                continue
            else:
                print('Invalid Input (Regexw)')
                return False
        return True
def valid_value(sample, input, type):
    patterns = regex_dicts[type.lower()] if type.lower() in regex_dicts else regex_dicts[get_re_type(sample)]
    for reg in patterns:
        sample_matches = bool(re.fullmatch(pattern=patterns[reg], string=sample))
        input_matches = bool(re.fullmatch(pattern=sample, string=input))
        if sample_matches == input_matches:
            continue
        else:
            print('Invalid Input')
            return False
    return True
def make_pretty(rules):
    pretty_string = '('
    for rule in rules:
        if callable(rule):
            pretty_string += f"{rule.__name__} | "
        else:
            pretty_string += f"{rule} | "
    pretty_string = pretty_string[:-3] + ')'
    return pretty_string

    
def get_field_rules(device, field):
    try:
        device_map = device_regex_maps[device.upper()][field]
        return regex_dicts[device_map[0]][device_map[1]]
    except KeyError as e:
        raise ValueError(f"Invalid device '{device}' or field '{field}'")
    except ValueError as e:
        raise ValueError(f"Invalid device '{device}' or field '{field}'")
    except Exception as e: 
        raise ValueError(f"Invalid device '{device}' or field '{field}'")

def valid_field_value(rules, input, strict=False):
    try:
        return check_input_against_rules(input, rules)
    except Exception as e:
        rules = regex_dicts['string']['any']
        try:
            if not strict:
                return check_input_against_rules(input, rules)
            else:
                return False
        except Exception as e:
            raise ValueError(f'{e} - Error checking input against rules')
            return False
    
    
def check_input_against_rules(input, rules):
    ## ALL RULES MUST BE A BOOL METHOD OR REGEX STRING
    for reg in rules:
        if inspect.isfunction(reg):
            if not reg(input):
                return False
            else:
                continue
        elif input == '':
            
            return False
        elif not re.fullmatch(pattern=reg, string=input):
            return False
    return True

def valid_replacement(old, new, match_all=True, type='string') -> bool:
    patterns = regex_dicts[type.lower()] if type.lower() in regex_dicts else regex_dicts[get_re_type(old)]
    
    if not match_all:
        
        for reg in patterns:
            if re.match(pattern=reg, string=old) and re.match(pattern=reg, string=new):
                print(f"{old} and {new} match pattern {reg}")
                return True
        
        
        return False
    
    else:
        # Ensure new value matches all patterns matched by the old value      
        for reg in patterns:
            old_matches = bool(re.fullmatch(pattern=patterns[reg], string=old))
            new_matches = bool(re.fullmatch(pattern=patterns[reg], string=new))
            
            if old_matches == new_matches:
                continue
            else:
                print('Invalid Input (Regexw)')
                return False
        return True
            
def remove_non_hex(mac: str)-> str:
    return re.sub(pattern=patterns.not_hex.value, repl='', string=mac)
def mac_to_AABBCC(mac: str)-> str:
    mac = mac.upper()
    mac = remove_non_hex(mac)
    return mac
def switch_config_common_patterns():
    patterns = []
    


