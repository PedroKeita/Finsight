from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal
from models import Asset
from indicators import get_indicators
from collector import save_prices
from sqlalchemy import text
from database import engine
import pandas as pd

app = FastAPI(
    title = "Finsight API",
    description="API de análise de carteiras de investimentos",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Assets
@app.get("/assets", summary="Lista todos os ativos cadastrados")
def list_assets():
    db = SessionLocal()
    try:
        assets = db.query(Asset).all()
        return [
            {"id": a.id, "ticker": a.ticker, "name": a.name, "category": a.category}
            for a in assets
        ]
    finally:
        db.close()


# Prices

@app.get("/prices/{ticker}", summary="Retorna histórico de preços de um ativo")
def get_prices(ticker: str, period: str = Query(default="1y", pattern="^(1y|6m|3m)$")):
    period_map = {"1y": "365 days", "6m": "180 days", "3m": "90 days"}
    interval = period_map[period]

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
        raise HTTPException(status_code=404, detail=f"Ativo '{ticker} não encontrado")
    
    df["date"] = df["date"].astype(str)
    return df.to_dict(orient="records")


# Indicators
@app.get("/indicators/{ticker}", summary="Retorna indicadores financeiros de um ativo")
def get_asset_indicators(ticker: str, period: str = Query(default="1y", pattern="^(1y|6m|3m)$")):
    try:
        return get_indicators(ticker, period)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# Collect
@app.post("/collect/{ticker}", summary="Dispara coleta de dados de um ativo")
def collect(ticker: str, period: str = Query(default="1y", pattern="^(1y|6m|3m)$")):
    try:
        save_prices(ticker, period)
        return {"status": "ok", "message": f"Dados de {ticker} coletados com sucesso!!!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))