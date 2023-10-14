from flights import *
from unittest.mock import patch

import unittest
from unittest.mock import Mock

# Mock requests to control its behavior
get_flights = Mock()
poll_flights = Mock()

mock_get_good_destinations = Mock()
m_city = Mock()

m_city.city = "Test"
m_city.state = "Test"
m_city.latitude = 0
m_city.longitude = 0
m_city.airport = 'TST'
m_city.city_snow = 'x'
m_city.beach = ''
m_city.hiking = ''
m_city.snow = 3
m_city.precipitation = 3
m_city.temperature_min = 25
m_city.temperature_max = 30
m_city.datetime = datetime.utcnow()

mock_get_good_destinations.return_value = [m_city]

@patch('flights.get_flights')
@patch('flights.poll_flights')
@patch('flights.get_good_destinations', new=mock_get_good_destinations)
class TestFlights(unittest.TestCase):
    def test_fetch_flights(self, mock_poll, mock_get):
        # Test a successful, logged request
        mock_get.return_value = dict()
        fetch_flights('test')
        mock_get_good_destinations.assert_called_once()
        mock_get.assert_called_once()
        mock_poll.assert_not_called()

if __name__ == '__main__':
    unittest.main()