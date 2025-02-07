from flask import Flask
from config import Config

from .utils import load_clubs, load_competitions
from .routes import main


def create_app(test_config=None):
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)

    if test_config:
        app.config.update(test_config)

    # Load data
    app.clubs = load_clubs()
    app.competitions = load_competitions()

    # Blueprint for routes
    app.register_blueprint(main)

    return app
