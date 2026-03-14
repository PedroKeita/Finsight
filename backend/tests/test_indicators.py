import pytest
import pandas as pd
import numpy as np
from indicators import (
    calculate_returns,
    cumulative_return,
    volatility,
    max_drawdown,
    sharpe_ratio
)
from unittest.mock import patch, MagicMock
from collector import fetch_prices, save_prices


# Dados fictícios para teste
def make_df(prices):
    """Cria um DataFrame de preços fictício para testes."""

    df = pd.DataFrame({
        "date": pd.date_range(start="2024-01-01", periods=len(prices)),
        "close_price": prices
    })

    return calculate_returns(df)

# Retorno Acumulado

def test_cumulative_return_positivo():

    df = make_df([100, 110, 120, 130])
    result = cumulative_return(df)
   
    assert round(result, 4) == round(130/110 - 1, 4)

def test_cumulative_return_negativo():

    df = make_df([100, 90, 80, 70])
    result = cumulative_return(df)
    
    assert round(result, 4) == round(70/90 - 1, 4)

def test_cumulative_return_neutro():

    df = make_df([100, 100, 100, 100])
    result = cumulative_return(df)
    
    assert round(result, 4) == 0.0

# Volatilidade

def test_volatility_retorna_positivo():

    df = make_df([100, 102, 98, 105, 95, 110])
    result = volatility(df)

    assert result > 0

def test_volatility_serie_constante():

    df = make_df([100, 100, 100, 100, 100])
    result = volatility(df)

    assert result == 0.0  # Se não houver variação, não terá volatilidade


# Drawdown

def test_max_drawdown_retorna_negativo():

    df = make_df([100, 120, 80, 110, 90])
    result = max_drawdown(df)

    assert result < 0

def test_max_drawdown_sem_queda():

    df = make_df([100, 110, 120, 130, 140])
    result = max_drawdown(df)

    assert result == 0.0


# Sharpe

def test_sharpe_retorna_float():

    df = make_df([100, 102, 104, 106, 108, 110])
    result = sharpe_ratio(df)

    assert isinstance(result, float)

def test_sharpe_volatilidade_zero():

    df = make_df([100, 100, 100, 100, 100])
    result = sharpe_ratio(df)

    assert result == 0

def test_fetch_prices_retorna_dataframe():
    """Testa se fetch_prices retorna DataFrame com as colunas corretas."""

    with patch("collector.yf.Ticker") as mock_ticker:
        mock_history = pd.DataFrame({
            "Close": [100.0, 110.0, 120.0],
            "Volume": [1000, 2000, 3000]
        }, index=pd.date_range("2024-01-01", periods=3))

        mock_ticker.return_value.history.return_value = mock_history

        df = fetch_prices("PETR4.SA", "1y")

        assert not df.empty
        assert "date" in df.columns
        assert "close_price" in df.columns
        assert "volume" in df.columns

def test_fetch_prices_ticker_invalido():
    """Testa se fetch_prices retorna DataFrame vazio para ticker inválido."""
    
    with patch("collector.yf.Ticker") as mock_ticker:
        mock_ticker.return_value.history.return_value = pd.DataFrame()

        df = fetch_prices("TICKER_INVALIDO", "1y")

        assert df.empty