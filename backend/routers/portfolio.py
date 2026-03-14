from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from database import engine
from indicators import calculate_returns, volatility, sharpe_ratio
import pandas as pd
import numpy as np

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])

class Allocation(BaseModel):
    ticker: str
    weight: float

class PortfolioRequest(BaseModel):
    allocations: list[Allocation]
    period: str = "1y"

    model_config = {
        "json_schema_extra": {
            "example": {
                "allocations": [
                    {"ticker": "PETR4.SA", "weight": 0.40},
                    {"ticker": "VALE3.SA", "weight": 0.30},
                    {"ticker": "ITUB4.SA", "weight": 0.30}
                ],
                "period": "1y"
            }
        }
    }

@router.post("/", summary = "Simula o retorno de uma carteira com pesos definidos")
def simulate_portfolio(request: PortfolioRequest):

    #Validar se os pesos somam 100%
    total_weight = sum(a.weight for a in request.allocations)
    if not (0.99 <= total_weight <= 1.01):
        raise HTTPException(
            status_code=400,
            detail=f"Os pesos devem somar 100%. Total atual: {round(total_weight * 100, 2)}%"
        )
    
    period_map = {"1y": "365 days", "6m": "180 days", "3m": "90 days"}
    interval = period_map.get(request.period, "365 days")

    # Busca preços de todos os ativos
    tickers = [a.ticker for a in request.allocations]
    placeholders = ", ".join([f"'{t}'" for t in tickers])

    query = text(f"""
        SELECT a.ticker, p.date, p.close_price
        FROM prices p
        JOIN assets a ON a.id = p.asset_id
        WHERE a.ticker IN ({placeholders})
        AND p.date >= CURRENT_DATE - INTERVAL '{interval}'
        ORDER BY p.date
    """)

    df = pd.read_sql(query, engine)

    if df.empty:
        raise HTTPException(status_code=404, detail="Nenhum dado encontrado")

    # Pivot: linhas = datas e colunas = tickers
    pivot = df.pivot(index="date", columns="ticker", values="close_price")
    pivot = pivot.dropna()

    if pivot.empty:
        raise HTTPException(status_code=404, detail="Dados insuficientes para o período")

    # Retornos diários de cada ativo
    returns = pivot.pct_change().dropna()

    # Retorno ponderado da carteira
    weights = {a.ticker: a.weight for a in request.allocations}
    weight_series = pd.Series(weights)
    portfolio_returns = returns.dot(weight_series)

    # Retorno acumulado da carteira
    cumulative = (1 + portfolio_returns).cumprod()
    portfolio_return = round((cumulative.iloc[-1] - 1) * 100, 2)

    # Volatilidade anualizada
    portfolio_volatility = round(portfolio_returns.std() * np.sqrt(252) * 100, 2)

    # Sharpe da carteira
    risk_free = float(0.13)
    excess = (portfolio_returns.mean() * 252) - risk_free
    vol = portfolio_returns.std() * np.sqrt(252)
    portfolio_sharpe = round(excess / vol if vol != 0 else 0, 2)

    # Histórico normalizado para o gráfico
    history = [
        {"date": str(date), "value": round((val - 1) * 100, 2)}
        for date, val in cumulative.items()
    ]

    benchmark_query = text(f"""
            SELECT p.date, p.close_price
            FROM prices p
            JOIN assets a ON a.id = p.asset_id
            WHERE a.ticker = '^BVSP'
            AND p.date >= CURRENT_DATE - INTERVAL '{interval}'
            ORDER BY p.date
        """)

    benchmark_df = pd.read_sql(benchmark_query, engine)
    benchmark_df = benchmark_df[benchmark_df["date"].isin(pivot.index)]

    benchmark_returns = benchmark_df.set_index("date")["close_price"].pct_change().dropna()
    benchmark_cumulative = (1 + benchmark_returns).cumprod()

    benchmark_history = [
        {"date": str(date), "value": round((val - 1) * 100, 2)}
        for date, val in benchmark_cumulative.items()
    ]

    return {
        "return":            portfolio_return,
        "volatility":        portfolio_volatility,
        "sharpe":            portfolio_sharpe,
        "history":           history,
        "benchmark_history": benchmark_history
    }