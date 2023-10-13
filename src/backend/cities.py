from flask import Flask
from flask_restful import Resource
from dbHelper import db, Weather, Cities
import os

class CitiesApiHandler(Resource):
    @staticmethod
    def get():
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/vacation_helper')

        db.init_app(app)
        with app.app_context():
            arr = []
            query_results = db.session.query(Cities).order_by(Cities.city.asc()).all()
            for i, city in enumerate(query_results):
                arr.append({'CITY': city.city, "AP": city.airport, "KEY": i})
            return arr