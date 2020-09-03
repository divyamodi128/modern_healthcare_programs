import unittest
import json
import sys
from sqlalchemy import create_engine
from index import (app, db, Programs, Activities, Sections)
from sqlalchemy.orm import sessionmaker

from flask_fixtures import FixturesMixin


class TestConfig(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    testing = True
    debug = True

app.config.from_object('tests.test_programs.TestConfig')

class MyTest(unittest.TestCase, FixturesMixin):
    # engine_default = create_engine(DB_CONN_URI_DEFAULT)
    fixtures = ['tests/fixtures.json']
    app = app
    db = db
    db.create_all()

    def test_programs(self):
        programs = Programs.query.all()
        assert len(programs) == Programs.query.count() == 4
    
    def test_sections(self):
        sections = Sections.query.all()
        assert len(sections) == Sections.query.count() == 26

    def test_activities(self):
        activities = Activities.query.all()
        assert len(activities) == Activities.query.count() == 26
        # assert len(programs[0].id) == 3

    ## Similarly we can write testcase to add, update and delete data from the tables 

if __name__ == "__main__":
    unittest.main()
    ## To run test case
    # python -m unittest discover