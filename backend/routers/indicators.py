from fastapi import APIRouter, HTTPException, Query
from indicators import get_indicators
from cache import get_cache, set_cache

router = APIRouter(prefix="/indicators", tags=["Indicators"])

@router.get("/{ticker}", summary="Retorna indicadores financeiros de um ativo")
def get_asset_indicators(ticker: str, period: str = Query(default="1y", pattern="^(1y|6m|3m)$")):
    cache_key = f"indicators:{ticker}:{period}"
    cached = get_cache(cache_key)
    if cached:
        return cached

    try:
        result = get_indicators(ticker, period)
        set_cache(cache_key, result)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))