import requests
import json
from flask import Flask
# from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, request, render_template, redirect
from flask_restful import Resource, Api, reqparse
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from flask_sqlalchemy import SQLAlchemy
# from models import Programs, Sections, Activities
# from fields import *


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:@localhost/admin'

db = SQLAlchemy(app)

api = Api(app)

### Models Class
class Programs(db.Model):
    # __tablename__ = 'programs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    descriptions = db.Column(db.String(200))

    def __repr__(self):
        return "<Programs(name='%s')>" % (self.name)
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Sections(db.Model):
    # __tablename__ = 'sections'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    descriptions = db.Column(db.String(200))
    image_url = db.Column(db.String(100))
    order_index = db.Column(db.Integer)
    programs = db.Column(db.Integer, db.ForeignKey('programs.id'))

    def __repr__(self):
       return "<Sections(name='%s')>" % (self.name)
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Activities(db.Model):
    # __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    activity_type = db.Column(db.String(25))
    descriptions = db.Column(db.String(500))
    sections = db.Column(db.Integer, db.ForeignKey('sections.id'))

    def __repr__(self):
       return "<Activities(name='%s')>" % (self.name)
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}


## Setups 
section_counter = {}

def get_section_counter():
    programs = Programs.query.all()  # 1
    for p in programs:
        section_counter[str(p.id)] = Sections.query.filter_by(programs=p.id).count()  # 4


def bad_request(msg=None):
    if msg:
        return {"ErrorMessage": msg}, 404
    return {"ErrorMessage": "Bad Request Error: Please check your apis and Try Again!"}, 404


get_section_counter()

## View Classess
program_args = reqparse.RequestParser()
program_args.add_argument('name', required=True)
program_args.add_argument('descriptions', required=True)


class ProgramsList(Resource):

    def get(self):
        base_uri = request.base_url
        program_list = []
        try: 
            query = Programs.query.all()
            for row in query:
                program_list.append(row.as_dict())
                program_list[-1]['url'] = base_uri + '/' + str(program_list[-1]['id'])
            if not program_list:
                raise ValueError
        except ValueError:
            return bad_request()
        except Exception as e:
            return bad_request(str(e))
        return program_list, 200
    
    def post(self):
        args = program_args.parse_args()
        program_obj = Programs(
            name=args.name,
            descriptions=args.descriptions
        )
        try:
            db.session.add(program_obj)
            db.session.commit()
        except SQLAlchemyError as e:
            return bad_request(str(e.__dict__['orig']))
        return program_obj.as_dict(), 201


class ProgramsDetail(Resource):
    def get(self, p_id):
        try:
            query = Programs.query.filter_by(id=p_id).all()
            if len(query) != 1:
                raise ValueError
            program = query[-1].as_dict()
            program["url"] = request.base_url
            program['sections'] = program["url"] + "/sections"
        except ValueError:
            return bad_request()
        except Exception as e:
            return bad_request(str(e))
        return program, 200


section_args = reqparse.RequestParser()
section_args.add_argument('name', required=True)
section_args.add_argument('descriptions', required=True)
section_args.add_argument('image_url', required=True)
# section_args.add_argument('order_index', type=int, required=True)
# section_args.add_argument('programs', type=int, required=True)


class SectionsList(Resource):

    def get(self, p_id):
        section_list = []
        try:
            query = Sections.query.filter_by(programs=p_id).all()
            for row in query:
                section_list.append(row.as_dict())
                section_list[-1]['url'] = request.base_url + '/' + str(section_list[-1]['id'])
            if not section_list:
                raise ValueError
        except ValueError:
            return bad_request()
        except Exception as e:
            return bad_request(str(e))
        return section_list, 200
    
    def post(self, p_id):
        args = program_args.parse_args()
        section_obj = Sections(
            name=args.name,
            descriptions=args.descriptions,
            image_url=args.image_url,
            order_index=section_counter[p_id] + 1,
            programs=int(p_id)
        )
        try:
            db.session.add(section_obj)
            db.session.commit()
            section_counter[p_id] += 1
        except SQLAlchemyError as e:
            return bad_request(str(e.__dict__['orig']))
        return section_obj.as_dict(), 201


class SectionsDetail(Resource):

    def get(self, p_id, s_id):
        try:
            query = Sections.query.filter_by(programs=p_id).filter_by(id=s_id).all()
            if len(query) != 1:
                raise ValueError
            section = query[-1].as_dict()
            section["url"] = request.base_url
            section['activity_url'] = section["url"] + "/activities"
            if section['order_index'] < section_counter[p_id]:
                next_id = str(int(s_id) + 1)
                section['next'] = next_id
            if section['order_index'] > 1:
                prev_id = str(int(s_id) - 1)
                section['previous'] = prev_id
            section['programs'] = request.url_root + 'programs/{}'.format(p_id)
        except ValueError:
            return bad_request()
        except Exception as e:
            return bad_request(str(e))
        return section, 200


activity_args = reqparse.RequestParser()
activity_args.add_argument('name', required=True)
activity_args.add_argument('descriptions', required=True)
activity_args.add_argument('activity_type', required=True)


class ActivitiesList(Resource):

    def get(self, p_id, s_id):
        activity_list = []
        try:
            query = Activities.query.filter_by(sections=s_id).all()
            for row in query:
                activity_list.append(row.as_dict())
                activity_list[-1]['url'] = request.base_url + '/' + str(activity_list[-1]['id'])
            if not activity_list:
                raise ValueError
        except ValueError:
            return bad_request()
        except Exception as e:
            return bad_request(str(e))
        return activity_list, 200
    
    def post(self, p_id, s_id):
        args = program_args.parse_args()
        activity_obj = Activities(
            name=args.name,
            descriptions=args.descriptions,
            activity_type=args.activity_type,
            sections=int(s_id)
        )
        try:
            db.session.add(activity_obj)
            db.session.commit()
            section_counter[p_id] += 1
        except SQLAlchemyError as e:
            return bad_request(str(e.__dict__['orig']))
        return activity_obj.as_dict(), 201


class ActivitiesDetail(Resource):

    def get(self, p_id, s_id, a_id):
        try:
            query = Activities.query.filter_by(sections=s_id).filter_by(id=a_id).all()
            if len(query) != 1:
                raise Exception.ValueError
            section = query[-1].as_dict()
            section["url"] = request.base_url
            section['activity'] = section["url"] + "/activities"
            
        except ValueError:
            return bad_request()
        except Exception as e:
            return bad_request(str(e))
        return section, 200

## UI endpoints
@app.route('/')
@app.route('/program_list')
def get_program():
    r = requests.get("http://127.0.0.1:5000/programs")
    return render_template("program_list.html", data=json.loads(r.text))

@app.route('/program_details/<p_id>')
def get_program_details(p_id=None):
    programs_details = requests.get("http://127.0.0.1:5000/programs/{}".format(p_id))
    section_list = requests.get("http://127.0.0.1:5000/programs/{}/sections".format(p_id))
    data = {
        'program_detail': json.loads(programs_details.text),
        'section_list': json.loads(section_list.text)
    }
    return render_template("program_details.html", data=data)

@app.route('/section_details/<p_id>/<s_id>')
def get_sections_details(p_id=None, s_id=None):
    programs_details = requests.get("http://127.0.0.1:5000/programs/{}".format(p_id))
    section_detials = requests.get("http://127.0.0.1:5000/programs/{}/sections/{}".format(p_id, s_id))
    activities = requests.get("http://127.0.0.1:5000/programs/{}/sections/{}/activities".format(p_id, s_id))
    data = {
        'program_detials': json.loads(programs_details.text),
        'section_details': json.loads(section_detials.text),
        'activity_details': json.loads(activities.text)
    }
    return render_template("section_details.html", data=data)


## RESTful Endpoints
api.add_resource(ProgramsList, '/programs')
api.add_resource(ProgramsDetail, '/programs/<p_id>')
api.add_resource(SectionsList, '/programs/<p_id>/sections')
api.add_resource(SectionsDetail, '/programs/<p_id>/sections/<s_id>')
api.add_resource(ActivitiesList, '/programs/<p_id>/sections/<s_id>/activities')
api.add_resource(ActivitiesDetail, '/programs/<p_id>/sections/<s_id>/activities/<a_id>')



if __name__ == '__main__':
    app.run(debug=True)
    