PRODUCT = {"name": "Notebook", "price": 50.0, "stock": 200}


def test_create_requires_login(client):
    res = client.post("/products", json=PRODUCT)
    assert res.status_code == 401


def test_product_crud(client, auth_headers):
    res = client.post("/products", json=PRODUCT, headers=auth_headers)
    assert res.status_code == 201
    product_id = res.json()["data"]["id"]

    res = client.put(f"/products/{product_id}", json={**PRODUCT, "stock": 150}, headers=auth_headers)
    assert res.status_code == 200
    assert res.json()["data"]["stock"] == 150

    res = client.delete(f"/products/{product_id}", headers=auth_headers)
    assert res.status_code == 200
    assert client.get(f"/products/{product_id}").status_code == 404


def test_search(client, auth_headers):
    client.post("/products", json=PRODUCT, headers=auth_headers)
    client.post("/products", json={"name": "Calculator", "price": 650.0, "stock": 35}, headers=auth_headers)

    res = client.get("/products", params={"search": "calc"})
    assert [p["name"] for p in res.json()["data"]] == ["Calculator"]


def test_invalid_price(client, auth_headers):
    res = client.post("/products", json={**PRODUCT, "price": -5}, headers=auth_headers)
    assert res.status_code == 422
