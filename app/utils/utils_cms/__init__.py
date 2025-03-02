"""
TD
"""

from .utils_dicts import get_dicts
from .utils_dicts import get_query
from .utils_dicts import get_dicts_updates
from .utils_dicts import get_query_update_series
from .utils_dicts import get_query_update_schedules


# Define what should be available when using "from .utils_shared import *"
__all__ = ['get_dicts',
           'get_query',
           'get_dicts_updates',
           'get_query_update_series',
           'get_query_update_schedules',
           ]
