from src.app import app


def test_home():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert response.json["application"] == "Cloud-Native Banking Platform"


def test_health():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def test_get_accounts():
    client = app.test_client()

    response = client.get("/accounts")

    assert response.status_code == 200
    assert len(response.json) >= 2


def test_create_account():
    client = app.test_client()

    response = client.post(
        "/accounts",
        json={"name": "Test User"}
    )

    assert response.status_code == 201
    assert response.json["name"] == "Test User"


def test_get_account():
    client = app.test_client()

    response = client.get("/accounts/10001")

    assert response.status_code == 200
    assert response.json["account_id"] == "10001"


def test_create_transaction():
    client = app.test_client()

    response = client.post(
        "/transactions",
        json={
            "from_account": "10001",
            "to_account": "10002",
            "amount": 5000
        }
    )

    assert response.status_code == 201
    assert response.json["status"] == "SUCCESS"


def test_invalid_transaction():
    client = app.test_client()

    response = client.post(
        "/transactions",
        json={
            "from_account": "10001",
            "to_account": "10002",
            "amount": -500
        }
    )

    assert response.status_code == 400