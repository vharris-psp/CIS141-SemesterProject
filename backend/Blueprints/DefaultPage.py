#from textual import on
#from textual.screen import Screen
#from textual.widgets import Button, Label, Static, Header
#from textual.widget import Widget
#from textual.containers import HorizontalGroup, VerticalGroup
#from widgets.CustomWidgets import Command_Output_Widget, SwitchQuickConnectButtons, SwitchSelectDropdown, WLCQuickConnectButtons, WLCConnectionDropdown, QuickConnectButtons, ConnectionSelector

from backend.Blueprints.Widgets.Buttons import HeaderButton, FooterButton
from backend.Blueprints.Widgets.CustomWidgets import CommandOutputWidget
    
class DefaultPage:
    # These now load in the base page, and can be overridden
    header_buttons = [ HeaderButton(label='Header', id='header-button-1'), HeaderButton(label='Buttons', id='header-button-2'), HeaderButton(label='Here', id='header-button-3')]
    footer_buttons = [ FooterButton(label='Footer', id='footer-button-1'), FooterButton(label='Buttons', id='footer-button-2'), FooterButton(label='Here', id='footer-button-3')]
    content: CommandOutputWidget  = None

    def __init__(self, label):  
        self.label = label
        self.content = CommandOutputWidget()
        #self.quick_connects = quick_connects
        #self.connect_dropdown = connect_dropdown
        #self.header_buttons = header_buttons
        #self.footer_buttons = footer_buttons
    def get_content(self):
        return self.content


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
    
    def __init__(self, label):
        #quick_connects = SwitchQuickConnectButtons()
        #connect_dropdown = SwitchSelectDropdown()
        #content_viewer = Command_Output_Widget()
        #super().__init__(label, quick_connects=quick_connects, connect_dropdown=connect_dropdown, content_viewer=content_viewer)
        pass
class DefaultWLCScreen(DefaultPage):
    def __init__(self, label):
        #quick_connects = WLCQuickConnectButtons()
        #connect_dropdown = WLCConnectionDropdown()
        #content_viewer = Command_Output_Widget()
        #super().__init__(label, quick_connects=quick_connects, connect_dropdown=connect_dropdown, content_viewer=content_viewer)
        pass
        
        
        
