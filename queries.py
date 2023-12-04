import sqlite3


def get_id_current_series(db):
    """Get id of current film series."""

    # Create connection and cursor
    connection = sqlite3.connect(db, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    # Query db
    query = "SELECT series_id FROM series ORDER BY series_id DESC LIMIT 1;"
    cursor.execute(query)
    current_series_id = cursor.fetchone()
    
    # Close cursor and connection
    cursor.close()
    connection.close()

    return(current_series_id)


def get_info_series(db, series_id):
    """Get info of series."""

    # Create connection and cursor
    connection = sqlite3.connect(db, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    # Query db
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
    query = query + "LEFT JOIN colors AS c ON s.series_id = c.series_id "
    query = query + "WHERE s.series_id = ?; "
    cursor.execute(query, (series_id,))
    results = cursor.fetchone()

    # Close cursor and connection
    cursor.close()
    connection.close()

    return(results)


def get_info_schedules(db, series_id):
    """Get info of series schedules."""

    # Create connection and cursor
    connection = sqlite3.connect(db, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    # Query db
    query = "SELECT strftime('%d', schedule) AS day, "
    query = query + "f.id, "
    query = query + "rtrim (substr ('January  February March    April    May      June     July     August   SeptemberOctober  November December', strftime ('%m', schedule) * 9 - 8, 9)) AS month, "
    query = query + "film_title, film_director, film_year, film_runtime, wiki, sc.schedule, sc.note "
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

    # Close cursor and connection
    cursor.close()
    connection.close()

    return(result)


def get_info_series_ids(db):
    """Get info of series ids."""

    # Create connection and cursor
    connection = sqlite3.connect(db, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    # Query db
    query = "SELECT DISTINCT(series_id), series_semester, series_year, series_display "
    query = query + "FROM series; "
    cursor.execute(query)

    # Get rows
    rows = cursor.fetchall()

    # Get the column names from cursor.description
    columns = [column[0] for column in cursor.description]

    # Convert each row into a dictionary using zip
    result = [dict(zip(columns, row)) for row in rows]

    return(result)


def get_info_serieses(db):
    """Get info of series ids."""

    # Create connection and cursor
    connection = sqlite3.connect(db, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    # Query db
    query = "SELECT "
    query = query + "s.series_id "
    query = query + ",series_semester || series_year AS semester "
    query = query + ",series_semester AS series_semester "
    query = query + ",series_year AS series_year "
    query = query + ",series_title "
    query = query + ",series_brief "
    query = query + ",series_poster_url "
    query = query + ",series_display "
    query = query + ",bgcolor1 AS color_1 "
    query = query + ",bgcolor2 AS color_2 "
    query = query + ",text_color3 AS color_3 "
    query = query + ",min(sc.schedule) AS min_date "
    query = query + ",max(sc.schedule) AS max_date "
    query = query + ",max(date(substr(sc.schedule, 1, 4) || '-' || substr(sc.schedule, 6, 2) || '-' || substr(sc.schedule, 9, 2))) < current_timestamp AS status "
    query = query + "FROM series s "
    query = query + "LEFT JOIN schedules sc ON s.series_id = sc.series_id "
    query = query + "LEFT JOIN colors AS c ON s.series_id = c.series_id "
    query = query + "GROUP BY s.series_id "
    cursor.execute(query)

    # Get rows
    rows = cursor.fetchall()

    # Get the column names from cursor.description
    columns = [column[0] for column in cursor.description]

    # Convert each row into a dictionary using zip
    result = [dict(zip(columns, row)) for row in rows]

    return(result)


def get_info_film(db, film_id):
    """Get info of film."""

    # Create connection and cursor
    connection = sqlite3.connect(db, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    # Query db
    query = "SELECT * "
    query = query + "FROM films "
    query = query + "WHERE id = ?; "
    cursor.execute(query, (film_id,))

    # Get row
    row = cursor.fetchone()

    # Convert row into a dictionary
    result = dict(row)

    return(result)


def get_info_series_status(db, series_id):

    # Create connection and cursor
    connection = sqlite3.connect(db, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    query = "SELECT "
    query = query + "max(date(substr(schedule, 1, 4) || '-' || substr(schedule, 6, 2) || '-' || substr(schedule, 9, 2))) < current_timestamp AS status "
    query = query + "FROM schedules WHERE series_id = ?; "
    cursor.execute(query, series_id)

    series_status = cursor.fetchone()

    # print(len(series_status))
    return(series_status)


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
    query = query + "sc.schedule, "
    query = query + "sc.note "
    query = query + "FROM series AS se "
    query = query + "JOIN schedules AS sc ON se.series_id = sc.series_id "
    query = query + "JOIN films AS f ON sc.film_id = f.id "
    query = query + "WHERE se.series_id = ? "
    query = query + "AND sc.schedule >= DATE('now') "
    query = query + "ORDER BY schedule "
    query = query + "LIMIT 1; "
    cursor.execute(query, (series_id,))

    cms_next = cursor.fetchone()

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

    return(cms_films)


def get_info_cms_schedules(db, series_id):

    # Create connection and cursor
    connection = sqlite3.connect(db, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    query = "SELECT  "
    query = query + "s.series_id "
    query = query + ",sc.schedule  "
    query = query + ",sc.film_id "
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

    return(cms_schedules)


def get_info_users(db):

    # Create connection and cursor
    connection = sqlite3.connect(db, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    query = "SELECT * FROM users ORDER BY name_first; "
    cursor.execute(query)

    results = cursor.fetchall()

    return(results)


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