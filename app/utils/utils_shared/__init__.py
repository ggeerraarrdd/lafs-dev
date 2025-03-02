"""
TD
"""

from .utils_shared import login_required
from .utils_shared import apology


# Define what should be available when using "from .utils_shared import *"
__all__ = ['login_required',
           'apology',
           ]
