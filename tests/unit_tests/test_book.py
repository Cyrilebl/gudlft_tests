import pytest


def test_book(client):
    club_name = "Club Test"
    competition_name = "Competition Test"

    response = client.get(
        f"/book/{club_name}/{competition_name}", follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Places available:" in response.data


@pytest.mark.parametrize(
    "club_name, competition_name",
    [
        ("Club Test", "Invalid Competition Test"),
        ("Invalid Club Test", "Competition Test"),
    ],
)
def test_book_with_invalid_data(client, club_name, competition_name):
    response = client.get(f"/book/{club_name}/{competition_name}")
    assert response.status_code == 200
    assert b"Something went wrong - Please try again" in response.data
