
from flask import Blueprint, render_template


## CONVERTED CODE
from enum import Enum
from backend.api.netreg import patterns, check_pattern
from backend.Blueprints.DefaultPage import DefaultSwitchScreen
class CommandMode(Enum):
    ALL_OUTPUTS = "All: Display All Outputs of a Command"
    DIFFERENCES = "Different: Display all Different Outputs of a Command"
    UNIQUE = "Unique: Display All Commands Unique to a Single Switch (Not Implemented)"  
    DIFFERENT_FROM_GOLDEN = "Not Golden: Not Implemented"
    
def contains_show_run(string: str):
    return check_pattern(regex_type=patterns.show, string=string)


class SwitchCommandScreen(DefaultSwitchScreen):
    # Deprecated, page now inherits from DefaultPage(Blueprint)
    #blueprint = Blueprint('switch_commands', __name__, template_folder='../../frontend/templates', static_folder='../../frontend/static')
    def __init__(self):
        super().__init__(name='switch_commands')
        self.outputs = {}
        
        
        @self.route('/command_page')
        def command_page():
            return render_template('command_page.html', header_buttons=SwitchCommandScreen.header_buttons, footer_buttons=SwitchCommandScreen.footer_buttons, content=SwitchCommandScreen.content)

        @self.route('/run_command')
        def run_command():
            # Logic for running commands
            return render_template('run_command.html')


    
## LEGACY CODE


        #self.label = label

        #self.input = Suggestion_Input(
        #    suggestion_type='',
        #    placeholder='interface', 
        #    type='text',
        #)
        #self.content = Command_Output_Widget()
        self.mode = CommandMode.ALL_OUTPUTS.value
        #self.invalidation_box = Pretty([])
        #self.mode_selector = ModeSelector.from_enum(CommandMode)


    #async def on_valid_input_submit(self, input_string: str):
    #    raise NotImplementedError('Can not execute abstract method')
#
    ### Class Methods 
    #@on(Select.Changed)
    #def on_mode_changed(self, event: Select.Changed) -> None:
    #    mode_selection = event.select.selection
    #    if mode_selection:
    #        self.mode = mode_selection
    #@on(Input.Submitted)
    #async def on_input_submit(self, event: Input.Submitted) -> None:
    #    
    #    if not event.validation_result.is_valid:
    #        self.input.value = ''
    #        self.input.placeholder = f'Invalid Input: {event.validation_result.failure_descriptions[0]}'
    #    else:
    #        await self.on_valid_input_submit(self.input.value, self.mode)
    #        self.header_buttons.display = True
    #        self.content.display = True
    #        self.input.value = ''
    #        
#
    #    
    #@on(Input.Changed)
    #def show_invalid_reasons(self, event: Input.Changed) -> None:
    #    if not event.validation_result.is_valid:
    #        self.invalidation_box.update(event.validation_result.failure_descriptions)
    #        self.invalidation_box.display = True
    #    else:
    #        self.invalidation_box.display = False
    #
    #def compose(self) -> ComposeResult:
    #    """Create the layout of the menu."""
    #    
    #    yield Header(show_clock=True)
    #    yield SwitchQuickConnectButtons()
    #    yield SwitchSelectDropdown()
    #    yield self.label
    #    yield self.mode_selector
    #    yield self.input
    #    yield self.invalidation_box
    #    yield Footer()
    #    yield self.header_buttons
    #    yield self.content
    #    yield self.footer_buttons
    #   
    #    
    #def _on_mount(self, event):
    #    
    #    return super()._on_mount(event)
    #
#
#class Show_Run_Screen(Command_Screen):
#
#    CSS = """
#    
#    """
#    
#    def __init__(self, label):
#        super().__init__(label)
#        self.input = Suggestion_Input(
#            suggestion_type='show_run',
#            value='show run', 
#            type='text',
#            validators=[
#            Function(contains_show_run, "Must begin with 'show'"),
#            Function(self.is_in_show_run_tree, 'Invalid Command'),
#            
#            ],
#        )           
#    def compose(self) -> ComposeResult:
#        """Create the layout of the menu."""
#        yield Header(show_clock=True)
#        yield self.label
#        yield self.input 
#        yield Footer()
#        yield HorizontalGroup(
#            Button('Close', id='exit'),
#            Button('Run Command', id='run'),
#            classes="footer-buttons",    
#        )
#
#    allowed_commands = {
#            'show' : {
#                'run' : {
#
#                }
#            }
#            
#        }
#    def is_in_show_run_tree(self, string):
#        strings = string.split()
#        depth = 0
#        while depth <= len(strings):
#            tree_dict = self.allowed_commands[strings[depth]]
#            if strings[depth] in tree_dict:
#                depth += 1
#                #finish this
#
#            else:
#                return False
#        return True
#        
#class Show_Run_Include_Screen(Command_Screen):
#    
#    def quit(self) -> None:
#        self.mount(self.app.switch_selector)
#    CSS = """
#    
#    """
#    
#    def __init__(self):
#        super().__init__(label='Show Run Include Screen')
#        self.input = Suggestion_Input(
#            suggestion_type='show_run_include',
#            placeholder='macro auto',
#            value='show run | include',
#            type='text',
#            validators= [
#                Function(contains_show_run, "Must begin with 'show'"),
#            ]
#        )
#        
#    async def on_valid_input_submit(self, input_string, selected_mode):
#        self.mount(self.content)
#        command = input_string
#        if 'show' not in input_string:
#           pass
#           #command = 'show run | include' + command
#        else:
#            await self.content.send_command_to_connected(command)
#        if self.mode == CommandMode.ALL_OUTPUTS.value:
#            await self.content.send_command_to_connected(command)
#        elif self.mode == CommandMode.DIFFERENCES.value:
#            await self.content.send_command_to_connected(command, 'DIFF')
#        elif self.mode == CommandMode.UNIQUE.value:
#            await self.content.send_command_to_connected(command, 'UNIQUE')
#        
#        
#        
    