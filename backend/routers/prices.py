from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import text
from database import engine
from cache import get_cache, set_cache
import pandas as pd

router = APIRouter(prefix="/prices", tags=["Prices"])

PERIOD_MAP = {
    "1y": "365 days",
    "6m": "180 days",
    "3m": "90 days"
}

@router.get("/{ticker}", summary="Retorna histórico de preços de um ativo")
def get_prices(ticker: str, period: str = Query(default="1y", pattern="^(1y|6m|3m)$")):

    cache_key = f"prices:{ticker}:{period}"
    cached = get_cache(cache_key)

    if cached:
        return cached

    interval = PERIOD_MAP[period]

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
        raise HTTPException(status_code=404, detail=f"Ativo '{ticker}' não encontrado")

    df["date"] = df["date"].astype(str)
    result = df.to_dict(orient="records")
    set_cache(cache_key, result)

    return result