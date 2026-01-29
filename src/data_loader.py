import yfinance as yf
import pandas as pd
import numpy as np
import streamlit as st

@st.cache_data
def load_data(ticker_symbol, start_date, end_date):
    """
    Récupère les données via l'objet Ticker.
    """
    print(f" Chargement des données pour {ticker_symbol}...")

    # 1. On crée l'objet Ticker
    ticker_obj = yf.Ticker(ticker_symbol)

    # 2. On récupère l'historique
    # Note : par défaut, .history() ajuste déjà le prix (auto_adjust=True)
    df = ticker_obj.history(start=start_date, end=end_date)

    # Vérification de sécurité : si le tableau est vide (mauvaise date ou mauvais ticker)
    if df.empty:
        raise ValueError(
            f"Aucune donnée trouvée pour {ticker_symbol}. Vérifie le nom ou les dates."
        )

    # 3. Sélection propre
    # Avec cette méthode, la colonne s'appelle toujours 'Close' et elle est déjà ajustée
    df = df[["Close"]]

    # On renomme en 'Price'
    df.columns = ["Price"]

    # 4. Calcul des Rendements Logarithmiques
    df["Log_Returns"] = np.log(df["Price"] / df["Price"].shift(1))

    # 5. Nettoyage
    df.dropna(inplace=True)

    return df


# --- Bloc de test ---
if __name__ == "__main__":
    try:
        # Test sur le SPY
        data = load_data("SPY", "2023-01-01", "2023-12-31")
        print("\nSUCCÈS : Données récupérées !")
        print(data.head())
        print(f"\nVolatilité (test) : {data['Log_Returns'].std() * (252**0.5):.2%}")
    except Exception as e:
        print(f"\nERREUR : {e}")
