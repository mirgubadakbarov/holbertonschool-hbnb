from app.models.base_model import BaseModel

class Review(BaseModel):
    def __init__(self, user, place, rating, comment):
        super().__init__()
        self.user = user
        self.place = place
        self.rating = rating
        self.comment = comment

    def to_dict(self):
        review_dict = super().to_dict()
        review_dict.update({
            "user": self.user.to_dict(),
            "place": self.place.to_dict(),
            "rating": self.rating,
            "comment": self.comment
        })
        return review_dict
