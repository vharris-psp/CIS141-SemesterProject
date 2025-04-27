from flask import Blueprint, render_template

commands_bp = Blueprint('commands', __name__, template_folder='../../frontend/templates', static_folder='../../frontend/static')

@commands_bp.route('/command_page')
def command_page():
    return render_template('command_page.html')

@commands_bp.route('/run_command')
def run_command():
    # Logic for running commands
    return render_template('run_command.html')