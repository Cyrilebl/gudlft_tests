from flask import Flask
from config import DevelopmentConfig

from .utils import load_clubs, load_competitions
from .routes import main


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config_class)

    # Load data
    app.clubs = load_clubs()
    app.competitions = load_competitions()

    # Blueprint for routes
    app.register_blueprint(main)

    return app
