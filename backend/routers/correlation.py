from fastapi import APIRouter, Query
from sqlalchemy import text
from database import engine
from cache import get_cache, set_cache 
import pandas as pd

router = APIRouter(prefix="/correlation", tags=["Correlation"])

@router.get("/", summary="Retorna matriz de correlação entre os ativos")
def get_correlation(period: str = Query(default="1y", pattern="^(1y|6m|3m)$")):

    cache_key = f"correlation:{period}"
    cached = get_cache(cache_key)

    if cached:
        return cached
    
    period_map = {"1y": "365 days", "6m": "180 days", "3m": "90 days"}
    interval = period_map[period]

    query = text(f"""
        SELECT a.ticker, p.date, p.close_price
        FROM prices p
        JOIN assets a ON a.id = p.asset_id
        WHERE p.date >= CURRENT_DATE - INTERVAL '{interval}'
        ORDER BY p.date
    """)

    df = pd.read_sql(query, engine)

    if df.empty:
        return {}
    
    # pivot -> linhas = datas e colunas = tickers
    pivot = df.pivot(index="date", columns="ticker", values="close_price")

    returns = pivot.pct_change().dropna()

    corr = returns.corr().round(2)

    tickers = corr.columns.tolist()
    matrix = []

    for ticker_row in tickers:
        row = []
        for ticker_col in tickers:
            row.append(corr.loc[ticker_row, ticker_col])
        matrix.append({"ticker": ticker_row, "values": row})
    
    result = {"tickers": tickers, "matrix": matrix}
    set_cache(cache_key, result)

    return result
    

    
