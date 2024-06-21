import uuid
from datetime import datetime

class Review:
    def __init__(self, user_id, place_id, rating, comment):
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.place_id = place_id
        self.rating = rating
        self.comment = comment
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'place_id': self.place_id,
            'rating': self.rating,
            'comment': self.comment,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def update(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()
