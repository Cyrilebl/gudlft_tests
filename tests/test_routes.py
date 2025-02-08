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
    fake_clubs = [{"name": "Club Test", "email": "test@example.com"}]
    monkeypatch.setattr(client.application, "clubs", fake_clubs)


def test_home_valid_email(client):
    """Test with a valid email."""
    response = client.post("/home", data={"email": "test@example.com"})
    assert response.status_code == 200


def test_home_invalid_email(client):
    """Test with an invalid email."""
    response = client.post(
        "/home", data={"email": "wrong@example.com"}, follow_redirects=True
    )
    assert response.status_code == 404


def test_home_missing_email(client):
    """Test with no email provided."""
    response = client.post("/home", data={}, follow_redirects=True)
    assert response.status_code == 400
