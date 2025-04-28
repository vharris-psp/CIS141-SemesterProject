from flask import Blueprint, render_template
from backend.Blueprints.DefaultPage import DefaultPage
from backend.Blueprints.Widgets.CustomWidgets import CommandOutputWidget, SettingsViewer
from backend.Blueprints.Widgets.Buttons import HeaderButton
class SettingsPage(DefaultPage):
    
    header_buttons = []
    footer_buttons = [] 
    content = None  # Placeholder for content
    label = "Settings Page"
    content = SettingsViewer(id='settings_content')  # Placeholder for content
    def __init__(self, label):
        super().__init__(label)
    
    blueprint = Blueprint('settings', __name__, template_folder='../../frontend/templates', static_folder='../../frontend/static')
    @blueprint.route('/settings')
    def settings():
        return render_template('settings.html', header_buttons=SettingsPage.header_buttons, footer_buttons=SettingsPage.footer_buttons, content=SettingsPage.content)
    
    @blueprint.route('/label')
    def label(self):
        return self.label


    

