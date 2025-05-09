#from textual import on
#from textual.screen import Screen
#from textual.widgets import Button, Label, Static, Header
#from textual.widget import Widget
#from textual.containers import HorizontalGroup, VerticalGroup
#from widgets.CustomWidgets import Command_Output_Widget, SwitchQuickConnectButtons, SwitchSelectDropdown, WLCQuickConnectButtons, WLCConnectionDropdown, QuickConnectButtons, ConnectionSelector
from flask import Flask, Blueprint, current_app
from backend.Blueprints.Widgets.Buttons import HeaderButton, FooterButton
from backend.Blueprints.Widgets.CustomWidgets import CommandOutputWidget
from typing import TYPE_CHECKING

if TYPE_CHECKING: 
    import backend.Blueprints.Widgets as Widgets
    from backend.Blueprints.Widgets import Container, Static
    from backend.Blueprints.SettingsPage import SettingsPage
import inspect

class DefaultPage(Blueprint):
    # These now load in the base page, and can be overridden
    header_buttons = [ HeaderButton(text='Header'), HeaderButton(text='Buttons'), HeaderButton(text='Here')]
    footer_buttons = [ FooterButton(text='Footer'), FooterButton(text='Buttons'), FooterButton(text='Exit')]
    
    app = current_app    
    
    

    def __init__(self, name):  
    
        self.content = self.content if hasattr(self, 'content') else None
        
        
        #self.quick_connects = quick_connects
        #self.connect_dropdown = connect_dropdown
        #self.header_buttons = header_buttons
        #self.footer_buttons = footer_buttons
        super().__init__(name=name, import_name=__name__, template_folder='../../frontend/templates', static_folder='../../frontend/static', )
    def get_content(self):
        return self.content
   
    def log_warning(self, message: str, **kwargs):
        # Log a warning message with formatted key-value pairs
        # Inject the class, calling method, and line number into kwargs
        stack = inspect.stack()
        if len(stack) > 1:
            caller_frame = stack[1]
            caller_class = caller_frame.frame.f_locals.get('self', None).__class__.__name__ if 'self' in caller_frame.frame.f_locals else None
            caller_method = caller_frame.function
            caller_line = caller_frame.lineno
            # Print caller information in a single line
            caller_info = f"\033[95mCaller Class\033[0m: {caller_class}, \033[95mCaller Method\033[0m: {caller_method}, \033[95mCaller Line\033[0m: {caller_line}"
            print(caller_info)
        # Print the message
        formatted_message = f"\033[93m{message}\033[0m"
        print(formatted_message)
    #quick_connects: QuickConnectButtons = None
    #connect_dropdown: ConnectionSelector = None
    #footer_buttons = _footer_buttons()
    #def __init__(self, label, content_viewer, quick_connects, connect_dropdown):
    #    self.quick_connects = quick_connects
    #    self.connect_dropdown = connect_dropdown
    #    super().__init__()
    #    self.label = Label(label)
       
    #@on(Button.Pressed)
    #def _on_button_pressed(self, event):
    #   id = event.button.id
    #    if id == 'clear' or id == 'clear_bottom':
    #        self.content.clear_outputs()
    #    if id == 'exit' or id  == 'exit_bottom':
    #        self.app.pop_screen()
    #def compose(self):
    #    yield Header(show_clock=True)
    #    yield self.quick_connects
    #    yield self.connect_dropdown
    #    yield self.label
    #    yield self.header_buttons
    #    yield self.content
    #    yield self.footer_buttons
    #    return super().compose() 
    
    
class DefaultSwitchScreen(DefaultPage):
    
    def __init__(self, name):
        #quick_connects = SwitchQuickConnectButtons()
        #connect_dropdown = SwitchSelectDropdown()
        #content_viewer = Command_Output_Widget()
        super().__init__(name=name)
        pass
class DefaultWLCScreen(DefaultPage):
    def __init__(self, name):
        #quick_connects = WLCQuickConnectButtons()
        #connect_dropdown = WLCConnectionDropdown()
        #content_viewer = Command_Output_Widget()
        #super().__init__(label, quick_connects=quick_connects, connect_dropdown=connect_dropdown, content_viewer=content_viewer)
        super().__init__(name=name)
        
        
        
