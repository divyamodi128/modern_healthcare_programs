import json

from index import (app, db, Programs, Activities, Sections)
from flask_fixtures import FixturesMixin


class LoadMyFixtures(FixturesMixin):
    fixtures = ['tests/fixtures.json']
    app = app
    db = db
    db.create_all()

    def __init__(self):
        import pdb; pdb.set_trace()
        pass

if __name__ == "__main__":
    LoadMyFixtures()