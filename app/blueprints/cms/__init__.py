# Third-Party Libraries
from flask import Blueprint










cms_bp = Blueprint('cms_bp', 
                    __name__,
                    static_folder='static', 
                    static_url_path='/cms/static',
                    template_folder='templates')

from . import routes
