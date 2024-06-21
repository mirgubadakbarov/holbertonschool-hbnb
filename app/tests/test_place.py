import unittest
from app.models.place import Place
from app.services.place_service import PlaceService

class TestPlace(unittest.TestCase):
    def test_create_place(self):
        data = {
            "name": "Test Place",
            "description": "A place for testing",
            "address": "123 Test St",
            "city": {"name": "Test City", "country": {"name": "Test Country"}},
            "latitude": 40.7128,
            "longitude": -74.0060,
            "host": {"email": "host@example.com", "password": "password", "first_name": "Host", "last_name": "User"},
            "number_of_rooms": 3,
            "bathrooms": 2,
            "price_per_night": 100,
            "max_guests": 4
        }
        place = PlaceService.create_place(data)
        self.assertEqual(place.name, "Test Place")
        self.assertEqual(place.description, "A place for testing")

if __name__ == '__main__':
    unittest.main()
