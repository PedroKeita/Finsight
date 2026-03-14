from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import assets, prices, indicators, collect
from scheduler import start_scheduler
import logging

logger = logging.getLogger(__name__)

app = FastAPI(
    title="FinSight API",
    description="API de análise de carteiras de investimentos",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(assets.router)
app.include_router(prices.router)
app.include_router(indicators.router)
app.include_router(collect.router)

@app.on_event("startup")
async def startup_event():
    start_scheduler()
    logger.info("FinSight API iniciada")
