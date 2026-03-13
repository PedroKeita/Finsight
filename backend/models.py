from sqalchemy import Column, Integer, String, Numeric, BigInteger, Date, ForeignKey, UniqueConstraint
from sqalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(20), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)
    prices = relationship("Price", back_populates="asset")

    def __repr__(self):
        return f"<Asset {self.ticker} - {self.name}>"
    

class Price(Base):
    __tablename__ = "prices"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    date = Column(Date, nullable=False)
    close_price = Column(Numeric(12, 4), nullable=False)
    volume = Column(BigInteger)
    asset = relationship("Asset", back_populates="prices")

    __table_args__ = (
        UniqueConstraint("asset_id", "date", name="uq_asset_date"),
    )

    def __repr__(self):
        return f"<Price {self.asset_id} - {self.date} - {self.close_price}>"