import pytest

from app import create_app
from config import TestingConfig


@pytest.fixture
def client():
    """Create a test client for making requests"""
    app = create_app(TestingConfig)
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def setup(client, monkeypatch):
    """Set up fake data"""
    fake_club = [{"name": "Club Test", "email": "test@example.com", "points": "10"}]
    fake_competition = [{"name": "Competition Test", "numberOfPlaces": "5"}]
    monkeypatch.setattr(client.application, "clubs", fake_club)
    monkeypatch.setattr(client.application, "competitions", fake_competition)
