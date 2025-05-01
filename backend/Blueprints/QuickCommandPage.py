from flask import Blueprint, render_template
from backend.Blueprints.DefaultPage import DefaultPage
from backend.Blueprints.Widgets.CustomWidgets import ConnectionSelector
from backend.Blueprints.Widgets.Buttons import HeaderButton, FooterButton
class QuickCommandsPage(DefaultPage):
    """Quick Commands page class for the web application."""
    label = "Quick Commands Page"
    header_buttons = []
    footer_buttons = []
    #content = ConnectionSelector(id="outputs", children=[FooterButton(id='footer-button1', label='1')])  # Placeholder for content

    # Define the blueprint for the quick commands page
    blueprint = Blueprint('quick_commands', __name__, template_folder='../../frontend/templates', static_folder='../../frontend/static')

    def __init__(self):
        super().__init__(name='quick_commands')
        

        
    
        @self.route('/quick_commands_page')
        def quick_commands_page():
            page = QuickCommandsPage()
            content = page.get_content()
            return render_template('quick_commands.html', header_buttons=QuickCommandsPage.header_buttons, footer_buttons=QuickCommandsPage.footer_buttons, content=content)

   