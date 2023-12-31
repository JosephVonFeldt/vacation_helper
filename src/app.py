from flask import Flask, send_from_directory
from flask_restful import Api

from src.backend.cities import CitiesApiHandler
from src.backend.flights import VacationFinderApiHandler
from src.backend.utils import cleanup
import os

from src.backend.dbHelper import db

app = Flask(__name__, static_url_path='', static_folder='frontend/client-app/build')

api = Api(app)
db.app = app
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgres://postgres:postgres@localhost:5432/vacation_helper').replace("://", "ql://", 1)
db.init_app(app)

with app.app_context():
    engine_container = db.engine
    db.create_all()
    cleanup(db.session, engine_container)

@app.route("/")
def main():
    return send_from_directory(app.static_folder, 'index.html')


api.add_resource(CitiesApiHandler, '/cities')
api.add_resource(VacationFinderApiHandler, '/VF/<string:airport>/<string:vac_type>')
