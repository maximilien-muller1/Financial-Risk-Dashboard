import streamlit as st
import pandas as pd

from datetime import datetime, timedelta
from src.data_loader import load_data
from src.indicators import (
    calculate_annual_volatility,
    calculate_max_drawdown,
    calculate_var_95,
)
from src.simulation import monte_carlo_simulation

from src.strategies import backtest_dca_vs_lump_sum


#configuration de la page 
st.set_page_config(page_title="Risk Analysis Dashboard", layout="wide")

st.title("Dashboard d'Analyse de Risque Financier")
st.markdown(
    """
    Cette application permet d'analyser la **performance historique** et d'essayer de **simuler le futur** de n'importe quel actif financier afin de backtester une stratégie simple d'investissement.
    """
)

# SIDEBAR (PARAMÈTRES)
st.sidebar.header("Paramètres")

ticker = st.sidebar.text_input("Symbole Ticker (ex: SPY, AAPL, BTC-USD)", value="SPY")

# Dates par défaut (3 ans en arrière)
today = datetime.now()
three_years_ago = today - timedelta(days=3 * 365)

start_date = st.sidebar.date_input("Date de début", value=three_years_ago)
end_date = st.sidebar.date_input("Date de fin", value=today)


# LOGIQUE DE CHARGEMENT (MÉMOIRE) 
# Si l'utilisateur clique sur le bouton, on charge et on sauvegarde dans la session
if st.sidebar.button("Lancer l'analyse"):
    with st.spinner("Récupération des données en cours..."):
        try:
            # 1. On charge les données
            raw_data = load_data(
                ticker, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")
            )
            # 2. On les met en mémoire (session_state)
            st.session_state["data"] = raw_data
            st.session_state["ticker"] = ticker
            
        except Exception as e:
            st.error(f"Erreur lors du chargement : {e}")


# AFFICHAGE PRINCIPAL
# On vérifie si des données sont en mémoire. Si oui, on affiche tout.
if "data" in st.session_state:
    
    data = st.session_state["data"]
    current_ticker = st.session_state["ticker"]

    # ANALYSE HISTORIQUE
    try:
        # Calcul des indicateurs
        volatility = calculate_annual_volatility(data["Log_Returns"])
        max_dd = calculate_max_drawdown(data["Price"])
        var_95 = calculate_var_95(data["Log_Returns"])

        st.success(f"Analyse affichée pour {current_ticker}")
        st.markdown("Indicateurs de Risque")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                label="Volatilité Annualisée",
                value=f"{volatility:.2%}",
                help="Mesure l'intensité des variations (risque) sur un an.",
            )

        with col2:
            st.metric(
                label="Max Drawdown",
                value=f"{max_dd:.2%}",
                help="La pire perte historique enregistrée du sommet au creux.",
            )

        with col3:
            st.metric(
                label="Value at Risk (95%)",
                value=f"{var_95:.2%}",
                help="Dans 95% des cas, la perte journalière ne dépasse pas ce seuil.",
            )

        # Graphiques
        st.markdown("---")
        col_g1, col_g2 = st.columns(2)
        
        with col_g1:
            st.markdown("Évolution du Prix")
            st.line_chart(data["Price"])
        
        with col_g2:
            st.markdown("Distribution des Rendements")
            st.bar_chart(data["Log_Returns"])

        with st.expander("Voir les données brutes"):
            st.write(data)

       # SIMULATION MONTE CARLO
        st.markdown("---")
        st.subheader("Prédiction Monte Carlo")
        st.markdown("Simulez plusieurs scénarios futurs.")

        # Vérifie si une simulation est déjà stockée en mémoire
        if "sim_data" in st.session_state:
            
            # ÉCRAN DE RÉSULTAT
            # Bouton pour effacer et recommencer
            if st.button(" Réinitialiser / Nouvelle simulation"):
                del st.session_state["sim_data"] # On supprime les données
                st.rerun() # On recharge la page immédiatement

            st.success("Simulation terminée !")
            
            # Récupération des données stockées
            sim_data = st.session_state["sim_data"]
            horizon = st.session_state["sim_horizon"]
            last_price = data["Price"].iloc[-1] # Prix actuel pour comparer

            # Affichage du Graphique
            chart_data = pd.DataFrame()
            
            chart_data['Pire Scénario'] = sim_data.min(axis=1)     # La ligne du bas
            chart_data['Moyenne Attendue'] = sim_data.mean(axis=1) # La ligne du milieu
            chart_data['Meilleur Scénario'] = sim_data.max(axis=1) # La ligne du haut
            
            # On affiche seulement ces 3 courbes (C'est instantané !)
            st.line_chart(chart_data)

            # Calculs statistiques
            final_prices = sim_data.iloc[-1]
            mean_final = final_prices.mean()
            min_final = final_prices.min()
            max_final = final_prices.max()

            # Calcul des pourcentages
            progression_mean = (mean_final - last_price) / last_price
            progression_min = (min_final - last_price) / last_price
            progression_max = (max_final - last_price) / last_price

            # Affichage des KPIs
            col_pred1, col_pred2, col_pred3 = st.columns(3)
            
            col_pred1.metric(
                "Moyenne Attendue",
                f"{mean_final:.2f} $",
                f"{progression_mean:.2%}"
            )
            col_pred2.metric(
                "Pire Scénario (Crash)",
                f"{min_final:.2f} $",
                f"{progression_min:.2%}"
            )
            col_pred3.metric(
                "Meilleur Scénario",
                f"{max_final:.2f} $",
                f"{progression_max:.2%}"
            )

        else:
            # ÉCRAN DE CONFIGURATION (Avant de lancer)
            
            col_sim1, col_sim2 = st.columns(2)

            with col_sim1:
                n_sim = st.slider("Nombre de simulations", 50, 1000, 200, 50)

            with col_sim2:
                horizon = st.slider("Horizon (jours)", 3, 365, 252)

            # Bouton de lancement
            if st.button(f"Lancer la simulation ({horizon} jours)"):
                with st.spinner(f"Calcul de {n_sim} scénarios basés sur le passé..."):
                    
                    # On récupère les prix
                    last_price = data["Price"].iloc[-1]
                    
                   
                    historical_returns = data["Log_Returns"]
                    
                    # Appel de la fonction "Bootstrapping"
                    sim_data = monte_carlo_simulation(last_price, historical_returns, horizon, n_sim)
                    
                    # Sauvegarde dans la Session
                    st.session_state["sim_data"] = sim_data
                    st.session_state["sim_horizon"] = horizon
                    
                    # Rechargement
                    st.rerun()
                    

        st.markdown("---")
        st.subheader("Comparateur de Stratégies : 2 métheodes de DCA vs Lump Sum")
        st.markdown("Est-il préférable d'investir tout d'un coup ou petit à petit ?")

        col_strat1, col_strat2, col_strat3, col_strat4 = st.columns(4)

        with col_strat1:
            amount = st.number_input("Montant à investir ($)", value=10000, step=1000, key="strat_amount")

        with col_strat2:
            dca_day_1 = st.selectbox("Jour d'achat DCA", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], key="dca_1")
        
        with col_strat3:
            dca_day_2 = st.selectbox("Jour d'achat DCA", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], key="dca_2")

        with col_strat4:
            st.write("") # Juste pour aligner le bouton
            st.write("") 
            run_strat = st.button("Comparer les stratégies")

        if run_strat:
            # 1. On lance la simulation pour le JOUR 1
            res_1 = backtest_dca_vs_lump_sum(data, amount, dca_day_1)
            
            # 2. On lance la simulation pour le JOUR 2
            res_2 = backtest_dca_vs_lump_sum(data, amount, dca_day_2)
            
            # --- COMBINAISON DES RÉSULTATS ---
            # On crée un tableau final propre avec les 3 courbes
            strategy_df = pd.DataFrame()
            strategy_df["Lump Sum (Tout au début)"] = res_1["Lump_Sum_Value"]
            strategy_df[f"DCA {dca_day_1}"] = res_1["DCA_Value"]
            strategy_df[f"DCA {dca_day_2}"] = res_2["DCA_Value"]
            
            # --- CALCULS DE PERFORMANCE ---
            final_lump = strategy_df["Lump Sum (Tout au début)"].iloc[-1]
            final_dca_1 = strategy_df[f"DCA {dca_day_1}"].iloc[-1]
            final_dca_2 = strategy_df[f"DCA {dca_day_2}"].iloc[-1]
            
            perf_lump = (final_lump - amount) / amount
            perf_dca_1 = (final_dca_1 - amount) / amount
            perf_dca_2 = (final_dca_2 - amount) / amount

            # Affichage des gagnants
            col_res1, col_res2, col_res3 = st.columns(3)
            
            with col_res1:
                st.metric("Résultat Lump Sum", f"{final_lump:,.0f} $", f"{perf_lump:+.2%}")
            
            with col_res2:
                st.metric(f"Résultat DCA (le {dca_day_1})", f"{final_dca_1:,.0f} $", f"{perf_dca_1:+.2%}")
                
            with col_res2:
                st.metric(f"Résultat DCA (le {dca_day_2})", f"{final_dca_2:,.0f} $", f"{perf_dca_2:+.2%}")
            
                
            # Graphique
            st.line_chart(strategy_df)
            
            
            with st.expander("Comprendre le résultat"):
                st.write("""
                - **En marché haussier (Bull Market) :** Le **Lump Sum** gagne souvent car vous mettez tout votre argent au travail dès le début au prix le plus bas.
                - **En marché baissier (Bear Market) :** Le **DCA** gagne car il vous permet d'acheter des actions moins chères au fur et à mesure que le prix baisse, lissant votre prix de revient.
                """)    
    except Exception as e:
        st.error(f"Une erreur est survenue pendant l'affichage : {e}")

else:
    # Message d'accueil si aucune donnée n'est chargée
    st.info("Entrez un ticker dans le menu à gauche et cliquez sur 'Lancer l'analyse'.")