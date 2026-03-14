from database import SessionLocal
from models import Asset

ASSETS = [
    # Ações
    {"ticker": "PETR4.SA",  "name": "Petrobras",            "category": "ação",   "logo_url": "https://www.google.com/s2/favicons?domain=petrobras.com.br&sz=64"},
    {"ticker": "VALE3.SA",  "name": "Vale",                  "category": "ação",   "logo_url": "https://www.google.com/s2/favicons?domain=vale.com&sz=64"},
    {"ticker": "ITUB4.SA",  "name": "Itaú Unibanco",         "category": "ação",   "logo_url": "https://www.google.com/s2/favicons?domain=itau.com.br&sz=64"},
    {"ticker": "BBAS3.SA",  "name": "Banco do Brasil",       "category": "ação",   "logo_url": "https://www.google.com/s2/favicons?domain=bb.com.br&sz=64"},
    {"ticker": "ABEV3.SA",  "name": "Ambev",                 "category": "ação",   "logo_url": "https://www.google.com/s2/favicons?domain=ambev.com.br&sz=64"},
    {"ticker": "WEGE3.SA",  "name": "WEG",                   "category": "ação",   "logo_url": "https://www.google.com/s2/favicons?domain=weg.net&sz=64"},
    {"ticker": "RENT3.SA",  "name": "Localiza",              "category": "ação",   "logo_url": "https://www.google.com/s2/favicons?domain=localiza.com&sz=64"},
    {"ticker": "LREN3.SA",  "name": "Lojas Renner",          "category": "ação",   "logo_url": "https://www.google.com/s2/favicons?domain=lojasrenner.com.br&sz=64"},
    {"ticker": "MGLU3.SA",  "name": "Magazine Luiza",        "category": "ação",   "logo_url": "https://www.google.com/s2/favicons?domain=magazineluiza.com.br&sz=64"},
    {"ticker": "BBDC4.SA",  "name": "Banco Bradesco",        "category": "ação",   "logo_url": "https://www.google.com/s2/favicons?domain=bradesco.com.br&sz=64"},
    {"ticker": "SUZB3.SA",  "name": "Suzano",                "category": "ação",   "logo_url": "https://www.google.com/s2/favicons?domain=suzano.com.br&sz=64"},
    {"ticker": "RDOR3.SA",  "name": "Rede D'Or",             "category": "ação",   "logo_url": "https://www.google.com/s2/favicons?domain=redor.com.br&sz=64"},
    {"ticker": "EQTL3.SA",  "name": "Equatorial Energia",    "category": "ação",   "logo_url": "https://www.google.com/s2/favicons?domain=equatorial.com.br&sz=64"},
    {"ticker": "VIVT3.SA",  "name": "Vivo",                  "category": "ação",   "logo_url": "https://www.google.com/s2/favicons?domain=vivo.com.br&sz=64"},
    {"ticker": "EMBR3.SA",  "name": "Embraer",               "category": "ação",   "logo_url": "https://www.google.com/s2/favicons?domain=embraer.com&sz=64"},

    # Índices
    {"ticker": "^BVSP",     "name": "Ibovespa",              "category": "índice", "logo_url": "https://www.google.com/s2/favicons?domain=b3.com.br&sz=64"},
    {"ticker": "^GSPC",     "name": "S&P 500",               "category": "índice", "logo_url": "https://www.google.com/s2/favicons?domain=spglobal.com&sz=64"},

    # FIIs
    {"ticker": "MXRF11.SA", "name": "Maxi Renda FII",        "category": "fii",    "logo_url": "https://www.google.com/s2/favicons?domain=xpinvestimentos.com.br&sz=64"},
    {"ticker": "HGLG11.SA", "name": "CSHG Logística FII",    "category": "fii",    "logo_url": "https://www.google.com/s2/favicons?domain=cshg.com.br&sz=64"},
    {"ticker": "KNRI11.SA", "name": "Kinea Renda Imob. FII", "category": "fii",    "logo_url": "https://www.google.com/s2/favicons?domain=kinea.com.br&sz=64"},
]

def insert_asset(db, ticker, name, category, logo_url):
    existing = db.query(Asset).filter(Asset.ticker == ticker).first()
    if existing:
        print(f"Ativo {ticker} já existe, pulando...")
        return

    asset = Asset(ticker=ticker, name=name, category=category, logo_url=logo_url)
    db.add(asset)
    db.commit()
    print(f"Ativo {ticker} cadastrado com sucesso!")

def seed():
    db = SessionLocal()
    try:
        for asset in ASSETS:
            insert_asset(db, asset["ticker"], asset["name"], asset["category"], asset["logo_url"])
    finally:
        db.close()

if __name__ == "__main__":
    seed()