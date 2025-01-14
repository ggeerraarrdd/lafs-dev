# Third-Party Libraries
from flask import Flask
from flask_session import Session

# Local Libraries
from blueprints.main import main
from blueprints.cms import cms




# Configure application
app = Flask(__name__)

app.register_blueprint(main)
app.register_blueprint(cms)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)
