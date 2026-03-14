from fastapi import APIRouter, HTTPException, Query
from collector import save_prices

router = APIRouter(prefix="/collect", tags=["Collect"])

@router.post("/{ticker}", summary="Dispara coleta de dados de um ativo")
def collect(ticker: str, period: str = Query(default="1y", pattern="^(1y|6m|3m)$")):
    try:
        save_prices(ticker, period)
        return {"status": "ok", "message": f"Dados de {ticker} coletados com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))