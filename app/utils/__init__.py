"""
TD
"""

from .utils_cms import get_dicts
from .utils_cms import get_query
from .utils_cms import get_dicts_updates
from .utils_cms import get_query_update_series
from .utils_cms import get_query_update_schedules
from .utils_shared import login_required
from .utils_shared import apology


# Define what should be available when using "from .utils import *"
__all__ = ['login_required',
           'apology',
           ]
