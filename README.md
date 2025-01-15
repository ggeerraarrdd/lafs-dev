# LAFSCMS

A bespoke CMS for the Landscape Architecture Film Series website

## Description

_LAFSCMS_ is the companion content management system (CMS) for the _Landscape Architecture Film Series_ [website](https://l-a-f-s.org/). Currently in alpha, the plan is to merge the beta version with the [film series repo](https://github.com/ggeerraarrdd/film-series).

Just like any real-world organization, student-run organizations such as a film series experience knowledge loss when their membership graduate. Unless there is a knowledge transfer process, that loss may lead to technical resources being underutilized or altogether becoming inactive. Alternative resources and processes always exist, but they either must be created from scratch, requiring non-zero time and resources, or are imperfect substitutes. If existing resources do the job perfectly fine, why go through all that effort?

_LAFSCMS_ was developed to address that issue of knowledge loss by providing a CMS accessed through a user-friendly web interface to manage content and users.

![LAFSCMS](docs/images/lafscms_1.png)

The features of the system are based on business requirements as captured in the following user stories:

1. "As an admin or a curator, I want to log in or log out of the CMS, so that I can access the functionalities of the CMS or stop that access."
2. "As an admin or a curator, I want to create a film series, so that I can start the process of updating the website with the new film series."
3. "As an admin or a curator, I want to edit a film series, so that information related to the film series is updated."
4. "As an admin or a curator, I want to publish a film series, so that website visitors can view information about the film series."
5. "As an admin or a curator, I want to unpublish a film series, so that the film series is removed from the website."
6. "As an admin or a curator, I want to delete a film series, so that the film series is removed from both the website and database."
7. "As an admin or a curator, I want to update a scheduled film in an ongoing series, so that website visitors are informed about new nformation."
8. "As an admin or a curator, I want to see a list of all films in a completed, ongoing or unpublished series, so that I don't duplicate a film in a future series."
9. "As an admin or a curator, I want to media files, so that they are correct and up-to-date on the website or database."
10. "As an admin or curator, I want to read documentations on using the film series website and CMS, so that I can use them properly."
11. "As an admin or curator, I want to edit my user info and login credentials, so that they are correct and up-to-date."
12. "As an admin, I want to register new users, so that they can access the CMS."
13. "As an admin, I want to manage users, so that their info and login credentials are correct and up-to-date.."
14. "As an admin, I want to manage user privileges, so that users can access only the CMS functionalities based on their status and roles."

As of v2.0.0-alpha.2, all user stories have been implemented except for #1, #6, #9 and #10.

More screenshots below.

## Disclaimer

ALL CONTENTS IN THIS REPO ARE FOR EDUCATIONAL PURPOSES ONLY.

## Getting Started

### Dependencies

* Flask==3.0.0
* Werkzeug==3.0.1

### Usage

Clone it!

```bash
git clone https://github.com/ggeerraarrdd/lafs-cms.git
```

Go into the project directory and run the command:

```bash
flask run
```

To open the film series website, copy the URL after 'Running on'.

To open the CMS, add `cms` at the end of the url.

### Notes on Google Maps

This is disabled.

## Author(s)

* [@ggeerraarrdd](https://github.com/ggeerraarrdd/)

## Version History

### Release Notes

* See [https://github.com/ggeerraarrdd/lafs-cms/releases](https://github.com/ggeerraarrdd/lafs-cms/releases)

### Future Work

Development of primary features is ongoing.

## License

* [MIT License](https://github.com/ggeerraarrdd/large-parks/blob/main/LICENSE)

## Acknowledgments

* Notion AI

## Screenshots

![LAFSCMS](docs/images/lafscms_2.png)
![LAFSCMS](docs/images/lafscms_3.png)
![LAFSCMS](docs/images/lafscms_4.png)
![LAFSCMS](docs/images/lafscms_5.png)
![LAFSCMS](docs/images/lafscms_6.png)
![LAFSCMS](docs/images/lafscms_7.png)
