def test_register_user(client):
    response = client.post(
        "/users/register",
        json={
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
            "email": "login@test.com",
            "password": "strongpassword123",
            "full_name": "Test Login"
        },
    )
    
    # Now login
    response = client.post(
        "/auth/login",
        data={
            "username": "login@test.com",
            "password": "strongpassword123"
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"

def test_read_users_me(client):
    client.post(
        "/users/register",
        json={
            "email": "me@test.com",
            "password": "strongpassword123",
            "full_name": "Test Me"
        },
    )
    
    login_response = client.post(
        "/auth/login",
        data={
            "username": "me@test.com",
            "password": "strongpassword123"
        },
    )
    token = login_response.json()["access_token"]
    
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200, response.text
    assert response.json()["email"] == "me@test.com"

def test_unauthorized_access(client):
    response = client.get("/users/me")
    assert response.status_code == 401

def test_register_with_phone(client):
    response = client.post(
        "/users/register",
        json={
            "phone_number": "+84123456789",
            "password": "strongpassword123",
            "full_name": "Phone User"
        },
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["phone_number"] == "+84123456789"
    assert data["email"] is None

def test_login_with_phone(client):
    client.post(
        "/users/register",
        json={
            "phone_number": "+84987654321",
            "password": "strongpassword123",
            "full_name": "Phone Login User"
        },
    )
    
    response = client.post(
        "/auth/login",
        data={
            "username": "+84987654321",
            "password": "strongpassword123"
        },
    )
    assert response.status_code == 200, response.text
    assert "access_token" in response.json()

def test_register_without_email_and_phone(client):
    response = client.post(
        "/users/register",
        json={
            "password": "strongpassword123",
            "full_name": "No Contact User"
        },
    )
    assert response.status_code == 422, response.text

def test_refresh_token(client):
    # Register and login
    client.post(
        "/users/register",
        json={
            "email": "refresh@test.com",
            "password": "strongpassword123",
            "full_name": "Test Refresh"
        },
    )
    
    login_response = client.post(
        "/auth/login",
        data={
            "username": "refresh@test.com",
            "password": "strongpassword123"
        },
    )
    assert login_response.status_code == 200
    refresh_token = login_response.json()["refresh_token"]
    
    # Refresh the token
    refresh_response = client.post(
        "/auth/refresh",
        json={"refresh_token": refresh_token}
    )
    assert refresh_response.status_code == 200
    data = refresh_response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    
    # Ensure old refresh token cannot be used as access token
    failed_access_response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {refresh_token}"}
    )
    assert failed_access_response.status_code == 401
