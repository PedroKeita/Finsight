import yfinance as yf
import pandas as pd
from datetime import datetime
from sqlalchemy.dialects.postgresql import insert
from database import SessionLocal, engine
from models import Asset, Price
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ASSETS = [
    {"ticker": "PETR4.SA", "name": "Petrobras",          "category": "ação"},
    {"ticker": "VALE3.SA", "name": "Vale",                "category": "ação"},
    {"ticker": "ITUB4.SA", "name": "Itaú Unibanco",      "category": "ação"},
    {"ticker": "BBAS3.SA", "name": "Banco do Brasil",    "category": "ação"},
    {"ticker": "^BVSP",    "name": "Ibovespa",           "category": "índice"},
]

def fetch_prices(ticker: str, period: str = "1y") -> pd.DataFrame:
    """
    Busca histórico de preços de um ativo no Yahoo Finance
    Retorna um DataFrame com colunas: date, close_price, volume
    """

    try:
        logger.info(f"Coletando dados de {ticker}...")
        asset = yf.Ticker(ticker)
        df = asset.history(period=period)

        if df.empty:
            logger.warning(f"Nenhum dado encontrado para {ticker}")
            return pd.DataFrame()

        df = df[["Close", "Volume"]].reset_index()
        df.columns = ["date", "close_price", "volume"]
        df["date"] = pd.to_datetime(df["date"]).dt.date

        logger.info(f"{len(df)} registros coletados para {ticker}")
        return df
    
    except Exception as e:
        logger.error(f"Erro ao coletar{ticker}: {e}")
        return pd.DataFrame()

def save_prices(ticker: str, period: str = "1y"):
    """Salva os preços de um ativo no banco, sem duplicar registros."""
    db = SessionLocal()
    try:
        # Buscar ativo no banco através do ticker
        asset = db.query(Asset).filter(Asset.ticker == ticker).first()
        if not asset:
            logger.error(f"Ativo {ticker} não encontrado no banco")
            return
    
        # Busca os preços no Yahoo Finance
        df = fetch_prices(ticker, period)
        if df.empty:
            return
        

        # Upsert
        for _, row in df.iterrows():
            stmt = insert(Price).values(
                asset_id    = asset.id,
                date        = row["date"],
                close_price = row["close_price"],
                volume      = int(row["volume"]) if pd.notna(row["volume"]) else None
            ).on_conflict_do_nothing(
                index_elements=["asset_id", "date"]
            )
            db.execute(stmt)
        
        db.commit()
        logger.info(f"Preços de {ticker} salvos com sucesso!!!")

    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao salvar preços de {ticker}: {e}")
    finally:
        db.close()

def collect_all(period: str = "1y"):
    """Coleta e salva preços de todos os ativos cadastrados."""
    for asset in ASSETS:
        save_prices(asset["ticker"], period)

if __name__ == "__main__":
    collect_all()