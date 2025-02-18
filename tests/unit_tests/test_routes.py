def test_index_route(client):
    response = client.get("/")
    assert response.status_code == 200


def test_club_board(client):
    response = client.get("/club-board")
    assert response.status_code == 200


def test_home(client):
    with client.session_transaction() as sess:
        sess["club_name"] = "Club Test"

    response = client.get("/home")
    assert response.status_code == 200


def test_logout(client):
    response = client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert b"Welcome to the GUDLFT Registration Portal!" in response.data
