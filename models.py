from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    api_keys = relationship("APIKeyVault", back_populates="owner")
    watchlists = relationship("Watchlist", back_populates="owner")

class APIKeyVault(Base):
    __tablename__ = "api_key_vault"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    service_name = Column(String, nullable=False) # e.g., "Robinhood", "AlphaVantage"
    encrypted_key = Column(String, nullable=False) # AES-256 encrypted payload

    owner = relationship("User", back_populates="api_keys")

class Watchlist(Base):
    __tablename__ = "watchlists"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    ticker = Column(String, nullable=False) # e.g., "SPY", "NVDA", "GOOGL"
    added_at = Column(DateTime, default=datetime.datetime.utcnow)

    owner = relationship("User", back_populates="watchlists")