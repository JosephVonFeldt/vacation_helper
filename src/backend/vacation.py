# from datetime import datetime, timedelta
#
# from flask_restful import Resource
#
# from .dbHelper import Cities, Weather, db
# from .flights import get_flights, get_best_flight
# from .utils import check_weather, days_until_friday
# from .weather import get_weather, set_weather
#
#
# class VacationFinderApiHandler(Resource):
#     @staticmethod
#     def get(airport, vac_type):
#         condition = False
#         if vac_type == 'Snow':
#             condition = Cities.snow != ''
#         elif vac_type == 'Beach':
#             condition = Cities.beach != ''
#         elif vac_type == 'Hiking':
#             condition = Cities.hiking != ''
#         arr = []
#         subq = db.select(
#             Weather.city, Weather.state, Weather.snow, Weather.precipitation,
#             Weather.temperature_min, Weather.temperature_max,
#             db.func.max(Weather.datetime).label("datetime")
#         ).group_by(Weather.city, Weather.state)
#         query_results = db.session.query(Cities) \
#             .join(Weather, Cities.city == Weather.city and Weather.state == subq.state, isouter=True).order_by(
#             Weather.datetime.desc()) \
#             .add_columns(Cities.city, Cities.state, Cities.latitude, Cities.longitude, Cities.airport,
#                          Weather.snow, Weather.precipitation,
#                          Weather.temperature_min, Weather.temperature_max, Weather.datetime
#                          ).filter(condition).order_by(Cities.city.asc()).all()
#
#         for i, result in enumerate(query_results):
#             if result.airport == airport:
#                 continue
#             if result.datetime is None or (datetime.utcnow() - result.datetime).total_seconds() > 60 * 60:
#                 res = get_weather(result.latitude, result.longitude)
#                 w = set_weather(result.city, result.state, res)
#             else:
#                 w = Weather(city=result.city, state=result.state, snow=result.snow, precipitation=result.precipitation,
#                             temperature_min=result.temperature_min, temperature_max=result.temperature_max, )
#             arr.append({'CITY': result.city, "AP": result.airport, "POSSIBLE": check_weather(vac_type, w), "KEY": i})
#             if arr[-1]["POSSIBLE"]:
#                 day = datetime.today() + timedelta(days_until_friday())
#                 dday = day + timedelta(2)
#                 flights = get_flights(airport, arr[-1]["AP"], day, dday)
#                 try:
#
#                     price, link, _ = get_best_flight(flights)
#                     arr[-1]['PRICE'] = price
#                     arr[-1]['LINK'] = link
#                     if not price or price > 1000:
#                         arr.pop()
#                 except:
#                     arr.pop()
#                     print(flights.keys())
#         return arr
