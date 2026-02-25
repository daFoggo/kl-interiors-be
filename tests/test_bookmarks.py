def test_add_bookmark(client, admin_token, customer_token):
    # Admin creates category and product
    cat_res = client.post(
        "/categories/",
        json={"name": "Chairs", "slug": "chairs"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    cat_id = cat_res.json()["payload"]["id"]

    prod_res = client.post(
        "/products/",
        json={
            "category_id": cat_id,
            "name": "Dining Chair",
            "slug": "dining-chair",
            "price": 75.00
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    prod_id = prod_res.json()["payload"]["id"]

    # Customer bookmarks the product
    bm_res = client.post(
        "/bookmarks/",
        json={"product_id": prod_id},
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    assert bm_res.status_code == 201

    # Customer queries their bookmarks
    get_res = client.get(
        "/bookmarks/",
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    assert get_res.status_code == 200
    data = get_res.json()["payload"]["data"]
    assert len(data) > 0
    assert data[0]["product_id"] == prod_id

    # Duplicate bookmark should fail
    bm_res2 = client.post(
        "/bookmarks/",
        json={"product_id": prod_id},
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    assert bm_res2.status_code == 400

def test_delete_bookmark(client, admin_token, customer_token):
    # Create product to bookmark
    cat_res = client.post(
        "/categories/",
        json={"name": "Kitchen", "slug": "kitchen"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    cat_id = cat_res.json()["payload"]["id"]

    prod_res = client.post(
        "/products/",
        json={"category_id": cat_id, "name": "Island", "slug": "island", "price": 500},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    prod_id = prod_res.json()["payload"]["id"]

    # Bookmark it
    bm_res = client.post(
        "/bookmarks/",
        json={"product_id": prod_id},
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    bm_id = bm_res.json()["payload"]["id"]

    # Delete it
    del_res = client.delete(
        f"/bookmarks/{bm_id}",
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    assert del_res.status_code == 204

    # Fetch again, should be empty
    get_res = client.get(
        "/bookmarks/",
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    assert len(get_res.json()["payload"]["data"]) == 0
