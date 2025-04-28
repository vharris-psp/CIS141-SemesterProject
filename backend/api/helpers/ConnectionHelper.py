import concurrent
from typing import Any, Callable, Dict, List
from netmiko import ConnectionException, NetmikoTimeoutException, BaseConnection, ConnectHandler
import backend.api.parsers as parsers
import asyncio
import inspect
from backend.api.helpers.Helper import Helper
from backend.api.helpers.ConfigHelper import ConfigHelper
from enum import Enum
from flask import current_app
# def notify_screen(notification):
#     stack = inspect.stack()
#     for info in stack: 
#         frame_self = info.frame.f_locals.get("self")
#         if isinstance(frame_self, Screen):
#             frame_self.notify(notification)
#             return

def notify_screen(notification):
    with current_app.app_context():
        if hasattr(current_app, 'socketio'):
            socketio = current_app.socketio
            socketio.emit('notification', {'message': notification})
        else:
            print(f"Notification: {notification}")        
class NetDevice:
    connection: BaseConnection = None
    switch_list = lambda self: self.get_devices_by_type('switch')
    switch_connection = lambda self: self.get_connections_by_type('switch')
    
    def __init__(self, name, config, device_type):
        self.name = name
        self.config = config
        self.type = device_type
        self.status = None  # Initialize status to None
    def is_connected(self):
        return self.connection != None
    async def connect(self):
        connection_settings = self.config['connection_settings']
        try:
            self.connection = await asyncio.to_thread(ConnectHandler, **connection_settings)
            self.status = 'Connected'
        except Exception as e:
            self.status = e
    async def send_async_command(self, commands: List[str] | None=None, command: str = None) ->  (str | List[Any] | Dict[str, Any]): 
        results = []
        # Convert string to list or list to str if wrong argument is passed
        if isinstance(commands, str):
            command = commands
            commands = None
        if isinstance(command, list):
            commands = command
            command = None
        # Ensure at least one argument was passed
        if commands is None and command is None:
            raise (ValueError("At least one command is required"))
        # Ensure only one argument is passed
        if commands and command:
            raise ValueError(f"'command' and 'commands' can not be used simultaneously. Command: {command} Commands: {commands}")
        connection = self.connection

        # Handle accordingly
        if isinstance(commands, list):
            for command in commands: 
                notify_screen(f'Sending {command} to {connection.host}')
                results.append(connection.send_command(command, expect_string='\\#'))        
            return results
        elif isinstance(command, str):
            notify_screen(f'Sending {command} to {connection.host}')
            return connection.send_command(command, expect_string='\\#')
        else:
            raise TypeError('Command or Commands is Incorrect Type -- Should be list or str')
    
    async def disconnect(self):
        try: 
            self.connection.disconnect()
            self.connection = None
            self.status = None
        except ConnectionException as e:
            self.notify(f"Connection Error: {e}")
        except NetmikoTimeoutException as e:
            self.notify(f"Timeout Error: {e}") 
        except Exception as e: 
            raise(e)
            
    
class ConnectionHelper(Helper):
    class DeviceType(Enum):
        SWITCH = 'switch'
        WLC = 'wlc'

    
    
    def __init__(self):
        super().__init__()
        DeviceLookup = Dict[str, Callable[[], Dict[str, NetDevice]]]
        self.connected_devices: lambda: Dict[str, NetDevice] = lambda: {
            name: device for name, device in self.devices.items() if device.is_connected()
        }
    active_wlc = None
        
    
    def _on_mount(self, event):
        
        self.devices: dict[str,NetDevice] = {}
        chelper: ConfigHelper = self.app.config_helper
        device_map = chelper.get_all_device_configs()
        for device_type in ConnectionHelper.DeviceType:
            device_type = device_type.value
            for device_name, config in device_map[device_type].items():
                if device_type == 'wlc': 
                    self.devices[device_name] = WLC(name=device_name, config=config, device_type=device_type)
                elif device_type == 'switch':
                    self.devices[device_name] = Switch(name=device_name, config=config, device_type=device_type)
                
        super()._on_mount(event)
        

    def check_if_connected(self, hostname) -> bool:
        return self.devices[hostname].is_connected() 
    
    #async def connect_device(self, hostname):
    #    async def run_task():
    #        task = self.devices[hostname].connect()
    #        await asyncio.gather(*task)
    #    try:
    #        await self.devices[hostname].connect()
    #    except KeyError as e:
    #        self.notify(f"Device Configuration Error, '{e}' missing from '{hostname}' configuration")
    #    except Exception as e:
    #        self.notify(f'Unknown Error {e}')
    #        
    async def disconnect(self, hostname):
        try: 
            await self.devices[hostname].disconnect()
        except KeyError as e:
            self.notify(f"Disconnect error, {e} is not connected.")
        except Exception as e:
            self.notify(f'Unknown Error {e}')
    def connect_device(self, hostname):
        async def run_task():
            task = self.devices[hostname].connect()
            await asyncio.gather(task)
        if asyncio.get_event_loop().is_running():
            asyncio.create_task(run_task())
        else:
            asyncio.run(run_task())
    def __send_disconnect(self, hostname) -> None:
        self.devices[hostname].disconnect()   
    def update_connections(self) -> dict[str,int] | None:
        connections = {}
        for device in self.devices.values(): 
            if device.is_connected(): 
                connections[device.name] = device
        self.connected_devices = connections
        return connections
    def connection_counts_filtered_by_name(self, filter) -> int:
        count = 0
        for device in self.connected_devices.values():
            if filter in device.name: 
                count += 1
        return count
    def connection_counts_filtered_by_type(self, device_type, name_filter=None) -> int:
        count = 0
        for device in self.connected_devices().values():
            if device_type == device.type: 
                if name_filter:
                    if name_filter in device.name:
                        count += 1
                else:
                    count += 1
        return count
    def get_devices_by_type(self, device_type):
        devices = [device for device in self.devices.values() if device.type == device_type]
        return devices
    
    ## Connection Methods
    def connect_all(self, filter=None, type=None):
        async def connect_devices():
            if filter and type:
                tasks = [device.connect() for device in self.devices.values() if type == device.type and filter in device.name]
            elif filter and not type:
                tasks = [device.connect() for device in self.devices.values() if filter in device.name]
            elif type and not filter:
                tasks = [device.connect() for device in self.devices.values() if type == device.type]
            else:
                tasks = [device.connect() for device in self.devices.values()]
            await asyncio.gather(*tasks)
        try:
            if asyncio.get_event_loop().is_running():
                asyncio.create_task(connect_devices())
            else:
                asyncio.run(connect_devices())
        except Exception as e:
            raise RuntimeError(f"Error during connect_all: {e}")
    def disconnect_all_by_name(self, filter = None):       
        async def run_tasks():
            if filter:
               for device in self.devices.values(): 
                   if filter in device.name and device.is_connected():
                       await device.disconnect()  
            else:
                for device in self.devices.values():
                    if device.is_connected():
                        await device.disconnect()     
        try:
            if asyncio.get_event_loop().is_running():
                asyncio.create_task(run_tasks())
            else:
                asyncio.run(run_tasks())
                
        except Exception as e:
            self.notify(e)
            raise Exception(e)
    def disconnect_all_switches(self, filter = None):       
        async def run_tasks():
            if filter:
               
               for device in self.devices.values(): 
                   if device.type == 'switch' and filter in device.name and device.is_connected():
                       await device.disconnect() 
                       
            else:
                for device in self.devices.values():
                    if device.is_connected():
                        await device.disconnect()     
        try:
            if asyncio.get_event_loop().is_running():
                asyncio.create_task(run_tasks())
            else:
                asyncio.run(run_tasks())
        except Exception as e:
            self.notify(f'{e}')
            raise NotImplementedError(e)
    def get_connection_status(self, host: str) -> str:     
        try: 
            host = self.devices[host]
            if host.status:
                return f'{host.status}'
            else:
                return f'Not Connected'
        except KeyError as key_e:
            return f'Not Connected'
        except TypeError as key_e:
            return f'{key_e}'
        except KeyError as key_e:
            return f"Cannot connect to witch {host} - Switch not in connections - {key_e}"
        except Exception as e:
            return f'{e}'
        
    async def async_disconnect(self, host):
        try: 
            # Get switch Connection Dictionary
            try: 
                device = self.devices[host]
                if device:
                    device.disconnect()
            except KeyError as key_e:
                return
        except KeyError as key_e:
            return
## Command Methods
    async def get_device(self, hostname: str) -> NetDevice:
        return self.devices[hostname]
    async def send_async_command(self, connection, commands):
        results = []
        for command in commands: 
            notify_screen(f'Sending {command} to {connection}')
            results.append(connection.send_command(command))
        return results
    async def send_async_command(self, device: NetDevice, command: str):
        notify_screen(f'Sending {command} to {device.name}')
        result = await asyncio.to_thread(self.devices[device.name].send_command, command)
        await asyncio.sleep(0)  # Sleep for 1 second
        return result
    
    #
    #def send_command_to_one(self, device: NetDevice, command:str):
    #    notify_screen(f'Sending {command} to {device}')
    #    result = await device.send_async_command(command)
    #    return f'{result}'
    
    def get_connected_devices(self,) -> list:
        return [device for device in self.devices.values() if device.is_connected()]
    def send_command_to_all_connected(self, command):
        outputs = {}
        notify_screen(f'Sending {command} to all connected switches')
        
        def send_command(switch):
            if self.switch_connections[switch]:
                return switch, self.switch_connections[switch].send_command(command)
            return switch, None
    
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(send_command, self.switch_connections.keys())
    
        # Collect results into the dictionary
        outputs = {switch: output for switch, output in results if output is not None}
    
        return outputs
    def shut_no_shut_ports(self, switch, ports):
        outputs = []
        connection = None
        if self.switch_connections[switch]:
            connection = self.switch_connections[switch]
        else:
            notify_screen(f'Error sending commands to {switch} - Switch not connected')
            return
        for port in ports: 
            commands = [
                'conf t',
                f'{port}',
                'shut', 
                'no shut',
                
            ]
            connection.send_command_timing(command_string=f"conf t\n {port}\n shut\n no shut\n end\n")
            results = []
            
            outputs.append(results)
        return outputs 
            
    def load_ap_summary(self):
        pass
        
class Switch(NetDevice):
    def __init__(self, name, config, device_type):
        super().__init__(name, config, device_type)
    async def flap_port(self, port: str):
        return await self.send_async_interface_command(interface= port, commands=['shut', 'no shut'])
        
    async def get_port_config(self, port: str) -> str:
        new_config = await self.send_async_command(f'show run int {port}')
        clean_config = parsers.get_config_from_show_run_int(new_config, port)
        clean_config = clean_config[1:]
        return clean_config
    async def send_async_interface_command(self, interface, commands: List[str] | None=None, command: str = None) -> (str | List[Any] | Dict[str, Any]):
        results = []
        if isinstance(commands, str):
            command = commands
            commands = None
        if commands is None and command is None:
            raise (ValueError("At least one command is required"))
        if commands and command:
            raise ValueError("'command' and 'commands' can not be used simultaneously.")
        connection = self.connection
        results.append(connection.send_command('conf t', expect_string='\\(config\\)#'))
        results.append(connection.send_command(f'interface {interface}', expect_string='\\(config-if\\)#'))
        if isinstance(commands, list):
            for command in commands: 
                notify_screen(f'Sending {command} to {self.connection.host}')
                results.append(connection.send_command(command, expect_string='\\(config-if\\)#'))   
            results.append(connection.send_command('end', expect_string='\\#'))     
            return results
        elif isinstance(command, str):
            notify_screen(f'Sending {command} to {self.connection.host}')
            return connection.send_command(command)
        else:
            raise TypeError('Command or Commands is Incorrect Type -- Should be list or str') 
class WLC(NetDevice):
    def __init__(self, name, config, device_type):
        super().__init__(name, config, device_type)
    
