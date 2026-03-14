from fastapi import APIRouter, HTTPException, Query
from indicators import get_indicators

router = APIRouter(prefix="/indicators", tags=["Indicators"])

@router.get("/{ticker}", summary="Retorna indicadores financeiros de um ativo")
def get_asset_indicators(ticker: str, period: str = Query(default="1y", pattern="^(1y|6m|3m)$")):
    try:
        return get_indicators(ticker, period)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))