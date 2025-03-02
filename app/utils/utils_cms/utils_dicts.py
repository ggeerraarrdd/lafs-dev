"""
TD
"""









def get_dicts(post):
    """
    TD
    """
    keys_series = [
        "new_series_semester",
        "new_series_year",
        "new_series_title",
        "new_series_brief",
        "new_series_poster"
    ]

    keys_schedule = [
        "id",
        "schedule"
        ]

    keys_films = [
        "id",
        "film_title",
        "film_director",
        "film_year",
        "film_runtime",
        "film_description",
        "wiki",
        "note"
        ]

    keys_colors = [
        "color1",
        "color2",
        "color3"
        ]

    # PART 1
    # Create series dict
    dict_series = {k.lstrip('new_'): post[k] for k in keys_series if k in post}

    # INTERIM
    # Process post to create dictionary for schedule and films keys
    dict_all = {}

    for key, value in post.items():
        if key not in keys_series and key not in keys_colors:
            num = 'film' + key[-1]
            if key[-2].isdigit():
                num = 'film' + key[-2:]
                key = key.rstrip('0123456789')
            if num not in dict_all:
                dict_all[num] = {}
            key = key.rstrip('0123456789')
            dict_all[num][key] = value

    # PART 2
    # Only schedule keys in dict_all
    dict_schedule = {}

    for key, value in dict_all.items():
        film_values = {}
        for k, v in value.items():
            if k in keys_schedule:
                film_values[k] = v
        dict_schedule[key] = film_values

    # PART 3
    # Only film keys in dict_all
    dict_films = {}

    for key, value in dict_all.items():
        film_values = {}
        for k, v in value.items():
            if k in keys_films:
                film_values[k] = v
        dict_films[key] = film_values

    # PART 4
    # Create films dict
    dict_colors = {k: post[k] for k in keys_colors if k in post}

    # RETURN
    return dict_series, dict_schedule, dict_films, dict_colors


def get_query(data):
    """
    Translate dictionary into an INSERT query statement
    """
    # keys_series = [
    #     "new_series_semester",
    #     "new_series_year",
    #     "new_series_title",
    #     "new_series_brief",
    #     "new_series_poster"
    # ]

    # keys_schedule = [
    #     "id",
    #     "schedule"
    #     ]

    keys_films = [
        "id",
        "film_title",
        "film_director",
        "film_year",
        "film_runtime",
        "film_description",
        "wiki",
        "note"
        ]

    # keys_colors = [
    #     "color1",
    #     "color2",
    #     "color3"
    #     ]

    if "film1" in data:
        if "schedule" in list(data["film1"].keys()):
            table_name = "schedules"
        if "film_title" in list(data["film1"].keys()):
            table_name = "films"

        # COLUMNS
        col_names = ""

        for key in data['film1'].keys():
            col_names += key + ", "

        col_names = col_names.rstrip(", ")

        # VALUES
        values = ""

        for keys_films in data.keys():
            values += "("
            for key, value in data[keys_films].items():
                values += f"'{value}', "
            values = values.rstrip(", ")
            values += "), "

        values = values.rstrip(", ")

        # FULL QUERY
        query = f"INSERT INTO {table_name} ({col_names}) VALUES {values};" # pylint: disable=possibly-used-before-assignment
    else:
        if "series_title" in data:
            table_name = "series"
        elif 'color1' in data:
            table_name = "colors"

        columns = ", ".join(data.keys())
        values = ", ".join(["'" + str(value) + "'" for value in data.values()])
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values});"

    return query


def get_dicts_updates(post):
    """
    TD
    """
    keys_series = [
        "series_number",
        "series_semester",
        "series_year",
        "series_title",
        "series_brief",
        "series_poster"
    ]

    keys_schedule = [
        "schedule_id",
        "series_id",
        "imdb",
        "schedule",
        "notes"
        ]

    keys_films = [
        "id",
        "imdb",
        "film_title",
        "film_director",
        "film_year",
        "film_runtime",
        "film_description",
        "wiki",
        ]

    keys_colors = [
        "color1",
        "color2",
        "color3"
        ]

    # PART 1
    # Create series dict
    dict_series = {k.lstrip('new_'): post[k] for k in keys_series if k in post}

    # INTERIM
    # Process post to create dictionary for schedule and films keys
    dict_all = {}

    for key, value in post.items():
        if key not in keys_series and key not in keys_colors:
            num = 'film' + key[-1]
            if key[-2].isdigit():
                num = 'film' + key[-2:]
                key = key.rstrip('0123456789')
            if num not in dict_all:
                dict_all[num] = {}
            key = key.rstrip('0123456789')
            dict_all[num][key] = value

    # PART 2
    # Only schedule keys in dict_all
    dict_schedule = {}

    for key, value in dict_all.items():
        film_values = {}
        for k, v in value.items():
            if k in keys_schedule:
                film_values[k] = v
        dict_schedule[key] = film_values

    # PART 3
    # Only film keys in dict_all
    dict_films = {}

    for key, value in dict_all.items():
        film_values = {}
        for k, v in value.items():
            if k in keys_films:
                film_values[k] = v
        dict_films[key] = film_values

    # PART 4
    # Create films dict
    dict_colors = {k: post[k] for k in keys_colors if k in post}

    # RETURN
    return dict_series, dict_schedule, dict_films, dict_colors


def get_query_update_series(data):
    """
    TD
    """
    series_number = data.get("series_number")

    set_values = []

    count = 0
    for key, value in data.items():
        if key != "series_number":
            if value:
                set_values.append(f"{key} = '{value}'")
                count += 1

    set_values = ", ".join(set_values)

    if count == 0:
        query = None
    else:
        query = f"UPDATE series SET {set_values} WHERE series_id = {series_number};"

    return query


def get_query_update_schedules(data):
    """
    TD
    """
    count = 0
    query = []

    for key, value in data.items(): # pylint: disable=unused-variable

        set_values = []
        set_condition = []

        if value["notes"]:
            for inner_key, inner_value in value.items():
                if inner_key != "schedule_id":
                    if inner_key == "imdb":
                        set_values.append(f"film_id = '{inner_value}'")
                    else:
                        set_values.append(f"{inner_key} = '{inner_value}'")
                elif inner_key == "schedule_id":
                    set_condition.append(f"{inner_key} = '{inner_value}'")

            set_values = ", ".join(set_values)
            set_condition = " AND ".join(set_condition)

            query.append(f"UPDATE schedules SET {set_values} WHERE {set_condition};")

            count += 1

    if count == 0:
        query = None

    return query
