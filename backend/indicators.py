import pandas as pd
import numpy as np
from sqlalchemy import text
from database import engine
import os

TRADING_DAYS = 252

def get_prices(ticker: str, period: str = "1y") -> pd.DataFrame:
    """
    Busca a série de preços de um ativo no banco de dados.
    """

    period_map = {
        "1y": "365 days",
        "6m": "180 days",
        "3m": "90 days"
    }

    interval = period_map.get(period, "365 days")

    query = text(f"""
    SELECT p.date, p.close_price
    FROM prices p
    JOIN assets a ON a.id = p.asset_id
    WHERE a.ticker = :ticker
    AND p.date >= CURRENT_DATE - INTERVAL '{interval}'
    ORDER BY p.date
    """)
    
    df = pd.read_sql(query, engine, params={"ticker": ticker})

    if df.empty:
        raise ValueError(f"Nenhum preço encontrado para {ticker}")
    
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    return df

def calculate_returns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula os retornos percentuais diários.
    """

    df ["returns"] = df["close_price"].pct_change()
    df = df.dropna()

    return df

def cumulative_return(df: pd.DataFrame) -> float:
    """
    Retorno acumulado do período.
    """

    first_price = df["close_price"].iloc[0]
    last_price = df["close_price"].iloc[-1]

    return (last_price / first_price) - 1

def volatility(df: pd.DataFrame) -> float:
    """
    Volatilidade anualizada usando 252 dias úteis.
    """

    return df["returns"].std() * np.sqrt(TRADING_DAYS)

def max_drawdown(df: pd.DataFrame) -> float:
    """
    Calcula o maior drawdown do ativo.
    """

    cumulative = (1 + df["returns"]).cumprod()

    peak = cumulative.cummax()

    drawdown = (cumulative - peak) / peak

    return drawdown.min()

def sharpe_ratio(df: pd.DataFrame) -> float:
    """
    Calcula o Sharpe Ratio usando taxa livre de risco.
    """

    risk_free_rate = float(os.getenv("RISK_FREE_RATE", 0.13))

    excess_return = (df["returns"].mean() * TRADING_DAYS) - risk_free_rate

    vol = df["returns"].std() * np.sqrt(TRADING_DAYS)

    if vol == 0:
        return 0
    
    return excess_return / vol

def get_indicators(ticker: str, period: str = "1y"):
    """
    Retorna todos os indicadores de um ativo.
    """

    df = get_prices(ticker, period)
    df = calculate_returns(df)

    result = {
        "return": round(cumulative_return(df) * 100, 2),
        "volatility": round(volatility(df) * 100, 2),
        "drawdown": round(max_drawdown(df) * 100, 2),
        "sharpe": round(sharpe_ratio(df), 2),
        "daily_variation": daily_variation(df)
    }

    return result

def daily_variation(df: pd.DataFrame) -> float:
    """
    Calcula a variação do último dia em relação ao dia anterior.
    """

    if len(df) < 2:
        return 0.0
    
    last = df["close_price"].iloc[-1]
    prev = df["close_price"].iloc[-2]

    return round(((last - prev) / prev) * 100, 2)


