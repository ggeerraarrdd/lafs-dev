import os
import json
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
import pprint 

import queries 
from form import get_dicts, get_query


# Configure application
app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set SQLite database variable
db = "lafs.db"

# Make sure Google Maps API key is set
# if not os.environ.get("MAP_API_KEY"):
#     print("INFO: MAP_API_KEY not set")
#     print("INFO: Get a Google Maps API Key")
#     print("INFO: On terminal, excecute: 'export MAP_API_KEY=value'")

#     raise RuntimeError("MAP_API_KEY not set")
# else:
#     print("MAP_API_KEY set")
#     map_api_key = os.environ.get("MAP_API_KEY")
    

@app.route("/", methods=["GET", "POST"])
def index():

    # Populate Bottom Container
    # Website opens with list of films and their scheduled showtimes for current series

    if request.method == "POST":
        return redirect("/")

    else:

        # Get info of [current] series id
        query_result = queries.get_id_current_series(db)
        
        # Update session
        session["active_series_id"] = session["current_series_id"] = query_result[0]

        # NOTE: For development purposes, change current_series_id to first series, not actual current
        session["active_series_id"] = session["current_series_id"] = 1

        # Update function variable series_id
        series_id = session["active_series_id"]

        # Get info on [past] (1) series, (2) schedules, and (3) series ids
        series = dict(queries.get_info_series(db, series_id))
        schedules = queries.get_info_schedules(db, series_id)
        series_ids = queries.get_info_series_ids(db)

        # Print to debug
        # pp = pprint.PrettyPrinter(depth=4)
        # pp.pprint(schedules[0])

        return render_template("index.html", series=series, schedules=schedules, series_ids=series_ids)


@app.route("/series", methods=["GET", "POST"])
def series():

    # Populate Bottom Container
    # List of films and their scheduled showtimes for selected past series

    # Temporary bypass to session timeouts
    try:
        current_series_id = session["current_series_id"]
    except KeyError:
        current_series_id = 1

    if request.method == "POST":

        # Get info of clicked series id 
        series_id = int(request.form.get("series-id"))

        if series_id == current_series_id:
            return redirect("/")
        else:
            # Update session variable active_series_id 
            session["active_series_id"] = series_id

            # Get info on [past] (1) series, (2) schedules, and (3) series ids
            series = dict(queries.get_info_series(db, series_id))
            schedules = queries.get_info_schedules(db, series_id)
            series_ids = queries.get_info_series_ids(db)

        return render_template("index.html", series=series, schedules=schedules, series_ids=series_ids)

    else:
        return redirect("/")


@app.route("/film", methods=["GET", "POST"])
def film():

    # Populate Middle Container - Right
    # Individual film info for any series, current or past

    if request.method == "POST":
        # Get info of [active] series id
        series_id = request.form.get("series-id")
        series_id = int(series_id)

        # Get film_id of requested film
        film_id = request.form.get("film-id")

        # Get info on [past] (1) series, (2) schedules, and (3) series ids
        series = dict(queries.get_info_series(db, series_id))
        schedules = queries.get_info_schedules(db, series_id)
        series_ids = queries.get_info_series_ids(db)

        # Get info of requested film
        film = queries.get_info_film(db, film_id)

        return render_template("film.html", series=series, schedules=schedules, series_ids=series_ids, film=film)

    else:
        return redirect("/")


@app.route("/map")
def map():

    # Populate Middle Container - Right
    # Map of Plym Auditorium

    # Set map_api_key
    global map_api_key

    # Get info of [active] series id
    series_id = session["active_series_id"]

    # Get info on [active] (1) series, (2) schedules, and (3) series ids
    series = dict(queries.get_info_series(db, series_id))
    schedules = queries.get_info_schedules(db, series_id)
    series_ids = queries.get_info_series_ids(db)

    return render_template("map.html", series=series, schedules=schedules, series_ids=series_ids, map_api_key=map_api_key)


@app.route("/org")
def org():

    # Populate Middle Container - Right
    # Info on ORG

    # Get info of [active] series id
    series_id = session["active_series_id"]

    # Get info on [active] (1) series, (2) schedules, and (3) series ids
    series = dict(queries.get_info_series(db, series_id))
    schedules = queries.get_info_schedules(db, series_id)
    series_ids = queries.get_info_series_ids(db)

    return render_template("org.html", series=series, schedules=schedules, series_ids=series_ids)


@app.route("/cms")
def cms():

    # Get info of [active] series id
    global active_series_id
    series_id = active_series_id = 6

    # Get info on [active] (1) series, (2) schedules, and (3) series ids
    series = dict(queries.get_info_series(db, series_id))
    next = queries.get_info_cms_next_film(db, series_id)
    films = queries.get_info_schedules(db, series_id)
    series_ids = queries.get_info_series_ids(db)

    serieses = queries.get_info_serieses(db)
    # series_info = queries.get_info_series_status(db, series_id)

    return render_template("cms_index.html", 
                           current_series=series, 
                           next=next,
                           films=films, 
                           serieses=serieses, 
                           sidebar="index")


@app.route("/cms/series")
def cmsseries():

    # Get info of [active] series id
    global active_series_id
    series_id = active_series_id = "6"

    # Get info on [active] (1) series, (2) schedules, and (3) series ids
    series = dict(queries.get_info_series(db, series_id))
    schedules = queries.get_info_schedules(db, series_id)
    series_ids = queries.get_info_series_ids(db)

    serieses = queries.get_info_serieses(db)
    series_info = queries.get_info_series_status(db, series_id)

    return render_template("cms_series.html", 
                           current_series=series, 
                           schedules=schedules, 
                           serieses=serieses, 
                           series_info=series_info,
                           sidebar="series")


@app.route("/cms/create", methods=["GET", "POST"])
def cmscreate():

    if request.method == "POST":

        post = request.form.to_dict()

        dicts = get_dicts(post)
        dict_series = dicts[0]
        dict_schedule = dicts[1]
        dict_films = dicts[2]
        dict_colors = dicts[3]

        print(json.dumps(dict_series, indent=4))
        print(json.dumps(dict_schedule, indent=4))
        print(json.dumps(dict_films, indent=4))
        print(json.dumps(dict_colors, indent=4))
        
        #
        # FILM SERIES
        #
        # 1. Translate dict into SQL query
        query_series = get_query(dict_series)
        # 2. Execute query
        new_series_id = queries.insert_new_series(db, query_series)

        #
        # FILMS
        #
        # 1. Translate dict into SQL query
        query_films = get_query(dict_films)
        # 2. Execute query
        queries.insert_new_records(db, query_films)

        #
        # SCHEDULE
        #
        # 0. Update dictionary
        for film in dict_schedule:
            dict_schedule[film] = {"series_id": new_series_id, **dict_schedule[film]}
        for film in dict_schedule:
            if "id" in dict_schedule[film]:
                dict_schedule[film]["film_id"] = dict_schedule[film].pop("id")
        # 1. Translate dict into SQL query
        query_schedule = get_query(dict_schedule)
        # 2. Execute query
        queries.insert_new_records(db, query_schedule)

        #
        # COLORS
        #
        # 0. Update dictionary
        dict_colors = {"series_id": new_series_id, **dict_colors}
        # 1. Translate dict into SQL query
        query_colors = get_query(dict_colors)
        # 2. Execute query
        queries.insert_new_records(db, query_colors)


        print(query_series)
        print(query_films)
        print(query_schedule)
        print(query_colors)

        return redirect("/cms/series")
    
    else:
        return render_template("cms_create.html", 
                               sidebar="series")


@app.route("/cms/view", methods=["GET", "POST"])
def cms_view():

    if request.method == "POST":

        return redirect("/cms")
    
    else:
        cms_series_id = request.args.get('id')
       
        cms_series = dict(queries.get_info_series(db, cms_series_id))
        cms_schedules = queries.get_info_cms_schedules(db, cms_series_id)
        
        cms_serieses = queries.get_info_serieses(db)
        cms_status = next((series for series in cms_serieses if series['series_id'] == int(cms_series_id)), None)

        if cms_status['status'] == 1:
            edit_status = 'disabled'
        else:
            edit_status = ''

        return render_template("cms_view.html", 
                               cms_series=cms_series, 
                               cms_schedules=cms_schedules, 
                               cms_status=cms_status, 
                               edit_status=edit_status,
                               sidebar="series")


@app.route("/cms/unpublish", methods=["GET", "POST"])
def cms_unpublish():

    if request.method == "POST":

        series_id = request.args.get('unpublish')

        print(series_id)

        return render_template("cms_unpublish.html", 
                               sidebar="series")
    
    else:
        
        return redirect("/cms")


@app.route("/cms/films")
def cmsfilms():

    films = queries.get_info_cms_films(db)

    return render_template("cms_films.html", 
                           films=films,
                           sidebar="films")


@app.route("/cms/org")
def cmsorg():

    users = queries.get_info_users(db)

    return render_template("cms_org.html", 
                           users=users,
                           sidebar="org")


@app.route("/cms/register", methods=["GET", "POST"])
def cmsregister():

    if request.method == "POST":

        new_name_first = request.form.get("new_name_first")
        new_name_last = request.form.get("new_name_last")
        new_username = request.form.get("new_username")
        new_password = request.form.get("new_password")
        new_role = request.form.get("new_role")

        print(new_name_first)
        print(new_name_last)
        print(new_username)
        print(new_password)
        print(new_role)

        return redirect("/cms/org")

    else:

        return render_template("cms_register.html", 
                               sidebar="org")


@app.route("/cms/media")
def cmsmedia():

    return render_template("cms_media.html", 
                           sidebar="media")
