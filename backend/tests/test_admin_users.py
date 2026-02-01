def test_admin_access_denied_users(client, auth_token):
    res = client.get("/admin/users", headers={
        "Authorization": f"Bearer {auth_token}"
    })

    assert res.status_code == 403


def test_admin_email_filter(client, admin_token, many_users):
    res = client.get("/admin/users?page=1&limit=10&email=email5@example.com", headers={
        "Authorization": f"Bearer {admin_token}"
    })
    data = res.get_json()

    assert data["data"]["users"][0]["email"] == "email5@example.com"
    assert res.status_code == 200


def test_admin_username_sort(client, admin_token, many_users):
    res = client.get("/admin/users?page=1&limit=10&sort=username", headers={
        "Authorization": f"Bearer {admin_token}"
    })
    data = res.get_json()
    
    assert data["data"]["users"][2]["username"] <= data["data"]["users"][3]["username"]
    assert res.status_code == 200