# server/models/pet.py

from server.database import db

class Pet(db.Model):
    __tablename__ = 'pets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    species = db.Column(db.String(50), nullable=False)
    breed = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255))
    adoption_status = db.Column(db.String(50), default="Available")  # Available or Adopted
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # Reference to User (owner)

    # Relationships
    adoptions = db.relationship('Adoption', backref='pet', lazy=True)
    reviews = db.relationship('Review', backref='pet', lazy=True)
    favorites = db.relationship('Favorite', backref='pet', lazy=True)

    def __repr__(self):
        return f'<Pet {self.name}, {self.species}>'
