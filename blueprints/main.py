# Python Standard Library
import os

# Third-Party Libraries
from flask import Blueprint, redirect, render_template, request, session

# Local Libraries
from helpers import get_series_data
import queries 




main = Blueprint('main', __name__)

# Set constants
MAP_API_KEY = os.environ.get("MAP_API_KEY")
DATABASE_NAME = os.environ.get("DATABASE_NAME")


@main.route("/", methods=["GET", "POST"])
def index():
    """
    Handle the index route for the application.

    For GET requests:
    - Retrieve the current series ID from the database.
    - Update the session with the current series ID.
    - For development purposes, set the current series ID to 1.
    - Retrieve series data, schedules, and series IDs from the database.
    - Render the index.html template with the retrieved data.

    For POST requests:
    - Redirect to the index route.

    Returns:
        Response: Flask response object containing a rendered HTML template or a redirect.
    """
    if request.method == "POST":
        return redirect("/")

    # Get info of [current] series id
    query_result = queries.get_id_current_series(DATABASE_NAME)

    # Update session
    session["active_series_id"] = session["current_series_id"] = query_result[0]

    # NOTE: For development purposes, change current_series_id to first series, not actual current
    session["active_series_id"] = session["current_series_id"] = 1

    # Update function variable series_id
    series_id = session["active_series_id"]

    # Get info on [past] (1) series, (2) schedules, and (3) series ids
    series, schedules, series_ids = get_series_data(DATABASE_NAME, series_id)

    return render_template("index.html",
                            series=series,
                            schedules=schedules,
                            series_ids=series_ids)


@main.route("/series", methods=["GET", "POST"])
def series_view():
    """
    Handle the series view route for the application.

    For GET requests:
    - Redirect to the index route.

    For POST requests:
    - Retrieve the clicked series ID from the form.
    - If the clicked series ID is the same as the current series ID, redirect to the index route.
    - Update the session with the new active series ID.
    - Retrieve series data, schedules, and series IDs from the database.
    - Render the index.html template with the retrieved data.

    Returns:
        Response: Flask response object containing a rendered HTML template or a redirect.
    """
    current_series_id = session["current_series_id"]

    if request.method == "POST":

        # Get info of clicked series id
        series_id = int(request.form.get("series-id"))

        if series_id == current_series_id:
            return redirect("/")

        # Update session variable active_series_id
        session["active_series_id"] = series_id

        # Get info on [past] (1) series, (2) schedules, and (3) series ids
        series, schedules, series_ids = get_series_data(DATABASE_NAME, series_id)

        return render_template("index.html",
                               series=series,
                               schedules=schedules,
                               series_ids=series_ids)

    return redirect("/")


@main.route("/film", methods=["GET", "POST"])
def film_view():
    """
    Handle the series view route for the application.

    For GET requests:
    - Redirect to the index route.

    For POST requests:
    - Retrieve the clicked series ID from the form.
    - If the clicked series ID is the same as the current series ID, redirect to the index route.
    - Update the session with the new active series ID.
    - Retrieve series data, schedules, and series IDs from the database.
    - Render the index.html template with the retrieved data.

    Returns:
        Response: Flask response object containing a rendered HTML template or a redirect.
    """
    if request.method == "POST":
        # Get info of [active] series id
        series_id = request.form.get("series-id")
        series_id = int(series_id)

        # Get film_id of requested film
        film_id = request.form.get("film-id")

        # Get info on [past] (1) series, (2) schedules, and (3) series ids
        series, schedules, series_ids = get_series_data(DATABASE_NAME, series_id)

        # Get info of requested film
        film = queries.get_info_film(DATABASE_NAME, film_id)

        return render_template("film.html",
                               series=series,
                               schedules=schedules,
                               series_ids=series_ids,
                               film=film)

    return redirect("/")


@main.route("/location")
def location_view():
    """
    Handle the location view route for the application.

    - Retrieve the active series ID from the session.
    - Retrieve series data, schedules, and series IDs from the database.
    - Render the location.html template with the retrieved data and the map API key.

    Returns:
        Response: Flask response object containing a rendered HTML template.
    """
    # Get info of [active] series id
    series_id = session["active_series_id"]

    # Get info on [past] (1) series, (2) schedules, and (3) series ids
    series, schedules, series_ids = get_series_data(DATABASE_NAME, series_id)

    return render_template("location.html",
                           series=series,
                           schedules=schedules,
                           series_ids=series_ids,
                           map_api_key=MAP_API_KEY)


@main.route("/org")
def org_view():
    """
    Handle the org view route for the application.

    - Retrieve the active series ID from the session.
    - Retrieve series data, schedules, and series IDs from the database.
    - Render the org.html template with the retrieved data.

    Returns:
        Response: Flask response object containing a rendered HTML template.
    """
    # Get info of [active] series id
    series_id = session["active_series_id"]

    # Get info on [past] (1) series, (2) schedules, and (3) series ids
    series, schedules, series_ids = get_series_data(DATABASE_NAME, series_id)

    return render_template("org.html",
                           series=series,
                           schedules=schedules,
                           series_ids=series_ids)
