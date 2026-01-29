import yfinance as yf
import pandas as pd
import numpy as np
import streamlit as st

@st.cache_data
def load_data(ticker_symbol, start_date, end_date):
    """
    Fetches data via the yfinance Ticker object.
    """
    print(f" Loading data for {ticker_symbol}...")

    # 1. Create Ticker object
    ticker_obj = yf.Ticker(ticker_symbol)

    # 2. Fetch history
    # Note: .history() auto-adjusts price by default (auto_adjust=True)
    df = ticker_obj.history(start=start_date, end=end_date)

    # Safety check: if dataframe is empty (wrong date or ticker)
    if df.empty:
        raise ValueError(
            f"No data found for {ticker_symbol}. Check the symbol or dates."
        )

    # 3. Clean selection
    # With this method, the column is always named 'Close' and is adjusted
    df = df[["Close"]]

    # Rename to 'Price'
    df.columns = ["Price"]

    # 4. Calculate Log Returns
    df["Log_Returns"] = np.log(df["Price"] / df["Price"].shift(1))

    # 5. Cleaning
    df.dropna(inplace=True)

    return df


# --- Test Block ---
if __name__ == "__main__":
    try:
        # Test on SPY
        data = load_data("SPY", "2023-01-01", "2023-12-31")
        print("\nSUCCESS: Data fetched!")
        print(data.head())
        # Annualized Volatility Test
        print(f"\nVolatility (test): {data['Log_Returns'].std() * (252**0.5):.2%}")
    except Exception as e:
        print(f"\nERROR: {e}")
