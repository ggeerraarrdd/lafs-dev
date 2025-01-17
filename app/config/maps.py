import os
from .config import PRODUCTION









if PRODUCTION:
    MAP_API_KEY = os.getenv("MAP_API_KEY_PROD")
else:
    MAP_API_KEY = os.getenv("MAP_API_KEY_DEV")
