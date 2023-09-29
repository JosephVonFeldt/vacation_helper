import requests
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.sqlite import insert
from flask_restful import Resource
from datetime import datetime, timedelta, date
import json

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


class CitiesApiHandler(Resource):
    @staticmethod
    def get():
        arr = []
        query_results = db.session.query(Cities).order_by(Cities.city.asc()).all()
        for i, city in enumerate(query_results):
            arr.append({'CITY': city.city, "AP": city.airport, "KEY": i})
        return arr


class VacationFinderApiHandler(Resource):
    @staticmethod
    def get(airport, vac_type):

        condition = False
        if vac_type == 'Snow':
            condition = Cities.snow != ''
        elif vac_type == 'Beach':
            condition = Cities.beach != ''
        elif vac_type == 'Hiking':
            condition = Cities.hiking != ''
        arr = []
        subq = db.select(
            Weather.city, Weather.state, Weather.snow, Weather.precipitation,
            Weather.temperature_min, Weather.temperature_max,
            db.func.max(Weather.datetime).label("datetime")
        ).group_by(Weather.city, Weather.state)
        query_results = db.session.query(Cities) \
            .join(Weather, Cities.city == Weather.city and Weather.state == subq.state, isouter=True).order_by(
            Weather.datetime.desc()) \
            .add_columns(Cities.city, Cities.state, Cities.latitude, Cities.longitude, Cities.airport,
                         Weather.snow, Weather.precipitation,
                         Weather.temperature_min, Weather.temperature_max, Weather.datetime
                         ).filter(condition).order_by(Cities.city.asc()).all()

        for i, result in enumerate(query_results):
            if result.airport == airport:
                continue
            if result.datetime is None or (datetime.utcnow() - result.datetime).total_seconds() > 60 * 60:
                res = get_weather(result.latitude, result.longitude)
                w = set_weather(result.city, result.state, res)
            else:
                w = Weather(city=result.city, state=result.state, snow=result.snow, precipitation=result.precipitation,
                            temperature_min=result.temperature_min, temperature_max=result.temperature_max, )
            arr.append({'CITY': result.city, "AP": result.airport, "POSSIBLE": check_weather(vac_type, w), "KEY": i})
            if arr[-1]["POSSIBLE"]:
                day = datetime.today() + timedelta(days_until_friday())
                dday = day + timedelta(2)
                flights = get_flights(airport, arr[-1]["AP"], day, dday)
                try:

                    price, link = get_best_flight(flights)
                    arr[-1]['PRICE'] = price
                    arr[-1]['LINK'] = link
                    if not price or price > 1000:
                        arr.pop()
                except:
                    arr.pop()
                    print(flights.keys())
        return arr


def check_weather(vac_type, weather):
    if vac_type == 'Snow':
        return check_snow(weather)
    elif vac_type == 'Beach':
        return check_beach(weather)
    elif vac_type == 'Hiking':
        return check_hiking(weather)


def check_snow(weather):
    return 0.5 < weather.snow < 7 and weather.temperature_max < 60 and weather.temperature_min < 32


def check_beach(weather):
    return weather.precipitation < 3 and 70 < weather.temperature_max and 50 < weather.temperature_min


def check_hiking(weather):
    return weather.precipitation < 2 and 70 < weather.temperature_max < 90 and 40 < weather.temperature_min


def days_until_friday():
    ans = (4 - date.today().weekday()) % 7
    if ans == 0:
        ans = 7
    return ans


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
                                       temperature_max=temperature_max).on_conflict_do_update( index_elements=['city','state'],
        set_={'city': city,
         'state': state,
         'snow': snow,
         'precipitation': precipitation,
         'temperature_min': temperature_min,
         'temperature_max': temperature_max,})
    db.session.execute(statement)
    db.session.commit()
    return w


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
    return response.json()

def get_best_flight(data):
    content = data['content']
    results = content['results']
    itineraries = results['itineraries']
    best = content['sortingOptions']['best']
    if len(best) == 0:
        return False, False
    id = best[0]['itineraryId']
    flight = itineraries[id]
    items = flight['pricingOptions'][0]['items']
    price = float('inf')
    link = ''
    for item in items:
        if float(item['price']['amount']) / 1000 < price:
            price = float(item['price']['amount']) / 1000
            link = item['deepLink']
    return price, link