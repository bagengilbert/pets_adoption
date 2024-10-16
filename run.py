import os
from flask import Flask
from flask_migrate import Migrate
from server.app import app, db  # Ensure this matches your structure

# Initialize Flask-Migrate
migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run()
