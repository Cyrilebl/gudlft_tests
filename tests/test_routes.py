from freezegun import freeze_time

# Index


def test_index_route(client):
    """Test if index route returns a 200 status."""
    response = client.get("/")
    assert response.status_code == 200


# Login


def test_login_valid_email(client):
    """Test with a valid email"""
    response = client.post("/login", data={"email": "test@example.com"})
    assert response.status_code == 302


def test_login_invalid_email(client):
    """Test with an invalid email"""
    response = client.post(
        "/login", data={"email": "wrong@example.com"}, follow_redirects=True
    )
    assert response.status_code == 200


def test_login_missing_email(client):
    """Test with no email provided"""
    response = client.post("/login", data={}, follow_redirects=True)
    assert response.status_code == 400


# Test Purchase Places

# Tests on valid scenarios


def test_purchase_places_with_valid_number(client):
    """Test with a club having enough points and a competition with enough places."""
    response = client.post(
        "/purchasePlaces",
        data={**client.common_data, "places": "3"},
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
        data={**client.common_data, "places": ""},
    )
    assert response.status_code == 200
    assert b"Please enter a number" in response.data


def test_purchase_places_with_negative_number(client):
    """Test with no negative number"""
    response = client.post(
        "/purchasePlaces",
        data={**client.common_data, "places": "-2"},
    )
    assert response.status_code == 200
    assert b"Please enter a number greater than zero" in response.data


def test_purchase_places_with_zero(client):
    """Test with zero"""
    response = client.post(
        "/purchasePlaces",
        data={**client.common_data, "places": "0"},
    )
    assert response.status_code == 200
    assert b"Please enter a number greater than zero" in response.data


@freeze_time("2030-01-01 12:00:00")
def test_purchase_in_past_competition(client):
    """Test booking places for a past competition"""
    response = client.post(
        "/purchasePlaces",
        data={
            **client.common_data,
            "places": 2,
        },
    )
    assert response.status_code == 200
    assert (
        b"This competition already took place on January 01 at 10:00 AM"
        in response.data
    )


def test_purchase_more_than_12_places(client):
    """Test to request more than 12 club points"""
    response = client.post(
        "/purchasePlaces",
        data={**client.common_data, "places": "13"},
    )
    assert response.status_code == 200
    assert b"You cannot book more than 12 places" in response.data


def test_purchase_places_request_above_club_points(client):
    """Test to request more club points than are available"""
    response = client.post(
        "/purchasePlaces",
        data={**client.common_data, "places": "11"},
    )
    assert response.status_code == 200
    assert b"Sorry, your club has 10 points left" in response.data


def test_purchase_places_request_above_competition_places(client):
    """Test to request more competition places than are available"""
    response = client.post(
        "/purchasePlaces",
        data={**client.common_data, "places": "6"},
    )
    assert response.status_code == 200
    assert b"Sorry, the competition has 5 places left" in response.data
