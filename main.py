from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from models import User, Watchlist, APIKeyVault
from services.stock_engine import calculate_21_ema
from pydantic import BaseModel
from services.security import encrypt_api_key, decrypt_api_key

# Initialize database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TradeGuard API",
    description="Fintech security & momentum indicator backend",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "Welcome to TradeGuard API. System is secure and operational."}

@app.get("/stock/{ticker}")
def get_stock_signal(ticker: str):
    """
    Fetch live stock data and calculate the 21 EMA signal for any ticker symbol (e.g., SPY, NVDA, GOOGL).
    """
    try:
        result = calculate_21_ema(ticker)
        # Remove dataframe from JSON response since pandas DataFrames aren't JSON serializable directly
        response_data = {
            "ticker": result["ticker"],
            "latest_close": result["latest_close"],
            "latest_21_ema": result["latest_21_ema"],
            "signal": result["signal"]
        }
        return response_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

class APIKeyRequest(BaseModel):
    user_id: int
    service_name: str
    api_key: str

@app.post("/vault/store-db")
def store_and_persist_api_key(payload: APIKeyRequest, db: Session = Depends(get_db)):
    """
    Encrypts an API key with AES-256 and persists it securely to the database.
    """
    try:
        encrypted_ciphertext = encrypt_api_key(payload.api_key)
        
        # Save to database
        db_key_entry = APIKeyVault(
            user_id=payload.user_id,
            service_name=payload.service_name,
            encrypted_key=encrypted_ciphertext
        )
        db.add(db_key_entry)
        db.commit()
        db.refresh(db_key_entry)
        
        return {
            "status": "success",
            "message": f"API key for {payload.service_name} securely encrypted and saved to database.",
            "record_id": db_key_entry.id,
            "service": payload.service_name
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database persistence failed: {str(e)}")