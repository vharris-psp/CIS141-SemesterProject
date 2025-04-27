from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS

from backend.Blueprints.home import home_bp
from backend.Blueprints.settings import settings_bp
from backend.Blueprints.command_page import commands_bp    
from backend.Blueprints.quick_commands import quick_commands_bp
# Set up Flask with correct folders
app = Flask(__name__, 
            static_folder='../frontend/static', 
            template_folder='../frontend/templates')
CORS(app)

CORS(app, resources={r"/*": {"origins": "*"}})


# Register blueprints
app.register_blueprint(home_bp)
app.register_blueprint(settings_bp)
app.register_blueprint(commands_bp)
app.register_blueprint(quick_commands_bp)
# Define the command runner function



# API route to run a command
@app.route('/send_command', methods=['POST'])
def send_command_route():    
    data = request.get_json()

    host = data.get('host')
    user = data.get('user')
    password = data.get('password')
    command = data.get('command')

    if not all([host, user, password, command]):
        return jsonify({'error': 'Missing required parameters'}), 400

    output = send_command_route(host, user, password, command)
    
    return jsonify({'output': output})

# Simple test API
@app.route('/test_api', methods=['GET'])
def test_api():
    return jsonify({'message': 'API is working'}), 200

# Serve any additional static files (optional)
@app.route('/frontend/static/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    app.run(debug=True)