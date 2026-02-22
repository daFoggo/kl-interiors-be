def test_register_user(client):
    response = client.post(
        "/users/register",
        json={
            "username": "testuser",
            "email": "test@test.com",
            "password": "strongpassword123",
            "full_name": "Test User"
        },
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["email"] == "test@test.com"
    assert "id" in data
    assert data["role"] == "CUSTOMER"

def test_login_user(client):
    # First register
    client.post(
        "/users/register",
        json={
            "username": "loginuser",
            "email": "login@test.com",
            "password": "strongpassword123",
            "full_name": "Test Login"
        },
    )
    
    # Now login
    response = client.post(
        "/auth/login",
        data={
            "username": "loginuser",
            "password": "strongpassword123"
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_read_users_me(client):
    client.post(
        "/users/register",
        json={
            "username": "meuser",
            "email": "me@test.com",
            "password": "strongpassword123",
            "full_name": "Test Me"
        },
    )
    
    login_response = client.post(
        "/auth/login",
        data={
            "username": "meuser",
            "password": "strongpassword123"
        },
    )
    token = login_response.json()["access_token"]
    
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200, response.text
    assert response.json()["username"] == "meuser"

def test_unauthorized_access(client):
    response = client.get("/users/me")
    assert response.status_code == 401
