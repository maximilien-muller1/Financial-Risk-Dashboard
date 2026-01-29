import numpy as np
import pandas as pd


def calculate_annual_volatility(log_returns):
    """
    Calcule la volatilité annualisée.
    Formule : Écart-type journalier * Racine(252 jours de bourse)
    """
    # .std() calcule l'écart-type (la dispersion autour de la moyenne)
    daily_vol = log_returns.std()

    # On multiplie par racine de 252 car il y a environ 252 jours de bourse par an
    annual_vol = daily_vol * np.sqrt(252)

    return annual_vol


def calculate_max_drawdown(prices):
    """
    Calcule la perte maximale historique (du sommet au creux).
    """
    # 1. On cherche le prix maximum atteint jusqu'à maintenant (Running Max)
    rolling_max = prices.cummax()

    # 2. On calcule la différence actuel par rapport à l'ATH
    drawdown = (prices - rolling_max) / rolling_max

    # 3. Le Max Drawdown = valeur la plus basse (tjrs négative)
    max_dd = drawdown.min()

    return max_dd


def calculate_var_95(log_returns):
    """
    Calcule la Value at Risk (VaR) historique à 95%.
    "Dans les 5% pires cas, combien je perds ?"
    """
    # On trie les rendements du pire au meilleur et on prend celui à la limite des 5%
    var_95 = np.percentile(log_returns, 5)
    return var_95
