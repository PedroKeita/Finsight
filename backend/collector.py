import yfinance as yf
import pandas as pd
from datetime import datetime
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