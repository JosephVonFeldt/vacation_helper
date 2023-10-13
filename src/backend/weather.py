import requests
from flask import Flask
from sqlalchemy.dialects.postgresql import insert
from datetime import datetime
try:
    from .dbHelper import db, Weather, Cities
    from .utils import days_until_friday
except:
    from dbHelper import db, Weather, Cities
    from utils import days_until_friday
import os
import pika

def get_weather(lat, long):
    response = requests.get(
        f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,snowfall_sum&temperature_unit=fahrenheit&precipitation_unit=inch&timezone=America%2FDenver')
    return response.json()


def set_weather(city, state, response):
    ind = days_until_friday() - 1
    daily = response['daily']
    snow = daily['snowfall_sum'][ind]
    precipitation = daily['precipitation_sum'][ind]
    temperature_min = daily['temperature_2m_min'][ind]
    temperature_max = daily['temperature_2m_max'][ind]

    w = Weather(city=city, state=state, snow=snow, precipitation=precipitation, temperature_min=temperature_min,
                temperature_max=temperature_max, datetime=datetime.utcnow())
    statement = insert(Weather).values(city=city, state=state, snow=snow, precipitation=precipitation,
                                       temperature_min=temperature_min,
                                       temperature_max=temperature_max,
                                       datetime=datetime.utcnow()).on_conflict_do_update(
        index_elements=['city', 'state'],
        set_={'city': city,
              'state': state,
              'snow': snow,
              'precipitation': precipitation,
              'temperature_min': temperature_min,
              'temperature_max': temperature_max,
              'datetime': datetime.utcnow()})
    db.session.execute(statement)
    db.session.commit()
    return w


if __name__ == "__main__":
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/vacation_helper')

    db.init_app(app)
    with app.app_context():
        query_results = db.session.query(Cities).add_columns(Cities.city, Cities.state, Cities.latitude, Cities.longitude).filter((Cities.snow != '') | (Cities.beach != '') | (Cities.hiking != '')).order_by(Cities.city.asc()).all()
        for result in query_results:
            lat = result.latitude
            long = result.longitude
            city = result.city
            state = result.state
            response = get_weather(lat, long)
            w = set_weather(city, state, response)
            print(f"{w.city}: {w.datetime}")
        query_results = db.session.query(Cities).add_columns(Cities.airport).order_by(Cities.city.asc()).all()

        url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost:5672/%2f')
        params = pika.URLParameters(url)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.queue_declare("Flights")
        for r in query_results:
            message = r.airport
            channel.basic_publish(exchange='',
                                  routing_key='Flights',
                                  body=message)
            print(f" [x] Sent '{message}'")
        channel.close()
