import numpy as np
import pandas as pd


def calculate_annual_volatility(log_returns):
    """
    Calculates annualized volatility.
    Formula: Daily Standard Deviation * Sqrt(252 trading days)
    """
    # .std() calculates standard deviation (dispersion around the mean)
    daily_vol = log_returns.std()

    # Multiply by sqrt(252) because there are approx. 252 trading days per year
    annual_vol = daily_vol * np.sqrt(252)

    return annual_vol


def calculate_max_drawdown(prices):
    """
    Calculates the maximum historical drawdown (peak to trough).
    """
    # 1. Calculate the running maximum price up to now
    rolling_max = prices.cummax()

    # 2. Calculate current drawdown relative to the peak (ATH)
    drawdown = (prices - rolling_max) / rolling_max

    # 3. Max Drawdown = the lowest value (always negative)
    max_dd = drawdown.min()

    return max_dd


def calculate_var_95(log_returns):
    """
    Calculates the historical Value at Risk (VaR) at 95%.
    "In the worst 5% of cases, how much do I lose?"
    """
    # Sort returns from worst to best and find the value at the 5% threshold
    var_95 = np.percentile(log_returns, 5)
    return var_95
