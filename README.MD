### Modern Health Care Program Take Home Assignment.

## Technical Stack
1. Flask
2. Flask-restful
3. PostgreSQL
4. SQLalchemy
5. Flask-Fixtures
6. psycopg2
7. unittest
8. Bootstrap
9. Jinja2


## Restful endpoints

1. /programs -> List of all avaliable Programs.
2. /programs/<p_id> -> Selected program details.
3. /programs/<p_id>/sections -> List of Sections inside the selected Program.
4. /programs/<p_id>/sections/<s_id> -> Details on particular Section of a selected Program
5. /programs/<p_id>/sections/<s_id>/activities -> Activities listed of selected Section
6. /programs/<p_id>/sections/<s_id>/activities/<a_id> -> Activities details of selected Section

Note: All the list apis are capable of adding new records in database.

## UI view for customers

1. '/', 'program_list' -> Displays the list of all avaliable Programs.
2. '/program_details/<p_id>' -> Displays the list of all Sections of a selected Program.
3. '/section_details/<p_id>/<s_id>' -> displays the details of the selected Section and Activity to perform.


## Hightlights

1. Breadcrumb display on the UI
2. User can do continue and previous on sections
3. Implemented Restful and UI urls with Flask
4. Enabled loading of Fixture data in UnitTesting with fake SQLite database and for main PostgreSQL database.

## How to load Fixtures in PostgreSQL DB?

`python load_fixtures.py`

## How to run Flask Application?

`python index.py`

## How to run UnitTests?

`python -m unittest discover`

## Directory Structure
```
/modern_health
    /__init__.py
    /index.py
    /load_fixtures.py
    /README.MD
    /requirements.txt
    /templates
        /program_list.html
        /program_details.html
        /section_details.html
    /tests
        /__init__.py
        /test_programs.py
        /fixtures.json
```

## Screenshots
1. program_list.html

![alt text](https://github.com/divyamodi128/modern_healthcare_programs/blob/master/templates/screenshots/screenshot1.png?raw=true)

2. progrma_detials.html

![alt text](https://github.com/divyamodi128/modern_healthcare_programs/blob/master/templates/screenshots/screenshot2.png?raw=true)

3. section_detials.html

![alt text](https://github.com/divyamodi128/modern_healthcare_programs/blob/master/templates/screenshots/screenshot3.png?raw=true)
