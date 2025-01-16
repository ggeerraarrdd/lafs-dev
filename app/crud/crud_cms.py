# Python Standard Library
import sqlite3
from typing import Dict, Any, List










def get_info_cms_next_film(db, series_id):

    # Create connection and cursor
    connection = sqlite3.connect(db, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

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
    query = query + "WHERE se.series_id = ? "
    query = query + "AND sc.schedule >= DATE('now') "
    query = query + "ORDER BY schedule "
    query = query + "LIMIT 1; "
    cursor.execute(query, (series_id,))

    cms_next = cursor.fetchone()

    connection.close()

    return(cms_next)


def get_info_cms_films(db):

    # Create connection and cursor
    connection = sqlite3.connect(db, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

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
    cursor.execute(query)

    cms_films = cursor.fetchall()

    connection.close()

    return(cms_films)


def get_info_cms_schedules(db, series_id):

    # Create connection and cursor
    connection = sqlite3.connect(db, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

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
    query = query + "WHERE s.series_id = ? "
    query = query + "ORDER BY sc.schedule ASC; "
    cursor.execute(query, (series_id,))

    cms_schedules = cursor.fetchall()

    connection.close()

    return(cms_schedules)


def get_info_users(db):

    # Create connection and cursor
    connection = sqlite3.connect(db, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    query = "SELECT * FROM users ORDER BY name_first; "
    cursor.execute(query)

    results = cursor.fetchall()

    connection.close()

    return(results)


def get_info_user(db, user_id):

    # Create connection and cursor
    connection = sqlite3.connect(db, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    query = "SELECT * FROM users WHERE user_id = ?; "
    cursor.execute(query, (user_id,))

    results = cursor.fetchone()

    connection.close()

    return(results)


def update_user_info(db, name_first, name_last, username, role, user_id):

    # Create connection and cursor
    connection = sqlite3.connect(db, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    query = "UPDATE users SET "
    query = query + "name_first = ?, "
    query = query + "name_last = ?, "
    query = query + "username = ?, "
    query = query + "role = ?, "
    query = query + "date_updated = datetime('now') "
    query = query + "WHERE user_id = ?; "
    cursor.execute(query, (name_first, name_last, username, role, user_id,))

    connection.commit()

    connection.close()

    return 1


def update_user_status(db, status, user_id):

    # Create connection and cursor
    connection = sqlite3.connect(db, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    query = "UPDATE users SET "
    query = query + "status = ?, "
    query = query + "date_updated = datetime('now') "
    query = query + "WHERE user_id = ?; "
    cursor.execute(query, (status, user_id,))

    connection.commit()

    connection.close()

    return 1


def update_user_hash(db, hash, user_id):

    # Create connection and cursor
    connection = sqlite3.connect(db, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    query = "UPDATE users SET "
    query = query + "hash = ?, "
    query = query + "date_updated = datetime('now') "
    query = query + "WHERE user_id = ?; "
    cursor.execute(query, (hash, user_id,))

    connection.commit()

    connection.close()

    return 1


def delete_user(db, user_id):

    # Create connection and cursor
    connection = sqlite3.connect(db, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    query = "DELETE FROM users "
    query = query + "WHERE user_id = ?; "
    cursor.execute(query, (user_id,))

    connection.commit()

    connection.close()

    return 1


def insert_new_series(db, query):

    # Create connection and cursor
    connection = sqlite3.connect(db, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(query)

    connection.commit()

    query = "SELECT series_id FROM series WHERE rowid = ?"
    cursor.execute(query, (cursor.lastrowid,))

    new_series_id = cursor.fetchone()[0]

    connection.close()

    return(new_series_id)


def insert_new_records(db, query):

    # Create connection and cursor
    connection = sqlite3.connect(db, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(query)

    connection.commit()

    return 1


def update_records(db, query):

    # Create connection and cursor
    connection = sqlite3.connect(db, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(query)

    connection.commit()

    connection.close()

    return 1
