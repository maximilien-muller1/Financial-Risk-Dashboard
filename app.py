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


# Page Configuration
st.set_page_config(page_title="Risk Analysis Dashboard", layout="wide")

st.title("Financial Risk Analysis Dashboard")
st.markdown(
    """
    This application allows you to analyze **historical performance** and simulate the **future** of any financial asset to backtest simple investment strategies.
    """
)

# SIDEBAR (SETTINGS)
st.sidebar.header("Settings")

ticker = st.sidebar.text_input("Ticker Symbol (e.g., SPY, AAPL, BTC-USD)", value="SPY")

# Default Dates (3 years back)
today = datetime.now()
three_years_ago = today - timedelta(days=3 * 365)

start_date = st.sidebar.date_input("Start Date", value=three_years_ago)
end_date = st.sidebar.date_input("End Date", value=today)


# DATA LOADING LOGIC 
# If user clicks the button, load and save to session
if st.sidebar.button("Run Analysis"):
    with st.spinner("Fetching data..."):
        try:
            raw_data = load_data(
                ticker, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")
            )
            st.session_state["data"] = raw_data
            st.session_state["ticker"] = ticker
            
        except Exception as e:
            st.error(f"Error loading data: {e}")


# MAIN DISPLAY
# Check if data is in memory. If yes, display everything.
if "data" in st.session_state:
    
    data = st.session_state["data"]
    current_ticker = st.session_state["ticker"]

    # HISTORICAL ANALYSIS
    try:
        # Calculate indicators
        volatility = calculate_annual_volatility(data["Log_Returns"])
        max_dd = calculate_max_drawdown(data["Price"])
        var_95 = calculate_var_95(data["Log_Returns"])

        st.success(f"Analysis for {current_ticker}")
        st.markdown("### Risk Indicators")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                label="Annualized Volatility",
                value=f"{volatility:.2%}",
                help="Measures the intensity of variations (risk) over a year.",
            )

        with col2:
            st.metric(
                label="Max Drawdown",
                value=f"{max_dd:.2%}",
                help="The worst historical loss recorded from peak to trough.",
            )

        with col3:
            st.metric(
                label="Value at Risk (95%)",
                value=f"{var_95:.2%}",
                help="In 95% of cases, the daily loss will not exceed this threshold.",
            )

        # Charts
        st.markdown("---")
        col_g1, col_g2 = st.columns(2)
        
        with col_g1:
            st.markdown("#### Price Evolution")
            st.line_chart(data["Price"])
        
        with col_g2:
            st.markdown("#### Returns Distribution")
            st.bar_chart(data["Log_Returns"])

        with st.expander("View Raw Data"):
            st.write(data)

       # MONTE CARLO SIMULATION
        st.markdown("---")
        st.subheader("Monte Carlo Prediction")
        st.markdown("Simulate multiple future scenarios.")

        # Check if simulation is already stored in memory
        if "sim_data" in st.session_state:
            
            # RESULT SCREEN
            # Reset button
            if st.button("Reset / New Simulation"):
                del st.session_state["sim_data"] # Delete data
                st.rerun() # Reload page immediately

            st.success("Simulation complete!")
            
            # Retrieve stored data
            sim_data = st.session_state["sim_data"]
            horizon = st.session_state["sim_horizon"]
            last_price = data["Price"].iloc[-1] # Current price for comparison

            # Chart Display
            chart_data = pd.DataFrame()
            
            chart_data['Worst Case'] = sim_data.min(axis=1)      # Bottom line
            chart_data['Expected Mean'] = sim_data.mean(axis=1)  # Middle line
            chart_data['Best Case'] = sim_data.max(axis=1)       # Top line
            
            # Display only these 3 lines
            st.line_chart(chart_data)

            # Statistical Calculations
            final_prices = sim_data.iloc[-1]
            mean_final = final_prices.mean()
            min_final = final_prices.min()
            max_final = final_prices.max()

            # Percentage calculations
            progression_mean = (mean_final - last_price) / last_price
            progression_min = (min_final - last_price) / last_price
            progression_max = (max_final - last_price) / last_price

            # KPIs Display
            col_pred1, col_pred2, col_pred3 = st.columns(3)
            
            col_pred1.metric(
                "Expected Mean",
                f"{mean_final:.2f} $",
                f"{progression_mean:.2%}"
            )
            col_pred2.metric(
                "Worst Case (Crash)",
                f"{min_final:.2f} $",
                f"{progression_min:.2%}"
            )
            col_pred3.metric(
                "Best Case",
                f"{max_final:.2f} $",
                f"{progression_max:.2%}"
            )

        else:
            # CONFIGURATION SCREEN 
            
            col_sim1, col_sim2 = st.columns(2)

            with col_sim1:
                n_sim = st.slider("Number of Simulations", 50, 1000, 200, 50)

            with col_sim2:
                horizon = st.slider("Horizon (days)", 3, 365, 252)

            # Run Button
            if st.button(f"Run Simulation ({horizon} days)"):
                with st.spinner(f"Calculating {n_sim} scenarios based on past data..."):
                    
                    # Retrieve inputs
                    last_price = data["Price"].iloc[-1]
                    historical_returns = data["Log_Returns"]
                    
                    # Call "Bootstrapping" function
                    sim_data = monte_carlo_simulation(last_price, historical_returns, horizon, n_sim)
                    
                    # Save to Session
                    st.session_state["sim_data"] = sim_data
                    st.session_state["sim_horizon"] = horizon
                    
                    # Rerun
                    st.rerun()
                    

        st.markdown("---")
        st.subheader("Strategy Comparator: DCA vs Lump Sum")
        st.markdown("Is it better to invest all at once or little by little?")

        col_strat1, col_strat2, col_strat3, col_strat4 = st.columns(4)

        with col_strat1:
            amount = st.number_input("Investment Amount ($)", value=10000, step=1000, key="strat_amount")

        with col_strat2:
            dca_day_1 = st.selectbox("DCA Day #1", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], key="dca_1")
        
        with col_strat3:
            dca_day_2 = st.selectbox("DCA Day #2", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], key="dca_2")

        with col_strat4:
            st.write("") # Spacer to align button
            st.write("") 
            run_strat = st.button("Compare Strategies")

        if run_strat:
            #Run simulation for DAY 1
            res_1 = backtest_dca_vs_lump_sum(data, amount, dca_day_1)
            
            #Run simulation for DAY 2
            res_2 = backtest_dca_vs_lump_sum(data, amount, dca_day_2)
            
            # COMBINE RESULTS
            strategy_df = pd.DataFrame()
            strategy_df["Lump Sum (All at start)"] = res_1["Lump_Sum_Value"]
            strategy_df[f"DCA {dca_day_1}"] = res_1["DCA_Value"]
            strategy_df[f"DCA {dca_day_2}"] = res_2["DCA_Value"]
            
            # PERFORMANCE CALCULATION
            final_lump = strategy_df["Lump Sum (All at start)"].iloc[-1]
            final_dca_1 = strategy_df[f"DCA {dca_day_1}"].iloc[-1]
            final_dca_2 = strategy_df[f"DCA {dca_day_2}"].iloc[-1]
            
            perf_lump = (final_lump - amount) / amount
            perf_dca_1 = (final_dca_1 - amount) / amount
            perf_dca_2 = (final_dca_2 - amount) / amount

            # Display Winners
            col_res1, col_res2, col_res3 = st.columns(3)
            
            with col_res1:
                st.metric("Lump Sum Result", f"{final_lump:,.0f} $", f"{perf_lump:+.2%}")
            
            with col_res2:
                st.metric(f"DCA Result (on {dca_day_1})", f"{final_dca_1:,.0f} $", f"{perf_dca_1:+.2%}")
                
            with col_res3:
                st.metric(f"DCA Result (on {dca_day_2})", f"{final_dca_2:,.0f} $", f"{perf_dca_2:+.2%}")
            
                
            # Chart
            st.line_chart(strategy_df)
            
            
            with st.expander("Understand the Result"):
                st.write("""
                - **Bull Market:** **Lump Sum** often wins because you put all your money to work early at the lowest price.
                - **Bear Market:** **DCA** wins because it allows you to buy shares cheaper as the price drops, lowering your average cost basis.
                """)    
    except Exception as e:
        st.error(f"An error occurred during display: {e}")

else:
    # Welcome message if no data is loaded
    st.info("Enter a ticker in the sidebar menu and click 'Run Analysis'.")
