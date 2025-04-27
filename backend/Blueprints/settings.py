from flask import Blueprint, render_template

settings_bp = Blueprint('settings', __name__, template_folder='../../frontend/templates', static_folder='../../frontend/static')

@settings_bp.route('/settings')
def settings():
    return render_template('settings.html')