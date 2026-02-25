def test_create_product_admin(client, admin_token, db_session):
    # First create a category to attach the product to
    cat_res = client.post(
        "/categories/",
        json={"name": "Furniture", "slug": "furniture", "description": "All furniture"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    cat_id = cat_res.json()["payload"]["id"]

    response = client.post(
        "/products/",
        json={
            "category_id": cat_id,
            "name": "Luxury Sofa",
            "slug": "luxury-sofa",
            "price": 1000.50,
            "stock_quantity": 10,
            "status": "PUBLISHED"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 201
    assert response.json()["payload"]["name"] == "Luxury Sofa"

def test_create_product_customer(client, customer_token, db_session):
    response = client.post(
        "/products/",
        json={
            "category_id": "123e4567-e89b-12d3-a456-426614174000",
            "name": "Customer Product",
            "slug": "cust-prod",
            "price": 100
        },
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    assert response.status_code == 403

def test_get_products(client, admin_token):
    # Public route
    res = client.get("/products/")
    assert res.status_code == 200

def test_update_product_admin(client, admin_token):
    cat_res = client.post(
        "/categories/",
        json={"name": "Lighting", "slug": "lighting"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    cat_id = cat_res.json()["payload"]["id"]

    prod_res = client.post(
        "/products/",
        json={
            "category_id": cat_id,
            "name": "Lamp",
            "slug": "lamp",
            "price": 50
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    prod_id = prod_res.json()["payload"]["id"]

    update_res = client.put(
        f"/products/{prod_id}",
        json={
            "category_id": cat_id,
            "name": "Super Lamp",
            "slug": "super-lamp",
            "price": 55,
            "status": "PUBLISHED"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert update_res.status_code == 200
    assert update_res.json()["payload"]["name"] == "Super Lamp"

def test_delete_product_admin(client, admin_token):
    cat_res = client.post(
        "/categories/",
        json={"name": "Decor", "slug": "decor"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    cat_id = cat_res.json()["payload"]["id"]

    prod_res = client.post(
        "/products/",
        json={
            "category_id": cat_id,
            "name": "Vase",
            "slug": "vase",
            "price": 20
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    prod_id = prod_res.json()["payload"]["id"]

    del_res = client.delete(
        f"/products/{prod_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert del_res.status_code == 204
