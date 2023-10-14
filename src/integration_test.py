from .app import app
from unittest import TestCase

class TestIntegrations(TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_thing(self):
        response = self.app.get('/')
        assert response.status_code == 200

    def test_cities(self):
        response = self.app.get('/cities')
        assert response.status_code == 200

    def test_VF(self):
        response = self.app.get('/VF/DEN/Snow')
        assert response.status_code == 200
