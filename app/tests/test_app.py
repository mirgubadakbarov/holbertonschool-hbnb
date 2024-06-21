import unittest
import json
from app import app

class TestCountryCityEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_countries(self):
        response = self.app.get('/countries')
        self.assertEqual(response.status_code, 200)

    def test_get_country(self):
        response = self.app.get('/countries/US')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['code'], 'US')

    def test_create_city(self):
        response = self.app.post('/cities', data=json.dumps({
            'name': 'New York',
            'country_code': 'US'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)

    def test_get_cities(self):
        response = self.app.get('/cities')
        self.assertEqual(response.status_code, 200)

    def test_get_city(self):
        create_response = self.app.post('/cities', data=json.dumps({
            'name': 'Los Angeles',
            'country_code': 'US'
        }), content_type='application/json')
        city_id = create_response.json['id']
        response = self.app.get(f'/cities/{city_id}')
        self.assertEqual(response.status_code, 200)

    def test_update_city(self):
        create_response = self.app.post('/cities', data=json.dumps({
            'name': 'Chicago',
            'country_code': 'US'
        }), content_type='application/json')
        city_id = create_response.json['id']
        response = self.app.put(f'/cities/{city_id}', data=json.dumps({
            'name': 'New Chicago'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'New Chicago')

    def test_delete_city(self):
        create_response = self.app.post('/cities', data=json.dumps({
            'name': 'Houston',
            'country_code': 'US'
        }), content_type='application/json')
        city_id = create_response.json['id']
        response = self.app.delete(f'/cities/{city_id}')
        self.assertEqual(response.status_code, 204)

if __name__ == '__main__':
    unittest.main()
