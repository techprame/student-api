STUDENT = {"name": "Aarav Sharma", "email": "aarav@school.com", "age": 16, "course": "Computer Science"}


def test_create_requires_login(client):
    res = client.post("/students", json=STUDENT)
    assert res.status_code == 401


def test_student_crud(client, auth_headers):
    # Create
    res = client.post("/students", json=STUDENT, headers=auth_headers)
    assert res.status_code == 201
    student_id = res.json()["data"]["id"]

    # Read (public)
    res = client.get(f"/students/{student_id}")
    assert res.status_code == 200
    assert res.json()["data"]["name"] == STUDENT["name"]

    # Update
    updated = {**STUDENT, "age": 17}
    res = client.put(f"/students/{student_id}", json=updated, headers=auth_headers)
    assert res.status_code == 200
    assert res.json()["data"]["age"] == 17

    # Delete
    res = client.delete(f"/students/{student_id}", headers=auth_headers)
    assert res.status_code == 200
    assert client.get(f"/students/{student_id}").status_code == 404


def test_duplicate_email(client, auth_headers):
    client.post("/students", json=STUDENT, headers=auth_headers)
    res = client.post("/students", json=STUDENT, headers=auth_headers)
    assert res.status_code == 409


def test_validation_error(client, auth_headers):
    res = client.post("/students", json={**STUDENT, "age": 3, "email": "not-an-email"}, headers=auth_headers)
    assert res.status_code == 422
    fields = {err["field"] for err in res.json()["data"]}
    assert fields == {"age", "email"}


def test_list_and_search(client, auth_headers):
    client.post("/students", json=STUDENT, headers=auth_headers)
    client.post(
        "/students",
        json={"name": "Diya Patel", "email": "diya@school.com", "age": 15, "course": "Mathematics"},
        headers=auth_headers,
    )

    assert len(client.get("/students").json()["data"]) == 2

    res = client.get("/students", params={"search": "math"})
    names = [s["name"] for s in res.json()["data"]]
    assert names == ["Diya Patel"]


def test_student_not_found(client):
    res = client.get("/students/999")
    assert res.status_code == 404
    assert res.json()["message"] == "Student not found"
