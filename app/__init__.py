from flask import Flask, jsonify, request, abort
from app.persistence.data_manager import DataManager
from app.models.country import Country
from app.models.city import City

app = Flask(__name__)
data_manager = DataManager()


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
