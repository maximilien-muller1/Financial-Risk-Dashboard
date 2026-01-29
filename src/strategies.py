import pandas as pd
import numpy as np

def backtest_dca_vs_lump_sum(df, total_amount, dca_day_name):
    """
    Compare deux stratégies sur l'historique fourni :
    1. Lump Sum : Tout investir le premier jour.
    2. DCA : Investir progressivement chaque semaine (jour choisi).
    """
    
    # On s'assure que l'index est bien au format Date
    df = df.copy()
    df.index = pd.to_datetime(df.index)
    
    # STRATÉGIE LUMP SUM (Investissement Unique)
    start_price = df['Price'].iloc[0]
    num_shares_lump = total_amount / start_price
    
    # La valeur du portefeuille suit simplement l'évolution du prix
    df['Lump_Sum_Value'] = num_shares_lump * df['Price']
    
    
    # STRATÉGIE DCA (Investissement Programmé)
    # On trouve tous les jours qui correspondent (ex: tous les 'Monday')
    # day_name() renvoie 'Monday', 'Tuesday', etc.
    dca_dates = df[df.index.day_name() == dca_day_name].index
    
    if len(dca_dates) == 0:
        return df # Cas erreur si pas de dates trouvées
        
    # On calcule combien on met à chaque fois
    # Ex: 10 000$ divisé par 50 lundis = 200$ par semaine
    installment_amount = total_amount / len(dca_dates)
    
    # On initialise les colonnes
    df['DCA_Shares'] = 0.0
    df['DCA_Cash'] = total_amount # Au début, tout est en cash
    
    current_shares = 0.0
    current_cash = total_amount
    
    # On parcourt chaque jour (C'est une boucle, un peu lent mais facile à comprendre)
    # Pour optimiser, on pourrait vectoriser, mais pour <5000 lignes ça va vite.
    for date, row in df.iterrows():
        price = row['Price']
        
        # Si c'est un jour d'achat (ex: Lundi) et qu'il nous reste des sous
        if date in dca_dates and current_cash > 1: # >1 pour éviter les centimes
            # On achète
            shares_bought = installment_amount / price
            current_shares += shares_bought
            current_cash -= installment_amount
            
        # On met à jour l'état du jour
        df.at[date, 'DCA_Shares'] = current_shares
        df.at[date, 'DCA_Cash'] = current_cash

    # Valeur Totale DCA = (Actions * Prix) + Cash Restant
    df['DCA_Value'] = (df['DCA_Shares'] * df['Price']) + df['DCA_Cash']
    
    return df[['Lump_Sum_Value', 'DCA_Value']]