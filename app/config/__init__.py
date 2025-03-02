"""
Configuration module for LAFS application.

This module imports and re-exports all configuration settings from:

config_db.py:
    Database configuration including connection pool settings and retry mechanism.
    Loads settings from environment variables with fallback defaults for:
    - Database location
    - Connection pool parameters (size, overflow, timeout, recycling)
    - Operation retry settings

config_map.py:
    Google Maps API configuration and key management.
    Loads the Google Maps API key from environment variables for:
    - Static map image generation
"""

from .config_db import DATABASE_NAME
from .config_db import POOL_SIZE
from .config_db import MAX_OVERFLOW
from .config_db import POOL_TIMEOUT
from .config_db import POOL_RECYCLE
from .config_db import ECHO
from .config_db import MAX_RETRIES
from .config_db import BASE_DELAY
from .config_db import MAX_DELAY
from .config_map import MAP_API_KEY


# Define what should be available when using "from .config import *"
__all__ = ['DATABASE_NAME',
           'POOL_SIZE',
           'MAX_OVERFLOW',
           'POOL_TIMEOUT',
           'POOL_RECYCLE',
           'ECHO',
           'MAX_RETRIES',
           'BASE_DELAY',
           'MAX_DELAY',
           'MAP_API_KEY'
]
