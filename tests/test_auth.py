USER = {"email": "student@school.com", "password": "secret123"}


def test_home(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json()["message"] == "Student Management API is running"


def test_register_login_and_me(client):
    res = client.post("/auth/register", json=USER)
    assert res.status_code == 201
    assert res.json()["data"]["email"] == USER["email"]

    res = client.post("/auth/login", json=USER)
    assert res.status_code == 200
    token = res.json()["data"]["access_token"]

    res = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert res.json()["data"]["email"] == USER["email"]


def test_register_duplicate_email(client):
    client.post("/auth/register", json=USER)
    res = client.post("/auth/register", json=USER)
    assert res.status_code == 409


def test_login_wrong_password(client):
    client.post("/auth/register", json=USER)
    res = client.post("/auth/login", json={**USER, "password": "wrong-password"})
    assert res.status_code == 401


def test_me_without_token(client):
    res = client.get("/auth/me")
    assert res.status_code == 401


def test_me_with_invalid_token(client):
    res = client.get("/auth/me", headers={"Authorization": "Bearer not-a-real-token"})
    assert res.status_code == 401
