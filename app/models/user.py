from app.models.base_model.py import BaseModel

class User(BaseModel):
    def __init__(self, email, password, first_name, last_name):
        super().__init__()
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.places = []

    def to_dict(self):
        user_dict = super().to_dict()
        user_dict.update({
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "places": [place.to_dict() for place in self.places]
        })
        return user_dict
