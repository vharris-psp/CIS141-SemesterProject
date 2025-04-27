from flask import Blueprint, render_template

quick_commands_bp = Blueprint('quick_commands', __name__, template_folder='../../frontend/templates', static_folder='../../frontend/static')

@quick_commands_bp.route('/quick_commands_page')
def quick_commands_page():
    return render_template('quick_commands.html')

   