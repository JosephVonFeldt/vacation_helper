from flask import Flask
from flask_restful import Resource
from .dbHelper import db, Cities
from .utils import cleanup
import os

class CitiesApiHandler(Resource):
    @staticmethod
    def get():
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL',
                                                               'postgres://postgres:postgres@localhost:5432/vacation_helper').replace(
            "://", "ql://", 1)
        db.init_app(app)
        db.app = app
        arr = []
        with app.app_context():
            engine_container = db.engine
            query_results = db.session.query(Cities).order_by(Cities.city.asc()).all()
            for i, city in enumerate(query_results):
                arr.append({'CITY': city.city, "AP": city.airport, "KEY": i})
            cleanup(db.session, engine_container)
        return arr
