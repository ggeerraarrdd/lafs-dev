# Python Standard Library
import sqlite3
from typing import Dict, Any, List

# Local
from helpers import DatabaseConnection










def get_id_current_series(db: str) -> int:
    """
    Fetch the ID of the current film series.

    Args:
        db (str): Name of the database to query.

    Returns:
        int: ID of the current film series.
    """
    with DatabaseConnection(db) as cursor:
        query = "SELECT series_id FROM series ORDER BY series_id DESC LIMIT 1;"
        cursor.execute(query)
        
        current_series_id = cursor.fetchone()

    return current_series_id


def get_info_series(db: str, series_id: int) -> Dict[str, Any]:
    """
    Fetch information about a specific series.

    Args:
        db (str): Name of the database to query.
        series_id (int): ID of the series to fetch.

    Returns:
        Dict[str, Any]: Information about the series.
    """
    with DatabaseConnection(db) as cursor:
        query = "SELECT s.series_id, "
        query = query + "series_semester || series_year AS semester, "
        query = query + "series_semester, "
        query = query + "series_year, "
        query = query + "series_title, "
        query = query + "series_brief, "
        query = query + "series_poster, "
        query = query + "series_poster_url, "
        query = query + "series_display, "
        query = query + "color1, "
        query = query + "color2, "
        query = query + "color3 "
        query = query + "FROM series s "
        query = query + "JOIN colors AS c ON s.series_id = c.series_id "
        query = query + "WHERE s.series_id = ?; "
        cursor.execute(query, (series_id,))
        
        results = cursor.fetchone()

    # Construct the full URL for the series poster
    results = dict(results)
    if results['series_poster_url']:
        results['series_poster_url'] = f"{{ url_for('main_bp.static', filename=f'images/{results['series_poster_url']}')  }}"

    return results


def get_info_schedules(db: str, series_id: int) -> List[Dict[str, Any]]:
    """
    Fetch information about the schedules of a specific series.

    Args:
        db (str): Name of the database to query.
        series_id (int): ID of the series to fetch schedules for.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing schedule information.
    """
    with DatabaseConnection(db) as cursor:
        query = "SELECT strftime('%d', schedule) AS day, "
        query = query + "f.id, "
        query = query + "rtrim (substr ('January  February March    April    May      June     July     August   SeptemberOctober  November December', strftime ('%m', schedule) * 9 - 8, 9)) AS month, "
        query = query + "film_title, film_director, film_year, film_runtime, wiki, sc.schedule, sc.notes "
        query = query + "FROM series AS se "
        query = query + "JOIN schedules AS sc ON se.series_id = sc.series_id "
        query = query + "JOIN films AS f ON sc.film_id = f.id "
        query = query + "WHERE se.series_id = ?; "
        cursor.execute(query, (series_id,))

        # Get rows
        rows = cursor.fetchall()

        # Get the column names from cursor.description
        columns = [column[0] for column in cursor.description]

    # Convert each row into a dictionary using zip
    result = [dict(zip(columns, row)) for row in rows]

    return result


def get_info_series_ids(db: str) -> List[Dict[str, Any]]:
    """
    Fetch information of all series IDs.

    Args:
        db (str): Name of the database to query.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing series ID information.
    """
    with DatabaseConnection(db) as cursor:
        query = "SELECT DISTINCT(series_id), series_semester, series_year, series_display FROM series; "
        cursor.execute(query)

        # Get rows
        rows = cursor.fetchall()

        # Get the column names from cursor.description
        columns = [column[0] for column in cursor.description]

    # Convert each row into a dictionary using zip
    result = [dict(zip(columns, row)) for row in rows]

    return result


def get_info_serieses(db: str) -> List[Dict[str, Any]]:
    """
    Fetch information of all series IDs.

    Args:
        db (str): Name of the database to query.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing series ID information.
    """
    with DatabaseConnection(db) as cursor:
        query = "SELECT DISTINCT(series_id), "
        query = query + "series_semester, "
        query = query + "series_year, "
        query = query + "series_display " 
        query = query + "FROM series; "
        cursor.execute(query)

        # Get rows
        rows = cursor.fetchall()

        # Get the column names from cursor.description
        columns = [column[0] for column in cursor.description]

    # Convert each row into a dictionary using zip
    result = [dict(zip(columns, row)) for row in rows]

    return result


def get_info_film(db: str, film_id: int) -> Dict[str, Any]:
    """
    Fetch information about a specific film.

    Args:
        db (str): Name of the database to query.
        film_id (int): ID of the film to fetch.

    Returns:
        Dict[str, Any]: Information about the film.
    """
    with DatabaseConnection(db) as cursor:
        query = "SELECT * "
        query = query + "FROM films "
        query = query + "WHERE id = ?; "
        cursor.execute(query, (film_id,))

        # Get row
        row = cursor.fetchone()

    # Convert row into a dictionary
    result = dict(row)

    return result


def get_info_series_status(db, series_id):

    with DatabaseConnection(db) as cursor:

        query = "SELECT "
        query = query + "max(date(substr(schedule, 1, 4) || '-' || substr(schedule, 6, 2) || '-' || substr(schedule, 9, 2))) < current_timestamp AS status "
        query = query + "FROM schedules WHERE series_id = ?; "
        cursor.execute(query, series_id)

        series_status = cursor.fetchone()

    return series_status
