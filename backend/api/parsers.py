import re
from collections import defaultdict
from backend.api.netreg import mac_to_AABBCC
import asyncio

def get_config_from_show_run_int(output, interface):
    config = []
    lines = output.splitlines()
    interface = interface.split(' ')[1]
    for line in lines:
        if interface in line:
            config.append(line)
        elif len(config) > 0:
            if line.startswith('!') or line == 'end':
                break
            config.append(line)
    return config

#def get_lldp_neighbors_and_ports(lldp_neighbor_output:str, device_strings) -> dict:
#    def merged_lines():
#        merged_lines = []
#        lldp_neighbor_lines = lldp_neighbor_output.splitlines()
#        
#        for line in lldp_neighbor_lines:
#            if len(line) == 0: 
#                continue     
#            if len(line.split()) == 1:
#                clean_line = line.strip()
#                clean_line += ' '
#                clean_line += lldp_neighbor_lines[lldp_neighbor_lines.index(line)+1].strip()
#                merged_lines.append(clean_line)
#            elif line[0] != ' ' and 'Ten' in line or line[0] != ' ' and 'Fiv' in line: 
#                merged_lines.append(line)                    
#        return merged_lines
#    lldp_neighbor_ports = {}
#    lldp_lines = merged_lines()
#    for line in lldp_lines:
#        split_line = line.split()
#        interface = " ".join(split_line[1:3])
#        # TODO This is a hack to get the port name, need to fix this
#        for type in device_strings:
#            if type in split_line[0]:
#                lldp_neighbor_ports[interface] = split_line[0]
#    return lldp_neighbor_ports


#def get_lldp_neighbors_and_ports(lldp_neighbor_output:str | None = None, device_strings = ['IPSPKR']) -> dict:





# This doesn't work if the device name is too long that it merged into the port name, can be removed eventually 
def get_lldp_neighbor_ports(lldp_neighbor_output):
        
        lldp_neighbor_ports = []
        lldp_neighbors = lldp_neighbor_output.splitlines()
        for line in lldp_neighbors:
            parts = line.split()
            if len(parts) >= 2:
                port = parts[1]
                lldp_neighbor_ports.append(port)
             
        return lldp_neighbor_ports
def get_10G_ports(running_config):
    
    ten_gig_ports = []
    

def ios_pattern(command):
    # Split command into parts
    parts = command.split()
    # Construct a regex pattern for each part
    pattern_parts = [re.escape(part) + r'.*?' for part in parts]
    # Join patterns with spaces to match in order
    pattern = r'\s+'.join(pattern_parts)
    # Create a regex pattern to match the whole line
    pattern = f".*{pattern}.*"
    return pattern

def normalize_mac(mac_address, format='xxxx.xxxx.xxxx'):
    clean_mac = ''.join(c for c in mac_address if c.isalnum())
    if len(clean_mac) != 12:
        raise ValueError("Invalid MAC address length")
    normalized_mac = clean_mac.lower()
    if format == 'xxxx.xxxx.xxxx':
        return f'{normalized_mac[0:4]}.{normalized_mac[4:8]}.{normalized_mac[8:12]}'.lower()
    if format == 'XXXX.XXXX.XXXX':
        return f'{normalized_mac[0:4]}.{normalized_mac[4:8]}.{normalized_mac[8:12]}'.upper()
    else:
        pass

def normalize_mac(mac_address, format='xxxx.xxxx.xxxx'):
    clean_mac = ''.join(c for c in mac_address if c.isalnum())
    if len(clean_mac) != 12:
        raise ValueError("Invalid MAC address length")
    normalized_mac = clean_mac.lower()
    if format == 'xxxx.xxxx.xxxx':
        return f'{normalized_mac[0:4]}.{normalized_mac[4:8]}.{normalized_mac[8:12]}'.lower()
    if format == 'XXXX.XXXX.XXXX':
        return f'{normalized_mac[0:4]}.{normalized_mac[4:8]}.{normalized_mac[8:12]}'.upper()
    if format == 'XX-XX-XX-XX-XX-XX':
        return '-'.join(normalized_mac[i:i+2] for i in range(0, len(normalized_mac), 2)).upper()
    else:
        print(f"Invalid format: {mac_address}")

def get_port_configs(ports, config, include_ports_not_configured = False, include_shutdown_ports = False):

    lldp_pattern = r"\bFi\d/\d+/\d+\b"
    sections = config_to_sections(config)
    port_configs = {}
    for port in ports:
        port_name = port
        if 'Fiv ' in port:
            port_name = f"{port}".replace('Fiv ', 'interface FiveGigabitEthernet').strip()
        if re.match(lldp_pattern, port_name):
            port_name = f"{port}".replace('Fi' , 'interface FiveGigabitEthernet')
        if 'Te' in port:
            port_name = port.split(' ', 1)[0]
            port_name = f"{port_name}".replace('Te', 'interface TenGigabitEthernet').strip()
        if 'Fo' in port:
            port_name = port.split(' ', 1)[0]
            port_name = f"{port_name}".replace('Fo', 'interface FortyGigabitEthernet').strip()
        if 'TwentyFive' in port:
            port_name = port.split(' ', 1)[0] 
            port_name = f"{port_name}".replace('TwentyFiveGigE', 'interface TwentyFiveGigE').strip()
        try: 
            if ' shutdown' in sections[port_name] and include_shutdown_ports == False:
                print(f"{port_name} not active")
                pass
            elif len(sections[port_name]) == 0 and include_ports_not_configured == False:
                print(f"No configuration on {port_name}")
            else:
                port_configs[port]= { 'port_name': port_name, 'config' : (sections[port_name])} 
        except KeyError as e:
            print(f"Error: Port '{e}' not found.")
    
    return port_configs

def macro_section_to_items(macro_section_output):
    
    sections = re.split(r'(?=^[^\s])', macro_section_output, flags=re.MULTILINE)
    no_macro_ports_count = 0
    descriptions = defaultdict(int)
    clean_sections = {}
    for section in sections:
        for line in section.splitlines():
            if line.startswith(' no macro auto processing'):
                no_macro_ports_count += 1
            if line.startswith(' macro description '):
                descriptions[line] += 1    
    for desc in descriptions:
        for section in section:
            section.replace(desc, '')
            section.replace('no macro auto processing', '')
    for desc, count in descriptions.items():
        print(f'{desc}: {count}')
    print(f'No Macro Ports: {no_macro_ports_count}')
    
    for section in sections: 
        print(section)
        
        
    
        
    return

    

def config_to_sections(config):

    config_sections = {}
    
    sections = f"{config}".split('!')
    
    for section in sections: 
        
        lines = section.strip().split('\n')
        if lines: 
            key = lines[0]
            
            
            config_sections[key] = lines[1:]

    return config_sections
    
async def wap_summary_to_dict_items(raw_summary, conn_helper):
    waps = {}
    def get_bldg_room_asst_from_name(name):
        building_pattern = r"([A-Z]{2,3})\d+"
        room_pattern = r"([A-Z]{2,3})(0-9){3}-"
        asset_pattern = r"-(\d{6})$"
        bldg_match = re.match(building_pattern,name)
        room_match = re.match(room_pattern, name)
        asset_match = re.search(asset_pattern, name)
        building = "XX"
        room = "XXX"
        asset = "ASSET"
        if bldg_match:
            building = bldg_match.group(1)
        if room_match:
            room = room_match.group(2)
        if asset_match:
            asset = asset_match.group(1)

        return building, room, asset
    async def summary_line_to_wap_dict(line):         
            #Pull and  Normalize MAC to AABBCC001122 format 
            wap = {}
            name = line.split()[0]
            ip = line.split()[7]
            mac = mac_to_AABBCC(line.split()[3])
            wap['Mac'] = mac
            wap['CAPWAP_NAME'] = name
            wap['IP'] = ip
            building, room, asset = get_bldg_room_asst_from_name(name)
            wap['Building'] = building
            wap['Room'] = room
            wap['Asset'] = asset
            # TODO:  This should all be requested at once
            output = await conn_helper.send_command_to_wlc(f'show ap name {name} inventory | include SN:')  
            wap['SN]'] = output.split()[5]
            return mac, wap
    wap_count = len(raw_summary)
    i = 0
    for line in raw_summary:
        i += 1
        mac, wap_dict = await summary_line_to_wap_dict(line)
        
        yield i / wap_count, mac, wap_dict