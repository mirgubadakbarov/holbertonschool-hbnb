from flask import Blueprint, request, jsonify
from app.models.place import Place
from app.services.place_service import PlaceService

place_routes = Blueprint('place_routes', __name__)

@place_routes.route('/places', methods=['POST'])
def create_place():
    data = request.json
    place = PlaceService.create_place(data)
    return jsonify(place.to_dict()), 201

