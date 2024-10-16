# server/models/adoption.py

from server.database import db
from datetime import datetime

class Adoption(db.Model):
    __tablename__ = 'adoptions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'), nullable=False)
    adoption_date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.String(255))

    def __repr__(self):
        return f'<Adoption User {self.user_id}, Pet {self.pet_id}>'
