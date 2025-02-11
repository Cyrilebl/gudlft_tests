import pytest
from freezegun import freeze_time


def test_index_route(client):
    """Test if index route returns a 200 status."""
    response = client.get("/")
    assert response.status_code == 200


class TestLogin:
    @pytest.fixture(autouse=True)
    def setup_method(self, client):
        self.client = client

    def test_login_valid_email(self):
        """Test with a valid email"""
        response = self.client.post("/login", data={"email": "test@example.com"})
        assert response.status_code == 302

    def test_login_invalid_email(self):
        """Test with an invalid email"""
        response = self.client.post(
            "/login", data={"email": "wrong@example.com"}, follow_redirects=True
        )
        assert b"Email not found" in response.data
        assert response.status_code == 200

    def test_login_missing_email(self):
        """Test with no email provided"""
        response = self.client.post("/login", data={"email": ""}, follow_redirects=True)
        assert b"Email is required" in response.data
        assert response.status_code == 200


def test_home(client):
    """Test home route"""
    with client.session_transaction() as sess:
        sess["club_name"] = "Club Test"

    response = client.get("/home")
    assert response.status_code == 200


def test_book(client):
    """Test the booking page with valid competition and club"""
    competition_name = "Competition Test"
    club_name = "Club Test"
    response = client.get(f"/book/{competition_name}/{club_name}")
    assert response.status_code == 200


class TestPurchasePlaces:
    @pytest.fixture(autouse=True)
    def setup_method(self, client):
        self.client = client
        self.common_data = client.common_data

    def test_purchase_places_with_valid_number(self):
        """Test with a club having enough points and a competition with enough places."""
        response = self.client.post(
            "/purchasePlaces",
            data={**self.common_data, "places": "3"},
        )
        assert response.status_code == 200
        assert b"Great - booking complete!" in response.data
        club = self.client.application.clubs[0]
        assert club["points"] == "7"
        competition = self.client.application.competitions[0]
        assert competition["numberOfPlaces"] == "2"

    @pytest.mark.parametrize(
        "places, expected_message",
        [
            ("", b"Please enter a number"),
            ("-2", b"Please enter a number greater than zero"),
            ("0", b"Please enter a number greater than zero"),
        ],
    )
    def test_purchase_places_invalid_numbers(self, places, expected_message):
        """Test invalid number of places"""
        response = self.client.post(
            "/purchasePlaces",
            data={**self.common_data, "places": places},
        )
        assert expected_message in response.data
        assert response.status_code == 200

    @freeze_time("2030-01-01 12:00:00")
    def test_purchase_in_past_competition(self):
        """Test booking places for a past competition"""
        response = self.client.post(
            "/purchasePlaces",
            data={
                **self.common_data,
                "places": 2,
            },
        )
        assert (
            b"This competition already took place on January 01, 2027, at 10:00 AM"
            in response.data
        )
        assert response.status_code == 200

    @pytest.mark.parametrize(
        "places, expected_message",
        [
            ("13", b"You cannot book more than 12 places"),
            ("11", b"Sorry, your club has 10 points left"),
            ("6", b"Sorry, the competition has 5 places left"),
        ],
    )
    def test_purchase_places_invalid_requests(self, places, expected_message):
        """Test invalid places purchase requests"""
        response = self.client.post(
            "/purchasePlaces",
            data={**self.common_data, "places": places},
        )
        assert expected_message in response.data
        assert response.status_code == 200


def test_logout(client):
    """Test if logout route returns a 302 status."""
    response = client.get("/logout")
    assert response.status_code == 302
