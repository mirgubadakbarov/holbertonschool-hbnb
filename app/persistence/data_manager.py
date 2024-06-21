class DataManager(IPersistenceManager):
    def __init__(self):
        self.data = {
            'Country': {},
            'City': {},
            'Amenity': {},
            'User': {},
            'Place': {},
            'Review': {}
        }

    def _preload_countries(self):
        # Example of pre-loading countries
        countries = [
            {"code": "US", "name": "United States"},
            {"code": "CA", "name": "Canada"}
        ]
        for country in countries:
            self.save(Country(country['code'], country['name']))

    def save(self, entity):
        entity_type = type(entity).__name__
        self.data[entity_type][entity.id] = entity.to_dict()

    def get(self, entity_id, entity_type):
        return self.data[entity_type].get(entity_id)

    def get_all(self, entity_type):
        return list(self.data[entity_type].values())

    def delete(self, entity_id, entity_type):
        if entity_id in self.data[entity_type]:
            del self.data[entity_type][entity_id]
    
    def get_by_field(self, entity_type, field_name, field_value):
        for entity in self.data[entity_type].values():
            if entity[field_name] == field_value:
                return entity
        return None
