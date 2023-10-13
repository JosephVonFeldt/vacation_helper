import time
from datetime import datetime, timedelta
import os
from flask_restful import Resource
import requests
import json

from flask import Flask
from sqlalchemy.dialects.postgresql import insert

from dbHelper import Cities, db, Weather, Flights
from utils import days_until_friday
from weather import check_snow, check_hiking, check_beach

import pika


def get_flights(origin, destination, arrival, departure):
    year, month, day = arrival.year, arrival.month, arrival.day
    dyear, dmonth, dday = departure.year, departure.month, departure.day
    params = {
        "query": {

            "market": "US",
            "locale": "en-US",

            "currency": "USD",
            "queryLegs": [
                {
                    "originPlaceId": {
                        "iata": origin
                    },
                    "destinationPlaceId": {
                        "iata": destination
                    },
                    "date": {
                        "year": year,
                        "month": month,
                        "day": day
                    }
                },
                {
                    "originPlaceId": {
                        "iata": destination
                    },
                    "destinationPlaceId": {
                        "iata": origin
                    },
                    "date": {
                        "year": dyear,
                        "month": dmonth,
                        "day": dday
                    }
                }
            ],
            "adults": 1,
            "childrenAges": [],
            "cabinClass": "CABIN_CLASS_ECONOMY",
            "excludedAgentsIds": [],
            "excludedCarriersIds": [],
            "includedAgentsIds": [],
            "includedCarriersIds": [],
            "includeSustainabilityData": False,
            "nearbyAirports": False
        }
    }
    url = 'https://partners.api.skyscanner.net/apiservices/v3/flights/live/search/create'
    header = {
        'x-api-key': 'sh428739766321522266746152871799',
        'Content-Type': 'application/json'}

    response = requests.post(url, headers=header, data=json.dumps(params))
    print(response)
    return response.json()


def poll_flights(session_token):
    url = f'https://partners.api.skyscanner.net/apiservices/v3/flights/live/search/poll/{session_token}'
    print(url)
    header = {
        'x-api-key': 'sh428739766321522266746152871799',
        'Content-Type': 'application/json'}

    response = requests.post(url, headers=header)
    print(response)
    return response.json()


def get_best_flight(data):
    try:
        content = data['content']
    except:
        return False, False, False
    session_token = data['sessionToken']
    results = content['results']
    itineraries = results['itineraries']
    best = content['sortingOptions']['best']
    if len(best) == 0:
        return False, False, session_token
    id = best[0]['itineraryId']
    flight = itineraries[id]
    items = flight['pricingOptions'][0]['items']
    price = float('inf')
    link = ''
    for item in items:
        if float(item['price']['amount']) / 1000 < price:
            price = float(item['price']['amount']) / 1000
            link = item['deepLink']
    return price, link, session_token


def fetch_flights(departureAirport):
    start = datetime.utcnow()
    print(f"Started {datetime.utcnow()}")
    condition =  (Cities.beach != '') | (Cities.hiking != '') | (Cities.snow != '')
    subq = db.select(
        Weather.city, Weather.state, Weather.snow, Weather.precipitation,
        Weather.temperature_min, Weather.temperature_max,
        db.func.max(Weather.datetime).label("datetime")
    ).group_by(Weather.city, Weather.state)
    query_results = db.session.query(Cities) \
        .join(Weather, Cities.city == Weather.city and Weather.state == subq.state, isouter=True).filter(condition).order_by(
        Weather.datetime.desc()) \
        .add_columns(Cities.city, Cities.state, Cities.latitude, Cities.longitude, Cities.airport,
                     Cities.snow.label("city_snow"),
                     Cities.beach, Cities.hiking, Weather.snow, Weather.precipitation,
                     Weather.temperature_min, Weather.temperature_max, Weather.datetime
                     ).order_by(Cities.city.asc()).all()
    session_token_list = []
    for i, result in enumerate(query_results):
        w = Weather(city=result.city, state=result.state, snow=result.snow, precipitation=result.precipitation,
                    temperature_min=result.temperature_min, temperature_max=result.temperature_max, )
        hiking = 'x' if result.hiking and check_hiking(w) else ''
        snow = 'x' if result.city_snow and check_snow(w) else ''
        beach = 'x' if result.beach and check_beach(w) else ''
        if hiking + snow + beach == "":
            session_token_list.append(False)
            continue

        if result.airport == departureAirport:
            session_token_list.append(False)
            continue
        if result.datetime is None:
            session_token_list.append(False)
            print(result.datetime)
            continue
        print(result.city)
        day = datetime.today() + timedelta(days_until_friday())
        dday = day + timedelta(2)
        time.sleep(1)
        flights = get_flights(departureAirport, result.airport, day, dday)
        price, link, session_token = get_best_flight(flights)
        session_token_list.append(session_token)
        if price and price <= 1000:
            statement = insert(Flights).values(originAirport=departureAirport, destinationAirport=result.airport,
                                               hiking=hiking, snow=snow, beach=beach, price=price, link=link,
                                               sessionToken=session_token,
                                               datetime=datetime.utcnow()).on_conflict_do_update(
                index_elements=['originAirport', 'destinationAirport'],
                set_={'originAirport': departureAirport,
                      'destinationAirport': result.airport,
                      'hiking': hiking,
                      'snow': snow,
                      'beach': beach,
                      'price': price,
                      'link': link,
                      'sessionToken': session_token,
                      'datetime': datetime.utcnow()})
            db.session.execute(statement)
            db.session.commit()
    for i, result in enumerate(query_results):
        if session_token_list[i]:
            time.sleep(1)
            res = poll_flights(session_token_list[i])
            price, link, session_token = get_best_flight(res)
            w = Weather(city=result.city, state=result.state, snow=result.snow, precipitation=result.precipitation,
                        temperature_min=result.temperature_min, temperature_max=result.temperature_max, )
            if price and price <= 1000:
                hiking = 'x' if result.hiking and check_hiking(w) else ''
                snow = 'x' if result.city_snow and check_snow(w) else ''
                beach = 'x' if result.beach and check_beach(w) else ''
                statement = insert(Flights).values(originAirport=departureAirport, destinationAirport=result.airport,
                                                   hiking=hiking, snow=snow, beach=beach, price=price, link=link,
                                                   sessionToken=session_token,
                                                   datetime=datetime.utcnow()).on_conflict_do_update(
                    index_elements=['originAirport', 'destinationAirport'],
                    set_={'originAirport': departureAirport,
                          'destinationAirport': result.airport,
                          'hiking': hiking,
                          'snow': snow,
                          'beach': beach,
                          'price': price,
                          'link': link,
                          'sessionToken': session_token,
                          'datetime': datetime.utcnow()})
                db.session.execute(statement)
                db.session.commit()
    end = datetime.utcnow()
    print(f"End {end}")
    print(f"Duration {end-start}")


def get_suggested_flights(departureAirport, vac_type):
    condition = False
    if vac_type == 'Snow':
        condition = Flights.snow != ''
    elif vac_type == 'Beach':
        condition = Flights.beach != ''
    elif vac_type == 'Hiking':
        condition = Flights.hiking != ''
    arr = []
    query_results = db.session.query(Flights).join(Cities,
                                                   Flights.destinationAirport == Cities.airport and Flights.originAirport == departureAirport,
                                                   isouter=True).add_columns(Cities.city, Flights.destinationAirport,
                                                                             Flights.price, Flights.link
                                                                             ).filter(condition).order_by(
        Cities.city.asc()).all()

    for i, result in enumerate(query_results):
        arr.append({'CITY': result.city, "AP": result.airport, "POSSIBLE": True, "KEY": i, "PRICE": result.price, "LINK": result.link})
    return arr

class VacationFinderApiHandler(Resource):
    @staticmethod
    def get(airport, vac_type):
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/vacation_helper')

        db.init_app(app)
        with app.app_context():
            condition = False
            if vac_type == 'Snow':
                condition = Flights.snow != ''
            elif vac_type == 'Beach':
                condition = Flights.beach != ''
            elif vac_type == 'Hiking':
                condition = Flights.hiking != ''
            arr = []
            query_results = db.session.query(Flights).add_columns(Flights.originAirport, Flights.destinationAirport,
                                                                  Flights.price, Flights.link, Flights.datetime).filter(condition & (Flights.originAirport == airport) )\
                .join(Cities, Cities.airport == Flights.destinationAirport ).add_columns(Cities.city).order_by(Cities.city.asc()).all()
            for i, result in enumerate(query_results):
                if result.datetime is None or (datetime.utcnow() - result.datetime).total_seconds() > 60 * 60 * 3:
                    continue
                arr.append({'CITY': result.city, "AP": result.destinationAirport, "POSSIBLE": True,
                            "PRICE": result.price, "LINK": result.link, "KEY": i})
            return arr


if __name__ == "__main__":
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/vacation_helper')

    db.init_app(app)
    with app.app_context():
        url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost:5672/%2f')
        params = pika.URLParameters(url)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.queue_declare("Flights")
        def callback(ch, method, properties, body):
            print(f" [x] Received {body.decode()}")
            fetch_flights(body.decode())

        channel.basic_consume(queue='Flights', on_message_callback=callback, auto_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
        channel.close()
