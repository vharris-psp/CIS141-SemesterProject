from flask import Blueprint, render_template
from backend.Blueprints.DefaultPage import DefaultPage


class SettingsPage(DefaultPage):
    header_buttons = []
    footer_buttons = [] 
    content = None  # Placeholder for content
    
    blueprint = Blueprint('settings', __name__, template_folder='../../frontend/templates', static_folder='../../frontend/static')
    @blueprint.route('/settings')
    def settings():
        return render_template('settings.html', header_buttons=SettingsPage.header_buttons, footer_buttons=SettingsPage.footer_buttons, content=SettingsPage.content)
        


    

