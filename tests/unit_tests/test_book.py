def test_book_with_valid_data(client):
    competition_name = "Competition Test"
    club_name = "Club Test"
    response = client.get(
        f"/book/{club_name}/{competition_name}", follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Places available:" in response.data


def test_book_with_invalid_club(client):
    competition_name = "Invalid Competition Test"
    club_name = "Club Test"
    response = client.get(f"/book/{club_name}/{competition_name}")
    assert response.status_code == 200
    assert b"Something went wrong - Please try again" in response.data


def test_book_invalid_competition(client):
    competition_name = "Competition Test"
    club_name = "Invalid Club Test"
    response = client.get(f"/book/{club_name}/{competition_name}")
    assert b"Something went wrong - Please try again" in response.data
