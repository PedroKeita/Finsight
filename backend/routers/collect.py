from fastapi import APIRouter, HTTPException, Query
from collector import save_prices
from database import SessionLocal
from models import Asset
from cache import invalidate_cache

router = APIRouter(prefix="/collect", tags=["Collect"])

@router.post("/all", summary="Atualiza dados de todos os ativos cadastrados")
def collect_all_assets(period: str = Query(default="1y", pattern="^(1y|6m|3m)$")):
    
    db = SessionLocal()

    try:

        assets = db.query(Asset).all()
        results = []

        for asset in assets:
            try:

                save_prices(asset.ticker, period)
                invalidate_cache(asset.ticker)
                results.append({"ticker": asset.ticker, "status": "ok"})

            except Exception as e:

                results.append({"ticker": asset.ticker, "status": "erro", "detail": str(e)})

        return {"updated": len(results), "results": results}
    
    finally:
        db.close()

@router.post("/{ticker}", summary="Dispara coleta de dados de um ativo")
def collect(ticker: str, period: str = Query(default="1y", pattern="^(1y|6m|3m)$")):

    try:

        save_prices(ticker, period)
        invalidate_cache(ticker)

        return {"status": "ok", "message": f"Dados de {ticker} coletados com sucesso"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

