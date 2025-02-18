def test_login_valid_email(client):
    """Test with a valid email"""
    response = client.post(
        "/login", data={"email": "test@example.com"}, follow_redirects=True
    )
    assert response.request.path == "/home"
    assert response.status_code == 200
    assert b"Welcome, test@example.com" in response.data


def test_login_invalid_email(client):
    """Test with an invalid email"""
    response = client.post(
        "/login",
        data={"email": "wrong@example.com"},
    )
    assert response.status_code == 200
    assert b"Email not found" in response.data


def test_login_missing_email(client):
    """Test with no email provided"""
    response = client.post("/login", data={"email": ""})
    assert response.status_code == 200
    assert b"Email is required" in response.data
