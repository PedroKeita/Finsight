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

    query