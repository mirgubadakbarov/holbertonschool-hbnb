from app.models.place import Place

class PlaceService:
    places = []

    @staticmethod
    def create_place(data):
        # Add logic to create a place with proper business rules
        place = Place(
            name=data['name'],
            description=data['description'],
            address=data['address'],
            city=data['city'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            host=data['host'],
            number_of_rooms=data['number_of_rooms'],
            bathrooms=data['bathrooms'],
            price_per_night=data['price_per_night'],
            max_guests=data['max_guests'],
            amenities=data.get('amenities', [])
        )
        PlaceService.places.append(place)
        return place
