import numpy as np
import pandas as pd
from scipy.stats import chi2, norm


def rolling_var(log_returns, window=250, confidence=0.95, method="historical"):
    """
    Computes a daily Value at Risk forecast for each day, using only the
    `window` previous days (no look-ahead: the VaR for day t uses data up to t-1).

    method = "historical": empirical quantile of past returns
    method = "parametric": mean + z * std, assuming normally distributed returns
    """
    alpha = 1 - confidence  # e.g. 0.05 for a 95 % VaR
    past = log_returns.rolling(window)

    if method == "historical":
        var = past.quantile(alpha)
    elif method == "parametric":
        var = past.mean() + norm.ppf(alpha) * past.std()
    else:
        raise ValueError("method must be 'historical' or 'parametric'")

    # Shift by one day: the forecast made at the close of t-1 is tested on day t
    return var.shift(1)


def kupiec_pof_test(n_obs, n_breaches, confidence=0.95):
    """
    Kupiec Proportion of Failures (POF) test.
    H0: the observed breach rate equals the expected rate (1 - confidence).
    Returns the likelihood-ratio statistic and its p-value (chi-squared, 1 df).
    """
    p = 1 - confidence
    x, T = n_breaches, n_obs
    p_hat = x / T

    # Log-likelihood under H0 (expected rate p)
    ll_h0 = (T - x) * np.log(1 - p) + x * np.log(p)

    # Log-likelihood under the observed rate (0 * log(0) is treated as 0)
    ll_obs = 0.0
    if x < T:
        ll_obs += (T - x) * np.log(1 - p_hat)
    if x > 0:
        ll_obs += x * np.log(p_hat)

    lr_stat = -2 * (ll_h0 - ll_obs)
    p_value = 1 - chi2.cdf(lr_stat, df=1)
    return lr_stat, p_value


def backtest_var(log_returns, window=250, confidence=0.95, method="historical"):
    """
    Backtests a VaR model: compares each daily return with the VaR forecast
    made the day before and counts the breaches (return below the VaR).
    """
    var = rolling_var(log_returns, window, confidence, method)

    df = pd.DataFrame({"Log_Returns": log_returns, "VaR": var}).dropna()
    df["Breach"] = df["Log_Returns"] < df["VaR"]

    n_obs = len(df)
    n_breaches = int(df["Breach"].sum())
    expected = n_obs * (1 - confidence)
    lr_stat, p_value = kupiec_pof_test(n_obs, n_breaches, confidence)

    stats = {
        "observations": n_obs,
        "breaches": n_breaches,
        "expected_breaches": expected,
        "breach_rate": n_breaches / n_obs,
        "kupiec_lr": lr_stat,
        "kupiec_p_value": p_value,
        # At the 5 % significance level, p < 0.05 means we reject the model
        "model_rejected": p_value < 0.05,
    }
    return df, stats
