from app.models.base_model import BaseModel

class Country(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def to_dict(self):
        country_dict = super().to_dict()
        country_dict.update({
            "name": self.name
        })
        return country_dict
