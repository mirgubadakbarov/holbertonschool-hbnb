import unittest
import json
from app import app

class TestPlaceEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        # Create a city and amenities for testing
        self.city_id = self._create_city('Test City', 'US')
        self.amenity_ids = [
            self._create_amenity('Free WiFi'),
            self._create_amenity('Swimming Pool')
        ]

    def _create_city(self, name, country_code):
        response = self.app.post('/cities', data=json.dumps({
            'name': name,
            'country_code': country_code
        }), content_type='application/json')
        return response.json['id']

    def _create_amenity(self, name):
        response = self.app.post('/amenities', data=json.dumps({
            'name': name
        }), content_type='application/json')
        return response.json['id']

    def test_create_place(self):
        response = self.app.post('/places', data=json.dumps({
            'name': 'Test Place',
            'description': 'A nice place',
            'address': '123 Main St',
            'city_id': self.city_id,
            'latitude': 40.7128,
            'longitude': -74.0060,
            'host_id': 'host123',
            'number_of_rooms': 2,
            'number_of_bathrooms': 1,
            'price_per_night': 150.0,
            'max_guests': 4,
            'amenity_ids': self.amenity_ids
        }), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)

    def test_get_places(self):
        response = self.app.get('/places')
        self.assertEqual(response.status_code, 200)

    def test_get_place(self):
        create_response = self.app.post('/places', data=json.dumps({
            'name': 'Test Place',
            'description': 'A nice place',
            'address': '123 Main St',
            'city_id': self.city_id,
            'latitude': 40.7128,
            'longitude': -74.0060,
            'host_id': 'host123',
            'number_of_rooms': 2,
            'number_of_bathrooms': 1,
            'price_per_night': 150.0,
            'max_guests': 4,
            'amenity_ids': self.amenity_ids
        }), content_type='application/json')
        place_id = create_response.json['id']
        response = self.app.get(f'/places/{place_id}')
        self.assertEqual(response.status_code, 200)

    def test_update_place(self):
        create_response = self.app.post('/places', data=json.dumps({
            'name': 'Test Place',
            'description': 'A nice place',
            'address': '123 Main St',
            'city_id': self.city_id,
            'latitude': 40.7128,
            'longitude': -74.0060,
            'host_id': 'host123',
            'number_of_rooms': 2,
            'number_of_bathrooms': 1,
            'price_per_night': 150.0,
            'max_guests': 4,
            'amenity_ids': self.amenity_ids
        }), content_type='application/json')
        place_id = create_response.json['id']
        response = self.app.put(f'/places/{place_id}', data=json.dumps({
            'description': 'An updated description'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['description'], 'An updated description')

    def test_delete_place(self):
        create_response = self.app.post('/places', data=json.dumps({
            'name': 'Test Place',
            'description': 'A nice place',
            'address': '123 Main St',
            'city_id': self.city_id,
            'latitude': 40.7128,
            'longitude': -74.0060,
            'host_id': 'host123',
            'number_of_rooms': 2,
            'number_of_bathrooms': 1,
            'price_per_night': 150.0,
            'max_guests': 4,
            'amenity_ids': self.amenity_ids
        }), content_type='application/json')
        place_id = create_response.json['id']
        response = self.app.delete(f'/places/{place_id}')
        self.assertEqual(response.status_code, 204)

class TestAmenityEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_create_amenity(self):
        response = self.app.post('/amenities', data=json.dumps({
            'name': 'Free WiFi'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)

    def test_get_amenities(self):
        response = self.app.get('/amenities')
        self.assertEqual(response.status_code, 200)

    def test_get_amenity(self):
        create_response = self.app.post('/amenities', data=json.dumps({
            'name': 'Swimming Pool'
        }), content_type='application/json')
        amenity_id = create_response.json['id']
        response = self.app.get(f'/amenities/{amenity_id}')
        self.assertEqual(response.status_code, 200)

    def test_update_amenity(self):
        create_response = self.app.post('/amenities', data=json.dumps({
            'name': 'Gym'
        }), content_type='application/json')
        amenity_id = create_response.json['id']
        response = self.app.put(f'/amenities/{amenity_id}', data=json.dumps({
            'name': 'Fitness Center'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Fitness Center')

    def test_delete_amenity(self):
        create_response = self.app.post('/amenities', data=json.dumps({
            'name': 'Parking'
        }), content_type='application/json')
        amenity_id = create_response.json['id']
        response = self.app.delete(f'/amenities/{amenity_id}')
        self.assertEqual(response.status_code, 204)


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
