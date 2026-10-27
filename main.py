from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from models import User, Watchlist
from services.stock_engine import calculate_21_ema

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