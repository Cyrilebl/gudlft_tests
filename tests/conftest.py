import pytest
import server
from server import app


@pytest.fixture
def client():
    """Create a test client for making requests"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def setup(client, monkeypatch):
    """Set up fake data"""
    fake_club = [{"name": "Club Test", "email": "test@example.com", "points": "10"}]
    fake_competition = [
        {
            "name": "Competition Test",
            "date": "2027-01-01 10:00:00",
            "numberOfPlaces": "5",
        }
    ]

    monkeypatch.setattr(server, "clubs", fake_club)
    monkeypatch.setattr(server, "competitions", fake_competition)

    # Default values to avoid repetitions
    client.common_data = {"club": "Club Test", "competition": "Competition Test"}
