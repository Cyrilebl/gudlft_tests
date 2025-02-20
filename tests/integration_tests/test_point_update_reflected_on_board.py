import server


def test_points_update(client):
    places_booked = 3

    response = client.post(
        "/purchase-places",
        data={**client.common_data, "places": str(places_booked)},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Great - booking complete!" in response.data

    assert server.clubs[0]["points"] == "7"
    assert server.competitions[0]["numberOfPlaces"] == "2"
