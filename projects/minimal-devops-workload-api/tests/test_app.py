import app.main as main


def test_health_endpoint_returns_ok():
    client = main.app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"
    assert response.get_json()["service"] == "minimal-devops-workload-api"


def test_ready_endpoint_returns_ready_when_database_is_reachable(monkeypatch):
    def fake_check_db():
        return None

    monkeypatch.setattr(main, "check_db", fake_check_db)

    client = main.app.test_client()
    response = client.get("/ready")

    assert response.status_code == 200
    assert response.get_json()["status"] == "ready"
    assert response.get_json()["database"] == "reachable"


def test_db_health_endpoint_returns_ok_when_database_is_reachable(monkeypatch):
    def fake_check_db():
        return None

    monkeypatch.setattr(main, "check_db", fake_check_db)

    client = main.app.test_client()
    response = client.get("/db-health")

    assert response.status_code == 200
    assert response.get_json()["database"] == "ok"
    assert response.get_json()["host"] == "postgres"
    assert response.get_json()["name"] == "appdb"


def test_ready_endpoint_returns_503_when_database_is_unreachable(monkeypatch):
    def fake_check_db():
        raise Exception("database connection failed")

    monkeypatch.setattr(main, "check_db", fake_check_db)

    client = main.app.test_client()
    response = client.get("/ready")

    assert response.status_code == 503
    assert response.get_json()["status"] == "not_ready"
    assert response.get_json()["database"] == "unreachable"
