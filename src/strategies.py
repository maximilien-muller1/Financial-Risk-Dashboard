import pandas as pd
import numpy as np

def backtest_dca_vs_lump_sum(df, total_amount, dca_day_name):
    """
    Compares two strategies based on provided historical data:
    Lump Sum: Invest everything on the first day.
    DCA: Invest progressively every week (on a chosen day).
    """
    
    # Ensure index is in datetime format
    df = df.copy()
    df.index = pd.to_datetime(df.index)
    
    # LUMP SUM STRATEGY (One-time investment)
    start_price = df['Price'].iloc[0]
    num_shares_lump = total_amount / start_price
    
    # Portfolio value simply tracks price evolution
    df['Lump_Sum_Value'] = num_shares_lump * df['Price']
    
    
    # DCA STRATEGY (Dollar Cost Averaging)
    dca_dates = df[df.index.day_name() == dca_day_name].index
    
    if len(dca_dates) == 0:
        return df # Error case if no dates found
