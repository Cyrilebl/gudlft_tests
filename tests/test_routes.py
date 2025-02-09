import pytest

from app import create_app
from config import TestingConfig


@pytest.fixture
def client():
    """Create a test client for making requests"""
    app = create_app(TestingConfig)
    with app.test_client() as client:
        yield client


def test_index_route(client):
    """Test if index route returns a 200 status."""
    response = client.get("/")
    assert response.status_code == 200


@pytest.fixture(autouse=True)
def setup(client, monkeypatch):
    """Set up fake data"""
    fake_club = [{"name": "Club Test", "email": "test@example.com", "points": "10"}]
    fake_competition = [{"name": "Competition Test", "numberOfPlaces": "5"}]
    monkeypatch.setattr(client.application, "clubs", fake_club)
    monkeypatch.setattr(client.application, "competitions", fake_competition)


def test_home_valid_email(client):
    """Test with a valid email"""
    response = client.post("/home", data={"email": "test@example.com"})
    assert response.status_code == 200


def test_home_invalid_email(client):
    """Test with an invalid email"""
    response = client.post(
        "/home", data={"email": "wrong@example.com"}, follow_redirects=True
    )
    assert response.status_code == 404


def test_home_missing_email(client):
    """Test with no email provided"""
    response = client.post("/home", data={}, follow_redirects=True)
    assert response.status_code == 400


# Tests on valid scenarios


def test_purchase_places_with_valid_number(client):
    """Test with a club having enough points and a competition with enough places."""
    response = client.post(
        "/purchasePlaces",
        data={"club": "Club Test", "competition": "Competition Test", "places": "3"},
    )
    assert response.status_code == 200
    assert b"Great - booking complete!" in response.data
    club = client.application.clubs[0]
    assert club["points"] == "7"
    competition = client.application.competitions[0]
    assert competition["numberOfPlaces"] == "2"


# Tests on invalid scenarios


def test_purchase_places_with_empty_number(client):
    """Test with no value provided"""
    response = client.post(
        "/purchasePlaces",
        data={"club": "Club Test", "competition": "Competition Test", "places": ""},
    )
    assert response.status_code == 200
    assert b"Please enter a number" in response.data


def test_purchase_places_with_negative_number(client):
    """Test with no negative number"""
    response = client.post(
        "/purchasePlaces",
        data={"club": "Club Test", "competition": "Competition Test", "places": "-2"},
    )
    assert response.status_code == 200
    assert b"Please enter a number greater than zero" in response.data


def test_purchase_places_with_zero(client):
    """Test with zero"""
    response = client.post(
        "/purchasePlaces",
        data={"club": "Club Test", "competition": "Competition Test", "places": "0"},
    )
    assert response.status_code == 200
    assert b"Please enter a number greater than zero" in response.data


def test_purchase_places_request_above_club_points(client):
    """Test to request more club points than are available"""
    response = client.post(
        "/purchasePlaces",
        data={"club": "Club Test", "competition": "Competition Test", "places": "11"},
    )
    assert response.status_code == 200
    assert b"Sorry, your club has 10 points left" in response.data


def test_purchase_places_request_above_competition_places(client):
    """Test to request more competition places than are available"""
    response = client.post(
        "/purchasePlaces",
        data={"club": "Club Test", "competition": "Competition Test", "places": "6"},
    )
    assert response.status_code == 200
    assert b"Sorry, the competition has 5 places left" in response.data
