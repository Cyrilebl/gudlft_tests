def test_login_and_logout(client):
    # Step 1: Login
    email = "test@example.com"
    response = client.post("/login", data={"email": email}, follow_redirects=True)
    assert response.status_code == 200
    assert f"Welcome, {email}".encode() in response.data

    # Step 2: Logout
    response = client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert b"Welcome to the GUDLFT Registration Portal!" in response.data
