from app.models.base_model import BaseModel

class City(BaseModel):
    def __init__(self, name, country):
        super().__init__()
        self.name = name
        self.country = country

    def to_dict(self):
        city_dict = super().to_dict()
        city_dict.update({
            "name": self.name,
            "country": self.country.to_dict()
        })
        return city_dict
