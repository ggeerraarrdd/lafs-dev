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


def get_info_cms_next_film(series_id: int) -> Dict[str, Any]:
    """
    Retrieves information about the next scheduled film in a series.
    
    Args:
        db_path (str): Path to SQLite database file
        series_id (int): ID of the series to query
        
    Returns:
        Dict containing next film's information with keys:
        - id: int
        - film_title: str 
        - film_director: str
        - film_year: int
        - film_runtime: int
        - wiki: str
        - schedule_id: int
        - schedule: str
        - notes: str
        
    Raises:
        sqlite3.Error: If database operation fails
    """
    query = "SELECT "
    query = query + "f.id, "
    query = query + "film_title, "
    query = query + "film_director, "
    query = query + "film_year, "
    query = query + "film_runtime, "
    query = query + "wiki, "
    query = query + "sc.schedule_id, "
    query = query + "sc.schedule, "
    query = query + "sc.notes "
    query = query + "FROM series AS se "
    query = query + "JOIN schedules AS sc ON se.series_id = sc.series_id "
    query = query + "JOIN films AS f ON sc.film_id = f.id "
    query = query + "WHERE se.series_id = :series_id "
    query = query + "AND sc.schedule >= DATE('now') "
    query = query + "ORDER BY schedule "
    query = query + "LIMIT 1; "

    results_query = get_db().execute_read_query(query, {"series_id": series_id})

    return results_query


def get_info_cms_films() -> List[Dict[str, Any]]:
    """
    Retrieves information about all films in the database.
    
    Args:
        db_path (str): Path to SQLite database file
        
    Returns:
        List of dictionaries containing film information with keys:
        - id: int
        - film_title: str
        - film_director: str
        - film_year: int
        - film_runtime: int
        - film_description: str
        - wiki: str
        - imdb: str
        - film_poster: str
        - entry_created: str
        - entry_updated: str
        - series: str
        
    Raises:
        sqlite3.Error: If database operation fails
    """
    query = "SELECT "
    query = query + "f.id "
    query = query + ", f.film_title "
    query = query + ", f.film_director "
    query = query + ", f.film_year "
    query = query + ", f.film_runtime "
    query = query + ", f.film_description "
    query = query + ", f.wiki, imdb "
    query = query + ", f.film_poster "
    query = query + ", date(f.entry_created) AS entry_created "
    query = query + ", date(f.entry_updated) AS entry_updated "
    query = query + ", group_concat(s.series_id, ', ') AS series "
    query = query + "FROM films f "
    query = query + "JOIN schedules s ON f.id = s.film_id "
    query = query + "GROUP BY f.id "
    query = query + "ORDER BY film_title ASC; "

    return get_db().execute_read_query(query)


def get_info_cms_schedules(series_id: int) -> List[Dict[str, Any]]:
    """
    Retrieves schedule information for a specific series.
    
    Args:
        db_path (str): Path to SQLite database file
        series_id (int): ID of the series to query
        
    Returns:
        List of dictionaries containing schedule information with keys:
        - series_id: int
        - schedule_id: int
        - schedule: str
        - film_id: int
        - notes: str
        - film_title: str
        - film_director: str
        - film_year: int
        - film_runtime: int
        - film_description: str
        - wiki: str
        - imdb: str
        - film_poster: str
        
    Raises:
        sqlite3.Error: If database operation fails
    """
    query = "SELECT  "
    query = query + "s.series_id "
    query = query + ",sc.schedule_id "
    query = query + ",sc.schedule  "
    query = query + ",sc.film_id "
    query = query + ",sc.notes"
    query = query + ",f.film_title "
    query = query + ",f.film_director "
    query = query + ",f.film_year "
    query = query + ",f.film_runtime "
    query = query + ",f.film_description "
    query = query + ",f.wiki "
    query = query + ",f.imdb "
    query = query + ",f.film_poster "
    query = query + "FROM series s "
    query = query + "JOIN schedules sc ON s.series_id = sc.series_id "
    query = query + "JOIN films f ON sc.film_id = f.id "
    query = query + "JOIN colors AS c ON s.series_id = c.series_id "
    query = query + "WHERE s.series_id = :series_id "
    query = query + "ORDER BY sc.schedule ASC; "

    return get_db().execute_read_query(query, {"series_id": series_id})


def get_info_users() -> List[Dict[str, Any]]:
    """
    Retrieves information about all users.
    
    Args:
        db_path (str): Path to SQLite database file
        
    Returns:
        List of dictionaries containing user information with keys:
        - user_id: int
        - name_first: str
        - name_last: str
        - username: str
        - role: str
        - status: str
        - hash: str
        - date_created: str
        - date_updated: str
        
    Raises:
        sqlite3.Error: If database operation fails
    """
    query = "SELECT * FROM users ORDER BY name_first; "

    return get_db().execute_read_query(query)


def get_info_user(user_id: int) -> Dict[str, Any]:
    """
    Retrieves information about a specific user.
    
    Args:
        db_path (str): Path to SQLite database file
        user_id (int): ID of the user to query
        
    Returns:
        Dictionary containing user information with keys:
        - user_id: int
        - name_first: str
        - name_last: str
        - username: str
        - role: str
        - status: str
        - hash: str
        - date_created: str
        - date_updated: str
        
    Raises:
        sqlite3.Error: If database operation fails
    """
    query = "SELECT * FROM users WHERE user_id = :user_id; "

    return get_db().execute_read_query(query, {"user_id": user_id})


def update_user_info(name_first: str, name_last: str, username: str, role: str, user_id: int) -> int:
    """
    Updates information for a specific user.
    
    Args:
        db_path (str): Path to SQLite database file
        name_first (str): User's first name
        name_last (str): User's last name
        username (str): User's username
        role (str): User's role
        user_id (int): ID of the user to update
        
    Returns:
        1 if successful, 0 if failed
        
    Raises:
        sqlite3.Error: If database operation fails
    """
    query = "UPDATE users SET "
    query = query + "name_first = :name_first, "
    query = query + "name_last = :name_last, "
    query = query + "username = (username, "
    query = query + "role = :role, "
    query = query + "date_updated = datetime('now') "
    query = query + "WHERE user_id = :user_id; "

    return get_db().execute_write_query(query, {"name_first": name_first, "name_last": name_last, "username": username, "role": role, "user_id": user_id})


def update_user_status(status: str, user_id: int) -> int:
    """
    Updates the status of a specific user.
    
    Args:
        db_path (str): Path to SQLite database file
        status (str): New status value
        user_id (int): ID of the user to update
        
    Returns:
        1 if successful, 0 if failed
        
    Raises:
        sqlite3.Error: If database operation fails
    """
    query = "UPDATE users SET "
    query = query + "status = :status, "
    query = query + "date_updated = datetime('now') "
    query = query + "WHERE user_id = :user_id; "

    return get_db().execute_write_query(query, {"status": status, "user_id": user_id})


def update_user_hash(user_hash: str, user_id: int) -> int:
    """
    Updates the hash value for a specific user.
    
    Args:
        db_path (str): Path to SQLite database file
        user_hash (str): New hash value
        user_id (int): ID of the user to update
        
    Returns:
        1 if successful, 0 if failed
        
    Raises:
        sqlite3.Error: If database operation fails
    """
    query = "UPDATE users SET "
    query = query + "hash = :user_hash, "
    query = query + "date_updated = datetime('now') "
    query = query + "WHERE user_id = :user_id; "

    return get_db().execute_write_query(query, {"hash": user_hash, "user_id": user_id})


def delete_user(user_id: int) -> int:
    """
    Deletes a specific user from the database.
    
    Args:
        db_path (str): Path to SQLite database file
        user_id (int): ID of the user to delete
        
    Returns:
        1 if successful, 0 if failed
        
    Raises:
        sqlite3.Error: If database operation fails
    """
    query = "DELETE FROM users "
    query = query + "WHERE user_id = :user_id; "

    return get_db().execute_write_query(query, {"user_id": user_id})


def insert_new_series(query: str) -> int:
    """
    Inserts a new series into the database.
    
    Args:
        db_path (str): Path to SQLite database file
        query (str): SQL query string for insertion
        
    Returns:
        ID of the newly inserted series if successful, 0 if failed
        
    Raises:
        sqlite3.Error: If database operation fails
    """
    query = "SELECT series_id FROM series WHERE rowid = :rowid; "

    return get_db().execute_read_query(query, {"rowid": query})


def insert_new_records(query: str) -> int:
    """
    Inserts new records into the database.
    
    Args:
        db_path (str): Path to SQLite database file
        query (str): SQL query string for insertion
        
    Returns:
        1 if successful, 0 if failed
        
    Raises:
        sqlite3.Error: If database operation fails
    """
    return get_db().execute_write_query(query)


def update_records(query: str) -> int:
    """
    Updates existing records in the database.
    
    Args:
        db_path (str): Path to SQLite database file
        query (str): SQL query string for update
        
    Returns:
        1 if successful, 0 if failed
        
    Raises:
        sqlite3.Error: If database operation fails
    """
    return get_db().execute_write_query(query)


# CMS only
def get_info_serieses() -> List[Dict[str, Any]]:
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
    results_query = get_db().execute_read_query(query)

    results_final = []
    if results_query:
        for row in results_query:
            results_final.append(dict(row))

    print(results_query == results_final)

    return results_final


# CMS only
def get_info_series_status(series_id: int) -> bool:
    """
    Check if a series is completed based on schedule dates.

    Args:
        series_id (int): ID of the series to check.
    
    Returns:
        bool: True if series is completed, False otherwise.
    """
    query = '''
        SELECT 
            max(date(substr(schedule, 1, 4) || '-' || substr(schedule, 6, 2) || '-' || substr(schedule, 9, 2))) < current_timestamp AS status
        FROM schedules 
        WHERE series_id = ?
        ;
    '''
    results_query = get_db().execute_read_query(query, (series_id,))

    if results_query:
        results_final = bool(results_query[0]['status'])
    else:
        results_final = False

    return results_final
