import pytest
from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch

client = TestClient(app)

def test_get_assets():

    response = client.get("/assets/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_get_assets_tem_campos():

    response = client.get("/assets/")
    asset = response.json()[0]

    assert "ticker" in asset
    assert "name" in asset
    assert "category" in asset
    assert "logo_url" in asset

def test_get_prices_valido():

    response = client.get("/prices/PETR4.SA?period=1y")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_get_prices_ticker_invalido():

    response = client.get("/prices/TICKER_INVALIDO")
    assert response.status_code == 404

def test_get_prices_periodo_invalido():

    response = client.get("/prices/PETR4.SA?period=10y")
    assert response.status_code == 422

def test_get_indicators_valido():

    response = client.get("/indicators/PETR4.SA?period=1y")
    assert response.status_code == 200
    data = response.json()

    assert "return" in data
    assert "volatility" in data
    assert "drawdown" in data
    assert "sharpe" in data

def test_get_indicators_ticker_invalido():

    response = client.get("/indicators/TICKER_INVALIDO")
    assert response.status_code == 404

def test_post_collect_valido():

    with patch("routers.collect.save_prices") as mock_save:

        mock_save.return_value = None
        response = client.post("/collect/PETR4.SA?period=1y")

        assert response.status_code == 200
        assert response.json()["status"] == "ok"

def test_post_collect_all():

    with patch("routers.collect.save_prices") as mock_save:

        mock_save.return_value = None
        response = client.post("/collect/all?period=1y")

        assert response.status_code == 200
        assert "updated" in response.json()
        assert "results" in response.json()

def test_post_portfolio_valido():
    response = client.post("/portfolio/", json={
        "allocations": [
            {"ticker": "PETR4.SA", "weight": 0.50},
            {"ticker": "VALE3.SA", "weight": 0.50}
        ],
        "period": "1y"
    })
    assert response.status_code == 200
    data = response.json()
    assert "return" in data
    assert "volatility" in data
    assert "sharpe" in data
    assert "history" in data
    assert "benchmark_history" in data

def test_post_portfolio_pesos_invalidos():
    response = client.post("/portfolio/", json={
        "allocations": [
            {"ticker": "PETR4.SA", "weight": 0.50},
            {"ticker": "VALE3.SA", "weight": 0.30}
        ],
        "period": "1y"
    })
    assert response.status_code == 400

def test_post_portfolio_periodo_invalido():
    response = client.post("/portfolio/", json={
        "allocations": [
            {"ticker": "PETR4.SA", "weight": 1.0}
        ],
        "period": "10y"
    })
    assert response.status_code == 200

def test_get_correlation():
    response = client.get("/correlation/?period=1y")
    assert response.status_code == 200
    data = response.json()
    assert "tickers" in data
    assert "matrix" in data

def test_get_correlation_periodo_invalido():
    response = client.get("/correlation/?period=10y")
    assert response.status_code == 422