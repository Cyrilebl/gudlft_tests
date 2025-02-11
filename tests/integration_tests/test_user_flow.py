def test_full_user_flow(client):
    # Step 1: Check club board
    response = client.get("/club-board")
    assert response.status_code == 200

    # Step 2: Login
    response = client.post(
        "/login", data={"email": "test@example.com"}, follow_redirects=True
    )
    assert b"Welcome" in response.data
    assert response.status_code == 200

    # Step 3: Book places for a competition
    response = client.post(
        "/purchase-places",
        data={**client.common_data, "places": "3"},
        follow_redirects=True,
    )
    assert b"Great - booking complete!" in response.data
    assert response.status_code == 200

    # Step 4: Logout
    response = client.get("/logout", follow_redirects=True)
    assert b"Welcome to the GUDLFT Registration Portal!" in response.data
    assert response.status_code == 200


def test_booking_without_login(client):
    response = client.post(
        "/purchase-places",
        data={**client.common_data},
        follow_redirects=True,
    )

    assert response.status_code == 400
