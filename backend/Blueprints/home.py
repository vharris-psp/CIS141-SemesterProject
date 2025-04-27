from flask import Blueprint, render_template

home_bp = Blueprint('home', __name__, template_folder='../../frontend/templates', static_folder='../../frontend/static')
@home_bp.route('/')
def index():
    return render_template('index.html')
@home_bp.route('/home')
def home():
    return render_template('index.html')
