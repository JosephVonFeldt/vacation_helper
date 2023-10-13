
from ..dbHelper import *
from ..weather import *


class TestClass:
    def test_hiking(self):
        w = Weather(city='test', state='TEST', snow=0, precipitation=1, temperature_min=50, temperature_max=85)
        assert check_weather('Hiking', w)

    def test_hiking_neg(self):
        w = Weather(city='test', state='TEST', snow=3, precipitation=3, temperature_min=20, temperature_max=45)
        assert not check_weather('Hiking', w)

    def test_snow(self):
        w = Weather(city='test', state='TEST', snow=3, precipitation=3, temperature_min=20, temperature_max=45)
        assert check_weather('Snow', w)

    def test_snow_neg(self):
        w = Weather(city='test', state='TEST', snow=9, precipitation=9, temperature_min=20, temperature_max=45)
        assert not check_weather('Snow', w)

    def test_beach(self):
        w = Weather(city='test', state='TEST', snow=0, precipitation=1, temperature_min=70, temperature_max=95)
        assert check_weather('Beach', w)

    def test_beach_neg(self):
        w = Weather(city='test', state='TEST', snow=9, precipitation=9, temperature_min=20, temperature_max=45)
        assert not check_weather('Beach', w)

    def test_hiking_dir(self):
        w = Weather(city='test', state='TEST', snow=0, precipitation=1, temperature_min=50, temperature_max=85)
        assert check_hiking(w)

    def test_hiking_neg_dir(self):
        w = Weather(city='test', state='TEST', snow=3, precipitation=3, temperature_min=20, temperature_max=45)
        assert not check_hiking(w)

    def test_snow_dir(self):
        w = Weather(city='test', state='TEST', snow=3, precipitation=3, temperature_min=20, temperature_max=45)
        assert check_snow(w)

    def test_snow_neg_dir(self):
        w = Weather(city='test', state='TEST', snow=9, precipitation=9, temperature_min=20, temperature_max=45)
        assert not check_snow(w)

    def test_beach_dir(self):
        w = Weather(city='test', state='TEST', snow=0, precipitation=1, temperature_min=70, temperature_max=95)
        assert check_beach(w)

    def test_beach_neg_dir(self):
        w = Weather(city='test', state='TEST', snow=9, precipitation=9, temperature_min=20, temperature_max=45)
        assert not check_beach(w)
