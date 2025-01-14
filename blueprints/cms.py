# Python Standard Library
import json
import sqlite3

# Third-Party Libraries
from flask import Blueprint, redirect, render_template, request
from werkzeug.security import check_password_hash, generate_password_hash

# Local Libraries
from form import get_dicts, get_query, get_dicts_updates, get_query_update_series, get_query_update_schedules
import queries 




cms = Blueprint('cms', __name__)

# Set SQLite database variable
db = "lafs.db"


@cms.route("/cms")
def cmsdash():

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


@cms.route("/cms/series")
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


@cms.route("/cms/create", methods=["GET", "POST"])
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


@cms.route("/cms/view", methods=["GET", "POST"])
def cms_view():

    if request.method == "POST":

        post = request.form.to_dict()

        # print(json.dumps(post, indent=4))

        dicts = get_dicts_updates(post)
        dict_series = dicts[0]
        dict_schedule = dicts[1]
        # dict_films = dicts[2]
        # dict_colors = dicts[3]

        # print(json.dumps(dict_series, indent=4))
        # print(json.dumps(dict_schedule, indent=4))
        # print(json.dumps(dict_films, indent=4))
        # print(json.dumps(dict_colors, indent=4))
    
        #
        # FILM SERIES
        #
        # 1. Translate dict into SQL query
        query_series = get_query_update_series(dict_series)
        # 2. Execute query
        if query_series is not None:
            print(query_series)
            queries.update_records(db, query_series)
        else:
            print("Series: nothing to update")

        #
        # SCHEDULE
        #
        # 0. Update dictionary
        for film in dict_schedule:
            if "id" in dict_schedule[film]:
                dict_schedule[film]["film_id"] = dict_schedule[film].pop("id")
        # 1. Translate dict into SQL query
        query_schedule = get_query_update_schedules(dict_schedule)
        print(query_schedule)
        # 2. Execute query
        if query_schedule is not None:
            for query in query_schedule:
                queries.update_records(db, query)

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


@cms.route("/cms/unpublish", methods=["GET", "POST"])
def cms_unpublish():

    if request.method == "POST":

        series_id = request.args.get('unpublish')

        print(series_id)

        return render_template("cms_unpublish.html", 
                               sidebar="series")
    
    else:
        
        return redirect("/cms")


@cms.route("/cms/films")
def cmsfilms():

    films = queries.get_info_cms_films(db)

    return render_template("cms_films.html", 
                            films=films,
                            sidebar="films")


@cms.route("/cms/org", methods=["GET", "POST"])
def cmsorg():

    if request.method == "POST":
        
        user_id = request.form.get("user-id")

        user = queries.get_info_user(db, user_id)

        return render_template("cms_user.html", 
                               user=user,
                               sidebar="org")
    
    else: 

        users = queries.get_info_users(db)

        return render_template("cms_org.html", 
                            users=users,
                            sidebar="org")


@cms.route("/cms/register", methods=["GET", "POST"])
def cmsregister():

    # It is best to leave actual implementent of this to a security expert.

    if request.method == "POST":

        new_name_first = request.form.get("new_name_first")
        new_name_last = request.form.get("new_name_last")
        new_username = request.form.get("new_username")
        new_password = request.form.get("new_password")
        new_password_again = request.form.get("new_password_again")
        new_role = request.form.get("new_role")

        if new_password == new_password_again:
            
            new_password = generate_password_hash(new_password_again)

            # Create connection and cursor
            connection = sqlite3.connect(db, check_same_thread=False)
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()

            # Query db
            query = "INSERT INTO users (name_first, name_last, role, status, username, hash)"
            query = query + "VALUES (?, ?, ?, ?, ?, ?); "
            cursor.execute(query, (new_name_first, new_name_last, new_role, 1, new_username, new_password,))

            connection.commit()
            
            # Close cursor and connection
            cursor.close()
            connection.close()

        return redirect("/cms/org")

    else:

        return render_template("cms_register.html", 
                               sidebar="org")


@cms.route("/cms/user", methods=["GET", "POST"])
def cmsuser():

    if request.method == "POST":

        form_name = request.form.get('form')
        user_id = request.form.get('user-id')

        user = queries.get_info_user(db, user_id)

        if form_name == "info":

            updated_name_first = request.form.get("updated_name_first")
            updated_name_last = request.form.get("updated_name_last")
            updated_username = request.form.get("updated_username")
            updated_role = request.form.get("new_role")

            update = 0

            if not updated_name_first:
                updated_name_first = user["name_first"]
            else:
                if updated_name_first != user["name_first"]:
                    update += 1

            if not updated_name_last:
                updated_name_last = user["name_last"]
            else:
                if updated_name_last != user["name_last"]:
                    update += 1
            
            if not updated_username:
                updated_username = user["username"]
            else:
                if updated_username != user["username"]:
                    update += 1

            if updated_role != user["role"]:
                update += 1

            if update > 0:
                queries.update_user_info(db, 
                                         updated_name_first, 
                                         updated_name_last, 
                                         updated_username, 
                                         updated_role, 
                                         user_id)

            return redirect("/cms/org")

        elif form_name == "status":

            current_status = int(user["status"])
            updated_status = int(request.form.get("status"))

            if current_status != updated_status:
                queries.update_user_status(db, updated_status, user_id)

            return redirect("/cms/org")
        
        elif form_name == "pass":

            # It is best to leave actual implementent of this to a security expert.

            pass_current_form = request.form.get("pass_current")
            pass_updated = request.form.get("pass_updated")
            pass_updated_again = request.form.get("pass_updated_again")

            if check_password_hash(user["hash"], pass_current_form) and pass_updated == pass_updated_again:

                queries.update_user_hash(db, generate_password_hash(pass_updated_again), user_id)

                print("Password saved")

            else:
                print("Password not saved")

            return redirect("/cms/org")
        
        elif form_name == "delete":

            queries.delete_user(db, user_id)

            return redirect("/cms/org")
        
        else:

            return redirect("/cms/org")

    else:

        user_id = request.form.get("user-id")

        print(user_id)

        return render_template("cms_user.html", 
                               sidebar="org")
    

@cms.route("/cms/media")
def cmsmedia():

    return render_template("cms_media.html", 
                           sidebar="media")
