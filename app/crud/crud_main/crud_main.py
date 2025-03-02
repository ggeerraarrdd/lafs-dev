"""
Database management module for SQLite operations.
"""

# Python Standard Library
import logging
from typing import Any, Dict, List

# Third-Part Libraries
from flask import g

# Local
from app.infra import DatabaseManager





# Set up logging for the database operations
logger = logging.getLogger(__name__)










def get_db():
    """
    Get or create DatabaseManager instance.
    """
    if 'db' not in g:
        db = DatabaseManager()
        g.db = db
    return g.db


def get_id_current_series() -> int:
    """
    Fetch the ID of the current film series.

    Returns:
        int: ID of the current film series.
    """
    query = '''
        SELECT
            series_id 
        FROM series 
        ORDER BY series_id 
        DESC LIMIT 1
        ;
    '''
    results_query = get_db().execute_read_query(query)

    if results_query:
        results = results_query[0]['series_id']
    else:
        results = None

    return results


def get_info_series(series_id: int) -> Dict[str, Any]:
    """
    Fetch information about a specific series.

    Args:
        series_id (int): ID of the series to fetch.

    Returns:
        Dict[str, Any]: Information about the series.
    """
    query = '''
        SELECT 
		    s.series_id,
            series_semester || series_year AS semester,
            series_semester,
            series_year,
            series_title,
            series_brief,
            series_poster,
            series_poster_url,
            series_display,
            color1,
            color2,
            color3
        FROM series s
        JOIN colors AS c ON s.series_id = c.series_id
        WHERE s.series_id = :series_id
        ;
    '''
    results_query = get_db().execute_read_query(query, {"series_id": series_id})

    if not results_query:
        return None

    results = results_query[0]
    if results['series_poster_url']:
        results['series_poster_url'] = f"{{ url_for('main_bp.static', filename=f'images/{results['series_poster_url']}') }}"

    return results


def get_info_schedules(series_id: int) -> List[Dict[str, Any]]:
    """
    Fetch information about the schedules of a specific series.

    Args:
        series_id (int): ID of the series to fetch schedules for.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing schedule information.
    
        rtrim (substr ('January  February March    April    May      June     July     August   SeptemberOctober  November December', strftime ('%m', schedule) * 9 - 8, 9)) AS month, "
    """
    query = '''
        SELECT 
            strftime('%d', schedule) AS day,
            f.id,
            rtrim (substr ('January  February March    April    May      June     July     August   SeptemberOctober  November December', strftime ('%m', schedule) * 9 - 8, 9)) AS month,
            film_title, 
            film_director, 
            film_year, 
            film_runtime, 
            wiki, 
            sc.schedule, 
            sc.notes
        FROM series AS se
        JOIN schedules AS sc ON se.series_id = sc.series_id
        JOIN films AS f ON sc.film_id = f.id
        WHERE se.series_id = :series_id
        ;
    '''
    results = get_db().execute_read_query(query, {"series_id": series_id})

    return results


def get_info_series_ids() -> List[Dict[str, Any]]:
    """
    Fetch information of all series IDs.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing series ID information.
    """
    query = '''
        SELECT 
	        DISTINCT(series_id), 
            series_semester, 
            series_year, 
            series_display 
        FROM series
        ;
    '''
    results = get_db().execute_read_query(query)

    return results


def get_info_film(film_id: int) -> Dict[str, Any]:
    """
    Fetch information about a specific film.

    Args:
        film_id (int): ID of the film to fetch.

    Returns:
        Dict[str, Any]: Information about the film.
    """
    query = '''
        SELECT
            *
        FROM films
        WHERE id = :id
        ;
    '''
    results_query = get_db().execute_read_query(query, {"id": film_id})

    if results_query:
        results = dict(results_query[0])
    else:
        # TD: If none, return a default page
        results = None

    return results
