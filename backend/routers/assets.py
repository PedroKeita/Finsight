from fastapi import APIRouter
from database import SessionLocal
from models import Asset

router = APIRouter(prefix="/assets", tags=["Assets"])

@router.get("/", summary="Lista todos os ativos cadastrados")
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