"""
TD
"""

from .crud_main import get_id_current_series
from .crud_main import get_info_series
from .crud_main import get_info_schedules
from .crud_main import get_info_series_ids
from .crud_main import get_info_film


# Define what should be available when using "from .crud import *"
__all__ = ['get_id_current_series',
           'get_info_series',
           'get_info_schedules',
           'get_info_series_ids',
           'get_info_film',
           ]
