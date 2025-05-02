# TODO: Convert these widget to work with
# import asyncio
# from textual import on, work
# from textual.keys import Keys
# from textual.containers import HorizontalGroup, VerticalGroup, Vertical, Grid
from backend.Blueprints.Widgets import Input, Static
from backend.Blueprints.Widgets.Container import VerticalGroup, HorizontalGroup, Collapsible
from backend.api.helpers.ConfigHelper import ConfigHelper
# from textual.widgets import Switch, Static, Button, Collapsible, Checkbox, Label, Input, Pretty, TextArea, Select
# from textual.app import ComposeResult
# from textual.suggester import SuggestFromList
# from textual.visual import Visual
# from textual.reactive import reactive, Reactive
# from textual.color import Color
# from textual.worker import Worker, WorkerState
# from helpers.ConnectionHelper import ConnectionHelper, NetDevice
# from textual.notifications import Notify
# from time import monotonic
# from helpers.ConfigHelper import ConfigHelper
# from textual.validation import Function
# from threading import Thread
# from time import sleep
# from enum import Enum

# class ConnectionIndicator(Static):
   
#     def __init__(self, content = "", *, expand = False, shrink = False, markup = True, name = None, id = None, classes = None, disabled = False):
#         super().__init__(content, expand=expand, shrink=shrink, markup=markup, name=name, id=id, classes=classes, disabled=disabled)
    
        
# class ConnectionStatusWidget(VerticalGroup): 
    
#     def __init__(self, switch):
#         self.hostname = switch
#         super().__init__(id=f'{self.hostname}-status-stack')
#         self.switch_name = Label(switch)
        
#         self.connection_indicator = ConnectionIndicator('Checking...', id=f'{self.hostname}-connection-indicator', classes='connected')
#         self.styles.color = 'gray'

#     def _on_mount(self, event):
#         self.set_interval(0.2, self.update_connection_status)
#         self.mount(self.switch_name)
#         self.mount(self.connection_indicator)
#         self.connection_helper: ConnectionHelper = self.app.connection_helper
#         return super()._on_mount(event)
#     #def on_timer(self, event):
#         #self.update_connection_status()
#         #return super().on_timer(event)
#     def update_connection_status(self):
        
#         status = self.connection_helper.get_connection_status(self.hostname)
#         if status == 'Connected':
#             self.connection_indicator.remove_class('connectionfailed')
#             self.connection_indicator.add_class('connected')
#             self.styles.color = 'green'
#         elif status == 'Not Connected': 
#             self.connection_indicator.add_class('connectionfailed')
#             self.styles.color = 'white'
#         else:
#             self.styles.color = 'red'
#         self.connection_indicator.update(status)      
# class Connection_Switch(Switch):
#     def __init__(self, value = False, *, animate = True, name = None, id = None, classes = None, disabled = False, tooltip = None):
#         super().__init__(value, animate=animate, name=name, id=id, classes=classes, disabled=disabled, tooltip=tooltip)
#         self.styles.width = 'auto'
#     async def _on_click(self, event):
#         super()._on_click(event)
#         connection_helper: ConnectionHelper = self.app.connection_helper
#         if self.value == False:
#             await connection_helper.connect_device(hostname=self.id)
#         else:
#             await connection_helper.disconnect(switch=self.id)
#     def _on_mount(self, event):
#         self.set_interval(1, self.update_connection_status)
#         super()._on_mount(event)
#     def update_connection_status(self):
        
#         status = ConnectionHelper().get_connection_status(self.id)
#         if status == 'Connected':
#             self.value = True
#         else: 
#             self.value = False
# class DeviceConnectionCheckbox(Checkbox):
#     def __init__(self, label = "", value = False, button_first = True, *, name = None, id = None, classes = None, disabled = False, tooltip = None):
#         super().__init__(label, value, button_first, name=name, id=str(id), classes=classes, disabled=disabled, tooltip=tooltip)
#         self.styles.width = 'auto'
#         self.styles.height = 'auto'
        
#     async def _on_click(self, event):
#         super()._on_click(event)
        
#         if self.value == False:
#             self.connection_helper.connect_device(hostname=self.id)
#         else:
#             await self.connection_helper.disconnect(hostname=self.id)
#     def _on_mount(self, event):
#         self.set_interval(1, self.update_connection_status)
#         self.connection_helper: ConnectionHelper = self.app.connection_helper
#         return super()._on_mount(event)
#     def update_connection_status(self):
#         status = self.connection_helper.get_connection_status(self.id)
#         if status == 'Connected':
#             self.value = True
#         else:
#             self.value = False
# class Connection_Toggle_Widget(VerticalGroup):
    
#     def __init__(self, device):
#         hostname = device['host']
#         super().__init__(id=f'{hostname}-togglegroup')
#         # Commented out, this will set the default to disconnected, saving selected switches does nothing now 
#         #is_selected = switch['selected']
#         self.hostname = hostname
#         self.toggle = Connection_Switch(False, id=f'{hostname}')
#         self.connection_indicator = ConnectionStatusWidget(hostname)
        
#     def value(self):
#         return self.toggle.value
#     def _on_mount(self, event):
#         self.mount(self.toggle)
#         self.mount(self.connection_indicator)
#         return super()._on_mount(event)
# class ConnectionCheckboxWidget(HorizontalGroup):
#     def __init__(self, net_device: NetDevice):
#         hostname = net_device.name
#         self.device = net_device
#         super().__init__(id=f'{hostname}-checkboxgroup')
#         # Commented out, this will set the default to disconnected, saving selected switches does nothing now 
#         #is_selected = switch['selected']
#         self.hostname = hostname
#         self.toggle = DeviceConnectionCheckbox(value=False, id=f'{hostname}')
#         self.connection_indicator = ConnectionStatusWidget(hostname)
#     def value(self):
#         return self.toggle.value
#     def _on_mount(self, event):
#         super()._on_mount(event)
#         self.mount(self.toggle)
#         self.mount(self.connection_indicator)
#         return super()._on_mount(event)



class ConfigInputContainer(HorizontalGroup):
    css_class = "config-input"
    def __init__(self, setting: str, value: str):
        
        self.children = [Static.Label(label_text=setting), Input.Input(id=f'{setting}-input', value=value)]

        super().__init__(id=f'{setting}config-input')
        
        
        
class ConfigContainer(VerticalGroup):
    css_class = "config-container"
    def __init__(self, setting: str, data: dict):
        self.data = data   
        super().__init__(id=f'{setting}-config-container')
   

class DeviceSettingContainer(ConfigContainer):
    _description = "Device Setting Container"
    css_class = "device-setting-container"
    def __init__(self, device: str, data: dict):
        self.device = device
        self.data = data
        self.children = [ConfigInputContainer(setting=setting, value=value) for setting, value in data.items()]
        super().__init__(setting=f'{device}', data=data)
        
        
   
class ConfigCollapsible(Collapsible):
    _default_css_class = "config-collapsible"
    def __init__(self, id: str, label_text: str, collapsed_symbol='>', expanded_symbol='V', config_elements: dict = None):
        self.inner_html = label_text
        
        super().__init__(id=id, collapsed_symbol=collapsed_symbol, expanded_symbol=expanded_symbol, label_text=label_text)
   

        
    
            
        
    
class ConnectionSelector(Collapsible):
    _default_css_class = "connection-selector"
    
    def __init__(self, id, children: list, collapsed_symbol= '>', expanded_symbol='V', title = 'Connection Selector'):    
        super().__init__(id, children, collapsed_symbol='>>>', expanded_symbol='V', label_text=title)
        
        
#     def compose(self) -> ComposeResult:
#         super().compose() 
#         self.connection_helper: ConnectionHelper = self.app.connection_helper
#         switch_list = self.connection_helper.get_devices_by_type('switch')
#         self.connection_widgets = []
#         for switch in switch_list:
#             switch_toggle = ConnectionCheckboxWidget(switch)
#             self.connection_widgets.append(switch_toggle)
#         """Create the layout of the menu."""
#         # Create a container for each group of buttons based on the first 2 chars of the id
#         containers = {}
#         for checkbox in self.connection_widgets:
#             dash_index = str.find(checkbox.id, '-')
#             building = checkbox.id[:dash_index]
#             if building not in containers:
#                 containers[building] = []
#             containers[building].append(checkbox)
#         # Yield each container with buttons, setting direction to horizontal
#         all_grid_items = []
#         for building, toggle_groups in containers.items():
#             if building in self.app.config_helper.building_map():
#                 building_lable = Static(f'{self.app.config_helper.building_map()[building]}-{len(toggle_groups)}')
#                 building_lable.styles.background = 'blue'
#                 building_lable.styles.border_bottom = 'solid', 'white'
#                 all_grid_items.append(building_lable)
#             grid = Grid(*toggle_groups, classes="checkbox-group")
#             grid.styles.height = 'auto'
#             grid.styles.grid_size_columns = 4
#             all_grid_items.append(grid)
#         yield self._title
        
#         yield self.Contents(*all_grid_items)
# class SwitchSelectDropdown(ConnectionSelector):
#     def __init__(self):
        
        
#         super().__init__(title='Switch Selector')
        
#         self.connection_count = reactive(0, recompose=True)
#     def _on_mount(self, event):
#         super()._on_mount(event)
#         self.connection_helper: ConnectionHelper = self.app.connection_helper
#         switch_list = self.connection_helper.get_devices_by_type('switch')
#         self.connection_widgets = []
#         for switch in switch_list:
#             switch_toggle = ConnectionCheckboxWidget(switch)
#             self.connection_widgets.append(switch_toggle)
#         self.set_interval(0.3, self.update_connection_counts)
#     def update_connection_counts(self):
#         connection_count = self.connection_helper.connection_counts_filtered_by_type(device_type='switch')
#         num_color = 'red' if connection_count == 0 else 'green'
#         if connection_count != self.connection_count:
#             self.connection_count = connection_count
#             self.title = f'Switch Selector -- Active Connections: [{num_color}]{connection_count}' 
# class WLCConnectionDropdown(ConnectionSelector):
#     def __init__(self):
#         self.connection_widgets = []
#         super().__init__(title='WLC Selector')
        
#     def _on_mount(self, event):
#         super()._on_mount(event)
#         wlc_list = ConnectionHelper().get_devices_by_type('wlc')
#         for hostname in wlc_list:
#             wlc_toggle = ConnectionCheckboxWidget(hostname)
#             self.connection_widgets.append(wlc_toggle)
#         self.connection_count = reactive(0, recompose=True)
#         self.set_interval(0.3, self.update_connection_counts)
#     def update_connection_counts(self):
#         connection_count = ConnectionHelper().connection_counts('wlc')
#         num_color = 'red' if connection_count == 0 else 'green'
#         if connection_count != self.connection_count:
#             self.connection_count = connection_count
#             self.title = f'WLC Selector -- Active Connections: [{num_color}]{connection_count}' 
# class Suggestion_Input(Input):
#     def switches_selected(string):
#         if string:
#             return ConnectionHelper().connection_counts_filtered_by_type('switch') > 0
#         else:
#             return True
#     def input_not_empty(string):
#         return True if len(string) > 0 else False
    
#     default_validators = [
#         Function(switches_selected, 'There are no active connections'),
#         Function(input_not_empty, 'Empty Input')
#     ]
#     def __init__(self, suggestion_type = None, value = None, placeholder = "", highlighter = None, password = False, *, restrict = None, type = "text", max_length = 0, suggester = None, validators = None, validate_on = None, valid_empty = False, select_on_focus = True, name = None, id = None, classes = None, disabled = False, tooltip = None):
#         validators = self.default_validators + validators if validators else self.default_validators

#         super().__init__(value, placeholder, highlighter, password, restrict=restrict, type=type, max_length=max_length, suggester=SuggestFromList(self.app.config_helper.get_suggestions(suggestion_type)), validators=validators, validate_on=validate_on, valid_empty=valid_empty, select_on_focus=select_on_focus, name=name, id=id, classes=classes, disabled=disabled, tooltip=tooltip)
#         self.last_input = None
#         self.suggestion_type = suggestion_type
#     @on(Input.Changed)
#     def get_suggestions(self):            
#         return self.app.config_helper.get_suggestions(self.suggestion_type)
#     def action_submit(self):
#         return super().action_submit()
# class Config_Output(Pretty):
#         def __init__(self, text: str):
#             super().__init__(text)
#             self.text = text
#             self.textbox = TextArea(text)
#             self.textbox.disabled = True
#             self.styles.background = Color(169, 169, 160)
#         def _on_click(self, event):
#             super()._on_click(event)
#             self.show_selectable_text_box(self.text)
#         async def update(self, object: list | None = None, raw: str | None = None):
#             if not raw: 
#                 raw = '\n'.join(object)
#             if not object: 
#                 object = raw.splitlines()
#             self.text = raw
#             return super().update(object)
#         def show_selectable_text_box(self, text):
#             if self.textbox.disabled:
#                 self.textbox.text = text
#                 self.textbox.disabled = False
#                 self.mount(self.textbox)
#             else:
#                 self.textbox.remove()
#                 self.textbox.disabled = True
# class ReactiveOutputBox(VerticalGroup):
#     def __init__(self, switchname):
#         super().__init__()
#         self.switch = switchname
#         self.label = Label(switchname)
#         self.label.styles.text_align = 'center'
#         self.label.styles.width = '100%'
#         self.label.styles.border = 'solid', 'blue'
#         self.output = Config_Output('Sending Command...')
#         self.output.styles.background = Color(169, 169, 169)
#     async def update_output(self, new_value: str | list):
#         if not new_value:
#             self.display = False
#             return
#         self.display = True
#         outputs = new_value
#         if type(outputs) == str:
#             outputs = outputs.split('\n') 
#         await self.output.update(outputs, new_value)
#     def _on_mount(self):
#         self.mount(self.label)
#         self.mount(self.output)

# class QuickConnectButtons(HorizontalGroup):
#     buttons = None
#     class QuickConnectButton(Button):
#         def __init__(self, label):
#             self.connection_count = 0
#             self.filter_str = label
#             super().__init__(f'{self.filter_str} {0}')
        
#         def check_connections(self):
#             raise NotImplementedError('QuickConnectButtons.check_connections is an abstract method')
#     def __init__(self):
        
#         super().__init__()
#     async def _on_click(self, event):
#         super()._on_click(event)
#     def _on_mount(self):
#         self.connection_helper = self.app.connection_helper
#         for button in self.buttons:
#             self.mount(button)
# class SwitchQuickConnectButtons(QuickConnectButtons):
#     device_type='switch'
    
#     class SwitchQuickConnectButton(QuickConnectButtons.QuickConnectButton):
#         @on(Button.Pressed)
#         async def _on_click(self, event):
#             if self.connection_count == 0:
#                 self.connection_helper.connect_all(self.filter_str)
#             else:
#                 self.connection_helper.disconnect_all_switches(self.filter_str)
            
#         def _on_mount(self, event):
#             self.connection_helper: ConnectionHelper= self.app.connection_helper
#             self.set_interval(0.3, self.check_connections)
#             return super()._on_mount(event)
#         def check_connections(self):
#             connection_count = self.connection_helper.connection_counts_filtered_by_type(device_type='switch', name_filter=self.filter_str)
#             num_color = 'gray' if connection_count == 0 else 'green'
#             if connection_count != self.connection_count:
#                 self.connection_count = connection_count
#                 self.label = f'{self.filter_str} [{num_color}]{connection_count}'    
#     buttons = [
#             SwitchQuickConnectButton('MDF'),
#             SwitchQuickConnectButton('IDF'),
#             SwitchQuickConnectButton('CORE'),
#             SwitchQuickConnectButton('HS-MDF'),
#             SwitchQuickConnectButton('TECH-MDF'),
#         ]
        
# class WLCQuickConnectButtons(QuickConnectButtons):
#     device_type='wlc'
    


#     class WLCQuickConnectButton(QuickConnectButtons.QuickConnectButton):
        
#         def __init__(self, label=None):
#             self.host = label
#             super().__init__(label)
#         def check_connections(self):
#             num_color = 'gray' if not ConnectionHelper().check_if_connected(self.host) else 'green'
#             self.label = f'[{num_color}]{self.host}'    
#         def _on_mount(self, event):
#             self.set_interval(0.3, self.check_connections)
#             return super()._on_mount(event)
#     buttons = [
#             WLCQuickConnectButton('HS-WLC'),    
#         ]                 
#     def __init__(self):
#         super().__init__()
class CommandOutputWidget(VerticalGroup):
     _default_css_class = "command-output-widget"
     def __init__(self, id: str, children: list = None):
         super().__init__(id, children)
         self.boxes = {}
#     def _on_mount(self):
#         self.mount(Label('Outputs:'))       
#     async def send_command_to_connected(self, command: str, mode=None) -> None:
#         connect_helper: ConnectionHelper = self.app.connection_helper
#         active_connections = connect_helper.connected_devices()
#         self.clear_outputs()

#         tasks = []
#         method =  self.send_command_and_update_output
#         for switch in active_connections.keys():
#             if switch not in self.boxes:
#                 self.boxes[switch] = ReactiveOutputBox(switch)
#                 self.mount(self.boxes[switch])
#             tasks.append(asyncio.create_task(self.send_command_and_update_output(active_connections[switch], command)))
#         await asyncio.gather(*tasks)
 
#         if mode == 'DIFF':
#             self.show_differences()
#         if mode == 'UNIQUE':
#             self.show_unique_lines()               
#     def show_differences(self):
#         current_results = {}
#         clean_results = {}
#         for box in self.boxes:
#             current_output = self.boxes[box].output.text
#             if current_output:
#                 current_results[box] = current_output.split('\n')
        
#         if not current_results:
#             return
        
#         # Find common lines in all results
#         common_lines = set.intersection(*map(set, current_results.values()))
        
#         # Remove common lines from each result
#         for box, lines in current_results.items():
#             clean_results[box] = [line for line in lines if line not in common_lines]
        
#         # Update the output boxes with the cleaned results
#         for box, lines in clean_results.items():
#             self.boxes[box].update_output('\n'.join(lines))
#     def show_unique_lines(self):
#         current_results = {}
#         line_counts = {}
#         # Collect current outputs
#         for box in self.boxes:
#             current_output = self.boxes[box].output.text
#             if current_output:
#                 lines = current_output.split('\n')
#                 current_results[box] = lines
#                 # Count occurrences of each line across all boxes
#                 for line in lines:
#                     line_counts[line] = line_counts.get(line, 0) + 1

#         if not current_results:
#             return

#     # Keep only unique lines (those that appear exactly once)
#         unique_results = {
#             box: [line for line in lines if line_counts[line] == 1]
#             for box, lines in current_results.items()
#         }

#         # Update the output boxes with the unique results
#         for box, lines in unique_results.items():
#             self.boxes[box].update_output('\n'.join(lines))
#     def clear_outputs(self):
#         self.display = False
#         for box in self.boxes: 
#             box = self.boxes[box]
#             box.display = False
#     async def send_command_and_update_output(self, switch: NetDevice, command: str) -> None:
#         result = await switch.send_async_command(command=command)
#         box: ReactiveOutputBox = self.boxes[switch.name]
#         await box.update_output(result)
    

#     ## Migrating this to an async method -- uncomment here and in ConfigCheckScreen to restore
#     '''
#     def show_outputs(self, switch_port_dict: dict):
#         self.switchport_dict = switch_port_dict
#         for switch in sorted(switch_port_dict.keys()):
#             if len(switch_port_dict[switch]) == 0:
#                 continue
#             if switch not in self.trees:
#                 tree = Config_Tree(switch_name=switch, switch_ports=switch_port_dict[switch])
#                 self.trees[switch] = tree
#                 self.mount(self.trees[switch])
#             else:
#                 tree = self.trees[switch]
#                 tree.update_trees(switch_port_dict[switch])
#         for tree in self.trees:
#             self.trees[tree].display = True
#     '''     
#     def compose(self) -> ComposeResult: 
#         yield Label('Config Ports')
#         super().compose()

        
# class ModeSelector(Select): 
#     def from_enum(enum: Enum, default_value = None):
#         select =  Select.from_values([mode.value for mode in enum])
#         select._allow_blank = False
#         select.value = next(iter(enum)).value
        
#         if default_value: 
#             select.value = default_value
#         select.prompt = select.selection
#         return select
    
    

