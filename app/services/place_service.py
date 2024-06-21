from app.models.place import Place

class PlaceService:
    @staticmethod
    def create_place(data):
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
        # Save place to file (implement this part)
        return place
