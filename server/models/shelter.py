# server/models/shelter.py

from server.database import db

class Shelter(db.Model):
    __tablename__ = 'shelters'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(15))
    website = db.Column(db.String(120))

    # Relationships
    pets = db.relationship('Pet', backref='shelter', lazy=True)

    def __repr__(self):
        return f'<Shelter {self.name}, {self.address}>'
