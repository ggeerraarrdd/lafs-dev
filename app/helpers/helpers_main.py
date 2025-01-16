# Python Standard Library
from typing import Tuple, List, Dict

# Local Libraries
import crud










def get_series_data(db: str, series_id: int) -> Tuple[Dict, List, List]:
    """Helper function to fetch series data from database.
    
    Args:
        db (str): Name of the database to query.
        series_id (int): ID of the series to fetch.

    Returns:
        Tuple[Dict, List, List]: A tuple containing:
            - series (Dict): Information about the series.
            - schedules (List): List of schedules for the series.
            - series_ids (List): List of all series IDs.
    """
    series = crud.get_info_series(db, series_id)
    schedules = crud.get_info_schedules(db, series_id)
    series_ids = crud.get_info_series_ids(db)

    return series, schedules, series_ids
