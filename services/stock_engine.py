import yfinance as yf
import pandas as pd
import math

def calculate_21_ema(ticker_symbol: str):
    # Fetch historical daily data for the past 3 months
    data = yf.download(ticker_symbol, period="3mo", interval="1d", progress=False)
    
    if data.empty:
        raise ValueError(f"No data found for ticker: {ticker_symbol}")
    
    # Flatten multi-index columns if present in newer yfinance versions
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    
    # Calculate the 21 Exponential Moving Average (EMA) on closing prices
    data['21_EMA'] = data['Close'].ewm(span=21, adjust=False).mean()
    
    # Drop rows with NaN values to ensure clean data
    data = data.dropna(subset=['Close', '21_EMA'])
    
    if data.empty:
        raise ValueError(f"Insufficient valid data for ticker: {ticker_symbol}")
    
    # Extract the latest closing price and latest EMA value safely as floats
    latest_close = float(data['Close'].iloc[-1])
    latest_ema = float(data['21_EMA'].iloc[-1])
    
    # Double check for NaN or infinite values
    if math.isnan(latest_close) or math.isnan(latest_ema):
        raise ValueError(f"Computed value resulted in NaN for ticker: {ticker_symbol}")
    
    # Determine basic crossover signal
    signal = "BULLISH (Price above 21 EMA)" if latest_close > latest_ema else "BEARISH (Price below 21 EMA)"
    
    return {
        "ticker": ticker_symbol.upper(),
        "latest_close": latest_close,
        "latest_21_ema": latest_ema,
        "signal": signal,
        "data_frame": data
    }

if __name__ == "__main__":
    print("Fetching stock data and calculating 21 EMA...")
    result = calculate_21_ema("SPY")
    print(f"Ticker: {result['ticker']}")
    print(f"Latest Close: {result['latest_close']:.2f}")
    print(f"Latest 21 EMA: {result['latest_21_ema']:.2f}")
    print(f"Signal: {result['signal']}")

def get_batch_stock_signals(tickers: list[str]) -> list[dict]:
    """
    Batch processes a list of tickers to compute real-time price and 21 EMA signals.
    """
    results = []
    for ticker in tickers:
        try:
            signal_data = get_stock_data_and_ema(ticker)
            results.append(signal_data)
        except Exception as e:
            results.append({
                "ticker": ticker,
                "error": f"Failed to compute signal: {str(e)}"
            })
    return results