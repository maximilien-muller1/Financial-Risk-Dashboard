import numpy as np
import pandas as pd

def monte_carlo_simulation(last_price, historical_returns, n_days, n_simulations):
    """
    Simule des prix futurs avec Bootstrapping ET ajustement de tendance (Avec taux sans risque).
    """
    
    # 1. Nettoyage
    hist_returns = historical_returns.dropna().values
    
    # On calcule la moyenne quotidienne historique (qui est trop élevée actuellement)
    mu_historical = np.mean(hist_returns)
    
    # On impose une tendance (5% par an ; Taux sans risque) 
    conservative_drift = 0.05 / 252 
    
    # On AJUSTE l'historique :
   
    adjusted_returns = hist_returns - mu_historical + conservative_drift

    #  Tirage au sort sur les rendements AJUSTÉS
    random_returns = np.random.choice(adjusted_returns, size=(n_days, n_simulations))
    
    # Reconstruction
    cumulative_returns = np.cumsum(random_returns, axis=0)
    simulation_paths = last_price * np.exp(cumulative_returns)
    
    # Mise en forme
    simulation_df = pd.DataFrame(simulation_paths)
    
    start_row = pd.DataFrame([[last_price] * n_simulations])
    simulation_df = pd.concat([start_row, simulation_df]).reset_index(drop=True)
    
    simulation_df.columns = [f"Sim_{i}" for i in range(n_simulations)]

    return simulation_df