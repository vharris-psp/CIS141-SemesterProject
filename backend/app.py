from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
from command_runner import run_command
import os

# Set up Flask with correct folders
app = Flask(__name__, 
            static_folder='../frontend/static', 
            template_folder='../frontend/templates')
CORS(app)

# Route to serve your index.html from templates
@app.route('/')
def serve_index():
    return render_template('index.html')

# API route to run a command
@app.route('/run_command', methods=['POST'])
def run_command_route():
    data = request.get_json()

    host = data.get('host')
    user = data.get('user')
    password = data.get('password')
    command = data.get('command')

    if not all([host, user, password, command]):
        return jsonify({'error': 'Missing required parameters'}), 400

    output = run_command(host, user, password, command)
    
    return jsonify({'output': output})

# Simple test API
@app.route('/test_api', methods=['GET'])
def test_api():
    return jsonify({'message': 'API is working'}), 200

# Serve any additional static files (optional)
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    app.run(debug=True)