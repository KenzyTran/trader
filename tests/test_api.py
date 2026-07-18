from fastapi.testclient import TestClient

from trader.api import app


client = TestClient(app)


def test_health():
    assert client.get("/api/health").json() == {"status": "ok"}


def test_unknown_trader_returns_404():
    response = client.get("/api/traders/unknown")
    assert response.status_code == 404


def test_market_status_has_expected_shape():
    payload = client.get("/api/market").json()
    assert payload["source"] in {"massive", "simulator"}
    assert isinstance(payload["is_market_open"], bool)


def test_trader_list_matches_original_frontend_contract():
    payload = client.get("/api/traders").json()
    assert payload[0].keys() == {"name", "lastname", "model_name"}


def test_trader_detail_matches_original_frontend_contract(monkeypatch, tmp_path):
    from trader.config import Settings

    test_settings = Settings(data_dir=tmp_path)
    monkeypatch.setattr("trader.database.settings", test_settings)
    response = client.get("/api/traders/Warren")
    assert response.status_code == 200
    payload = response.json()
    assert {"pnl", "holdings", "transactions", "time_series"} <= payload.keys()
