def test_create_category_admin(client, admin_token, db_session):
    response = client.post(
        "/categories/",
        json={"name": "Sofa", "slug": "sofa", "description": "Comfortable sofas"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 201
    assert response.json()["payload"]["name"] == "Sofa"

def test_create_category_customer(client, customer_token, db_session):
    response = client.post(
        "/categories/",
        json={"name": "Bed", "slug": "bed"},
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    assert response.status_code == 403

def test_get_categories(client, db_session):
    client.get("/categories/")

def test_update_category_admin(client, admin_token, db_session):
    client.post(
        "/categories/",
        json={"name": "Table", "slug": "table"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    cat = client.get("/categories/").json()["payload"]["data"][0]
    
    response = client.put(
        f"/categories/{cat['id']}",
        json={"name": "Table1", "slug": "table1"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert response.json()["payload"]["name"] == "Table1"

def test_delete_category_admin(client, admin_token, db_session):
    # Ensure there is a category
    client.post(
        "/categories/",
        json={"name": "Chair", "slug": "chair"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    cats = client.get("/categories/").json()["payload"]["data"]
    cat_id = cats[-1]['id']
    
    response = client.delete(
        f"/categories/{cat_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 204
