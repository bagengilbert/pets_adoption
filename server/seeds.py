from server.database import db
from server.models.user import User
from server.models.pet import Pet
from server.models.adoption import Adoption
from server.models.review import Review
from server.models.favorite import Favorite
from server.models.shelter import Shelter

def create_users():
    """Create sample users."""
    user1 = User(email="alice@example.com", password="Password1!", name="Alice", address="123 Main St")
    user2 = User(email="bob@example.com", password="Password1!", name="Bob", address="456 Elm St")

    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()
    print("Users created.")


def create_shelters():
    """Create sample shelters."""
    shelter1 = Shelter(name="Happy Paws Shelter", address="789 Pine St", phone="555-1234")
    shelter2 = Shelter(name="Furry Friends Rescue", address="101 Maple Ave", phone="555-5678")

    db.session.add(shelter1)
    db.session.add(shelter2)
    db.session.commit()
    print("Shelters created.")


def create_pets():
    """Create sample pets."""
    pet1 = Pet(name="Buddy", breed="Golden Retriever", age=3, description="Friendly and energetic", shelter_id=1)
    pet2 = Pet(name="Mittens", breed="Tabby", age=2, description="Loves to cuddle", shelter_id=2)

    db.session.add(pet1)
    db.session.add(pet2)
    db.session.commit()
    print("Pets created.")


def create_adoptions():
    """Create sample adoptions."""
    adoption1 = Adoption(user_id=1, pet_id=1, date_adopted="2024-01-15")
    adoption2 = Adoption(user_id=2, pet_id=2, date_adopted="2024-02-20")

    db.session.add(adoption1)
    db.session.add(adoption2)
    db.session.commit()
    print("Adoptions created.")


def create_reviews():
    """Create sample reviews."""
    review1 = Review(user_id=1, pet_id=1, rating=5, comment="Best dog ever!")
    review2 = Review(user_id=2, pet_id=2, rating=4, comment="Very friendly cat!")

    db.session.add(review1)
    db.session.add(review2)
    db.session.commit()
    print("Reviews created.")


def create_favorites():
    """Create sample favorites."""
    favorite1 = Favorite(user_id=1, pet_id=1)
    favorite2 = Favorite(user_id=2, pet_id=2)

    db.session.add(favorite1)
    db.session.add(favorite2)
    db.session.commit()
    print("Favorites created.")


def seed_data():
    """Seed the database with initial data."""
    create_users()
    create_shelters()
    create_pets()
    create_adoptions()
    create_reviews()
    create_favorites()  # Add favorites to the seeding process
    print("Database seeded successfully.")


if __name__ == "__main__":
    from server.app import create_app  # Adjust the import based on your app structure
    app = create_app()
    with app.app_context():
        db.create_all()  # Create all tables
        seed_data()
