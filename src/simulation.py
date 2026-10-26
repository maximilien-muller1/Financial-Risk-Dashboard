import numpy as np
import pandas as pd

def monte_carlo_simulation(last_price, historical_returns, n_days, n_simulations):
    """
    Simulates future prices using Bootstrapping AND trend adjustment (Drift).
    The historical mean is replaced by a fixed, conservative drift so that the
    simulation does not simply extrapolate past performance.
    """
    
    # Cleaning
    hist_returns = historical_returns.dropna().values
    
    # Calculate historical daily mean 
    mu_historical = np.mean(hist_returns)
    
    # Impose a conservative trend (5% per year, a fixed assumption)
    conservative_drift = 0.05 / 252 
    
    # ADJUST history:
    # Subtract past excess returns, add conservative drift
    adjusted_returns = hist_returns - mu_historical + conservative_drift

    # Random sampling from ADJUSTED returns (Bootstrapping)
    random_returns = np.random.choice(adjusted_returns, size=(n_days, n_simulations))
    
    # Path Reconstruction
    cumulative_returns = np.cumsum(random_returns, axis=0)
    simulation_paths = last_price * np.exp(cumulative_returns)
    
    # Formatting to DataFrame
    simulation_df = pd.DataFrame(simulation_paths)
    
    # Add start row (Day 0)
    start_row = pd.DataFrame([[last_price] * n_simulations])
    simulation_df = pd.concat([start_row, simulation_df]).reset_index(drop=True)
    
    simulation_df.columns = [f"Sim_{i}" for i in range(n_simulations)]

    return simulation_df
