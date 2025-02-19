import pytest
from freezegun import freeze_time


class TestPurchasePlaces:
    @pytest.fixture(autouse=True)
    def setup_method(self, client):
        self.client = client
        self.common_data = client.common_data

    def test_purchase_places_with_valid_number(self):
        response = self.client.post(
            "/purchase-places",
            data={**self.common_data, "places": "3"},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Great - booking complete!" in response.data

    @pytest.mark.parametrize(
        "places, expected_message",
        [
            ("", "Please enter a number"),
            ("-2", "Please enter a number greater than zero"),
            ("0", "Please enter a number greater than zero"),
            ("13", "You cannot book more than 12 places"),
            ("11", "Sorry, your club has 10 points left"),
            ("6", "Sorry, the competition has 5 places left"),
        ],
    )
    def test_purchase_places_invalid_input(self, places, expected_message):
        response = self.client.post(
            "/purchase-places",
            data={**self.common_data, "places": places},
        )
        assert response.status_code == 200
        assert expected_message.encode() in response.data

    @freeze_time("2030-01-01 12:00:00")
    def test_purchase_in_past_competition(self):
        response = self.client.post(
            "/purchase-places",
            data={
                **self.common_data,
                "places": 2,
            },
        )
        assert response.status_code == 200
        assert (
            b"This competition already took place on January 01, 2027, at 10:00 AM"
            in response.data
        )
