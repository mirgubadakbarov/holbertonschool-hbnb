from flask import Flask, jsonify, request, abort
from app.persistence.data_manager import DataManager
from app.models.country import Country
from app.models.city import City

app = Flask(__name__)
data_manager = DataManager()



@app.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    data = request.get_json()
    required_fields = ['user_id', 'rating', 'comment']
    for field in required_fields:
        if field not in data:
            abort(400, description=f"Missing required field: {field}")

    # Validate rating
    rating = data['rating']
    if not (1 <= rating <= 5):
        abort(400, description="Rating must be between 1 and 5")

    # Check if place_id exists
    if not data_manager.get(place_id, 'Place'):
        abort(404, description="Place not found")

    # Check if user_id exists
    if not data_manager.get(data['user_id'], 'User'):
        abort(404, description="User not found")

    # Ensure user is not the host of the place
    place = data_manager.get(place_id, 'Place')
    if place['host_id'] == data['user_id']:
        abort(400, description="Hosts cannot review their own places")

    review = Review(place_id=place_id, **data)
    data_manager.save(review)
    return jsonify(review.to_dict()), 201

@app.route('/users/<user_id>/reviews', methods=['GET'])
def get_user_reviews(user_id):
    reviews = [review for review in data_manager.get_all('Review') if review['user_id'] == user_id]
    return jsonify(reviews), 200

@app.route('/places/<place_id>/reviews', methods=['GET'])
def get_place_reviews(place_id):
    reviews = [review for review in data_manager.get_all('Review') if review['place_id'] == place_id]
    return jsonify(reviews), 200

@app.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    review = data_manager.get(review_id, 'Review')
    if not review:
        abort(404, description="Review not found")
    return jsonify(review), 200

@app.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    data = request.get_json()
    review = data_manager.get(review_id, 'Review')
    if not review:
        abort(404, description="Review not found")

    # Validate rating if provided
    if 'rating' in data:
        rating = data['rating']
        if not (1 <= rating <= 5):
            abort(400, description="Rating must be between 1 and 5")

    review_obj = Review(**review)
    review_obj.update(data)
    data_manager.save(review_obj)
    return jsonify(review_obj.to_dict()), 200

@app.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    review = data_manager.get(review_id, 'Review')
    if not review:
        abort(404, description="Review not found")
    data_manager.delete(review_id, 'Review')
    return '', 204



@app.route('/places', methods=['POST'])
def create_place():
    data = request.get_json()
    required_fields = ['name', 'description', 'address', 'city_id', 'latitude', 'longitude', 'host_id', 'number_of_rooms', 'number_of_bathrooms', 'price_per_night', 'max_guests', 'amenity_ids']
    for field in required_fields:
        if field not in data:
            abort(400, description=f"Missing required field: {field}")

    # Validate city_id
    if not data_manager.get(data['city_id'], 'City'):
        abort(400, description="Invalid city_id")

    # Validate amenity_ids
    for amenity_id in data['amenity_ids']:
        if not data_manager.get(amenity_id, 'Amenity'):
            abort(400, description=f"Invalid amenity_id: {amenity_id}")

    place = Place(**data)
    data_manager.save(place)
    return jsonify(place.to_dict()), 201

@app.route('/places', methods=['GET'])
def get_places():
    places = data_manager.get_all('Place')
    return jsonify(places), 200

@app.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    place = data_manager.get(place_id, 'Place')
    if not place:
        abort(404, description="Place not found")
    return jsonify(place), 200

@app.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    data = request.get_json()
    place = data_manager.get(place_id, 'Place')
    if not place:
        abort(404, description="Place not found")

    # Validate city_id if provided
    if 'city_id' in data and not data_manager.get(data['city_id'], 'City'):
        abort(400, description="Invalid city_id")

    # Validate amenity_ids if provided
    if 'amenity_ids' in data:
        for amenity_id in data['amenity_ids']:
            if not data_manager.get(amenity_id, 'Amenity'):
                abort(400, description=f"Invalid amenity_id: {amenity_id}")

    place_obj = Place(**place)
    place_obj.update(data)
    data_manager.save(place_obj)
    return jsonify(place_obj.to_dict()), 200

@app.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    place = data_manager.get(place_id, 'Place')
    if not place:
        abort(404, description="Place not found")
    data_manager.delete(place_id, 'Place')
    return '', 204


@app.route('/amenities', methods=['POST'])
def create_amenity():
    data = request.get_json()
    name = data.get('name')

    # Validation
    if not name:
        abort(400, description="Missing required fields")
    
    # Check for unique amenity name
    existing_amenity = data_manager.get_by_field('Amenity', 'name', name)
    if existing_amenity:
        abort(409, description="Amenity name already exists")

    amenity = Amenity(name)
    data_manager.save(amenity)
    return jsonify(amenity.to_dict()), 201

@app.route('/amenities', methods=['GET'])
def get_amenities():
    amenities = data_manager.get_all('Amenity')
    return jsonify(amenities), 200

@app.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    amenity = data_manager.get(amenity_id, 'Amenity')
    if not amenity:
        abort(404, description="Amenity not found")
    return jsonify(amenity), 200

@app.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    data = request.get_json()
    amenity = data_manager.get(amenity_id, 'Amenity')
    if not amenity:
        abort(404, description="Amenity not found")

    amenity_obj = Amenity(**amenity)
    amenity_obj.update(data)
    data_manager.save(amenity_obj)
    return jsonify(amenity_obj.to_dict()), 200

@app.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    amenity = data_manager.get(amenity_id, 'Amenity')
    if not amenity:
        abort(404, description="Amenity not found")
    data_manager.delete(amenity_id, 'Amenity')
    return '', 204

@app.route('/countries', methods=['GET'])
def get_countries():
    countries = data_manager.get_all('Country')
    return jsonify(countries), 200

@app.route('/countries/<country_code>', methods=['GET'])
def get_country(country_code):
    country = data_manager.get_by_field('Country', 'code', country_code)
    if not country:
        abort(404, description="Country not found")
    return jsonify(country), 200

@app.route('/countries/<country_code>/cities', methods=['GET'])
def get_cities_by_country(country_code):
    cities = [city for city in data_manager.get_all('City') if city['country_code'] == country_code]
    return jsonify(cities), 200

@app.route('/cities', methods=['POST'])
def create_city():
    data = request.get_json()
    name = data.get('name')
    country_code = data.get('country_code')

    # Validation
    if not name or not country_code:
        abort(400, description="Missing required fields")

    country = data_manager.get_by_field('Country', 'code', country_code)
    if not country:
        abort(400, description="Invalid country code")

    # Check for unique city name within the same country
    existing_city = data_manager.get_by_field('City', 'name', name)
    if existing_city and existing_city['country_code'] == country_code:
        abort(409, description="City name already exists in this country")

    city = City(name, country_code)
    data_manager.save(city)
    return jsonify(city.to_dict()), 201

@app.route('/cities', methods=['GET'])
def get_cities():
    cities = data_manager.get_all('City')
    return jsonify(cities), 200

@app.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    city = data_manager.get(city_id, 'City')
    if not city:
        abort(404, description="City not found")
    return jsonify(city), 200

@app.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    data = request.get_json()
    city = data_manager.get(city_id, 'City')
    if not city:
        abort(404, description="City not found")

    city_obj = City(**city)
    city_obj.update(data)
    data_manager.save(city_obj)
    return jsonify(city_obj.to_dict()), 200

@app.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    city = data_manager.get(city_id, 'City')
    if not city:
        abort(404, description="City not found")
    data_manager.delete(city_id, 'City')
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
