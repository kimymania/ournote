from fastapi.testclient import TestClient


def test_signup(client: TestClient) -> None:
    form_data = {
        "username": "admin",
        "password": "password",
    }
    res = client.post("/signup", data=form_data)
    expected_response = {"username": "admin"}
    assert res.status_code == 200
    assert res.json() == expected_response


def test_signup_conflict(client: TestClient) -> None:
    form_data = {
        "username": "admin",
        "password": "password",
    }
    res = client.post("/signup", data=form_data)
    expected_response = {"detail": "Conflict"}
    assert res.status_code == 409
    assert res.json() == expected_response


def test_login_wrong_username(client: TestClient) -> None:
    form_data = {
        "username": "foobar",
        "password": "password",
    }
    res = client.post("/login", data=form_data)
    expected_response = {"detail": "Unauthorized"}

    assert res.status_code == 401
    assert res.json() == expected_response


def test_login_wrong_password(client: TestClient) -> None:
    form_data = {
        "username": "admin",
        "password": "gibbledigob",
    }
    res = client.post("/login", data=form_data)
    expected_response = {"detail": "Unauthorized"}

    assert res.status_code == 401
    assert res.json() == expected_response


def test_login(client: TestClient) -> None:
    form_data = {
        "username": "admin",
        "password": "password",
    }
    res = client.post("/login", data=form_data)
    expected_response = {
        "username": "admin",
    }

    assert res.status_code == 200
    assert res.json() == expected_response
    assert "set-cookie" in res.headers

    set_cookie_header = res.headers.get("set-cookie")
    assert "Max-Age=1800" in set_cookie_header
    assert "HttpOnly" in set_cookie_header
    assert "Secure" in set_cookie_header
