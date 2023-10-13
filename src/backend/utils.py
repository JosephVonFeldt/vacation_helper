from datetime import date
def days_until_friday():
    ans = (4 - date.today().weekday()) % 7
    if ans == 0:
        ans = 7
    return ans

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