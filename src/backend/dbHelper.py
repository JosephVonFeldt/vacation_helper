from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Cities(db.Model):
    city = db.Column(db.String, primary_key=True, nullable=False)
    state = db.Column(db.String, primary_key=True, nullable=False)
    hiking = db.Column(db.String)
    snow = db.Column(db.String)
    beach = db.Column(db.String)
    airport = db.Column(db.String, nullable=False)
    latitude = db.Column(db.Double, nullable=False)
    longitude = db.Column(db.Double, nullable=False)


class Weather(db.Model):
    city = db.Column(db.String, primary_key=True, nullable=False)
    state = db.Column(db.String, primary_key=True, nullable=False)
    snow = db.Column(db.Float, nullable=False)
    precipitation = db.Column(db.Float, nullable=False)
    temperature_min = db.Column(db.Float, nullable=False)
    temperature_max = db.Column(db.Float, nullable=False)
    datetime = db.Column(db.DateTime, default=datetime.utcnow())


class Flights(db.Model):
    originAirport = db.Column(db.String, primary_key=True, nullable=False)
    destinationAirport = db.Column(db.String, primary_key=True, nullable=False)
    hiking = db.Column(db.String)
    snow = db.Column(db.String)
    beach = db.Column(db.String)
    price = db.Column(db.Float, nullable=False)
    link = db.Column(db.String, nullable=False)
    sessionToken = db.Column(db.String, nullable=False)
    datetime = db.Column(db.DateTime, default=datetime.utcnow())
