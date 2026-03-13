from database import SessionLocal
from models import Asset

def insert_asset(db, ticker: str, name: str, category: str):
    """Insere um ativo no banco, ignorando se o ticker já existir."""
    existing = db.query(Asset).filter(Asset.ticker == ticker).first()
    if existing:
        print(f"Ativo {ticker} já existe, pulando...")
        return
    
    asset = Asset(ticker=ticker, name=name, category=category)
    db.add(asset)
    db.commit()
    print(f"Ativo {ticker} cadastrado com sucesso!!!")

def seed():
    db = SessionLocal()
    try:
        insert_asset(db, "PETR4.SA", "Petrobras",       "ação")
        insert_asset(db, "VALE3.SA", "Vale",             "ação")
        insert_asset(db, "ITUB4.SA", "Itaú Unibanco",   "ação")
        insert_asset(db, "BBAS3.SA", "Banco do Brasil", "ação")
        insert_asset(db, "^BVSP",    "Ibovespa",        "índice")
    finally:
        db.close()

if __name__ == "__main__":
    seed()