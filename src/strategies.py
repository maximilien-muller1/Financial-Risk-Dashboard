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
        return df  # Error case if no dates found

    # Amount invested at each purchase date
    # e.g. 10,000 $ split over 50 Mondays = 200 $ per week
    installment_amount = total_amount / len(dca_dates)

    # Initialise columns: at the start, everything is in cash
    df['DCA_Shares'] = 0.0
    df['DCA_Cash'] = float(total_amount)

    current_shares = 0.0
    current_cash = float(total_amount)

    # Walk through each day (simple loop, fast enough for a few thousand rows)
    for date, row in df.iterrows():
        price = row['Price']

        # On a purchase day, buy as long as some cash is left (> 1 to ignore cents)
        if date in dca_dates and current_cash > 1:
            current_shares += installment_amount / price
            current_cash -= installment_amount

        df.at[date, 'DCA_Shares'] = current_shares
        df.at[date, 'DCA_Cash'] = current_cash

    # Total DCA value = (shares * price) + remaining cash
    df['DCA_Value'] = (df['DCA_Shares'] * df['Price']) + df['DCA_Cash']

    return df[['Lump_Sum_Value', 'DCA_Value']]

