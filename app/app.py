"""
TD
"""

# Python Standard Library
import os

# Third-Party Libraries
from flask import Flask
from flask_session import Session

# Local
from app.blueprints.main.routes import main_bp
from app.blueprints.cms.routes import cms_bp










# Configure application
app = Flask(__name__)

# Set secret key for session management
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Disable file caching and enable template auto-reloading
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

# Initialize session with the app
Session(app)

# Register blueprints for main and cms routes
app.register_blueprint(main_bp)
app.register_blueprint(cms_bp)
