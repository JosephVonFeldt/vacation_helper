from flask import Flask, request, send_from_directory
from flask_restful import Api, Resource
from backend.dataCollector import VacationFinderApiHandler, CitiesApiHandler, db

app = Flask(__name__, static_url_path='', static_folder='frontend/client-app/build')

api = Api(app)

un = 'postgres'
pw = 'postgres'
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{un}:{pw}@localhost:5432/vacation_helper'

db.init_app(app)
with app.app_context():
    db.create_all()

@app.route("/")
def main():
    return send_from_directory(app.static_folder, 'index.html')


api.add_resource(CitiesApiHandler, '/cities')
api.add_resource(VacationFinderApiHandler, '/VF/<string:airport>/<string:vac_type>')
