# Financial Risk & Investment Strategy Analyzer

> **A Data-Driven tool to visualize financial market uncertainty.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=Streamlit&logoColor=white)](https://streamlit.io/)

## Description

This project is an interactive dashboard designed to provide a deeper understanding of the **Risk/Return trade-off**.

The application focuses on three main pillars:
1.  **Risk Quantification:** Going beyond simple volatility metrics.
2.  **Future Scenario Simulation:** Using Monte Carlo simulations (Bootstrapping) to visualize uncertainty.
3.  **Strategy Comparison:** Backtesting investment methods (DCA vs. Lump Sum).

The goal is not to *predict* the future price of an asset, but to statistically analyze its past behavior to evaluate the best investment strategy.

## Key Features

* **Analysis Dashboard:** Automatic data fetching (Yahoo Finance) and calculation of key financial metrics (Log Returns, Rolling Volatility, Max Drawdown, Value at Risk).
* **Simulation Lab:** Generation of probable future scenarios via Monte Carlo methods (Historical Bootstrapping) to visualize uncertainty cones and potential outcomes.
* **Strategy Comparator:** Interactive backtesting engine:
    * *Lump Sum:* All-in investment.
    * *DCA (Dollar Cost Averaging):* Periodic scheduled investment.

## Quick Start

```bash
git clone https://github.com/maximilien-muller1/Financial-Risk-Dashboard.git
cd Financial-Risk-Dashboard
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Enter a ticker (e.g. `SPY`, `AAPL`, `BTC-USD`), pick a date range and click **Run Analysis**.

## How it works

* **Risk indicators:** annualised volatility (daily std × √252), maximum drawdown (peak to trough) and historical 95 % Value at Risk (5th percentile of daily log returns).
* **Monte Carlo:** daily returns are resampled with replacement (bootstrap). The historical mean is removed and replaced by a conservative 5 % annual drift, so the cone of scenarios does not simply extrapolate past performance.
* **DCA vs Lump Sum:** Lump Sum buys on the first day. DCA splits the same amount into equal weekly purchases on a chosen weekday. Uninvested cash is counted in the portfolio value, so both strategies are compared on the same capital.

## Limitations

* Value at Risk is **historical** only (no parametric or Monte Carlo VaR, and no backtesting of the VaR itself).
* The bootstrap draws returns independently, so it ignores volatility clustering and fat-tail dynamics.
* The 5 % drift is a fixed assumption, not an estimate. No transaction costs or taxes are modelled.
* Data comes from Yahoo Finance via `yfinance`, so availability depends on that service.

This is an educational tool, not investment advice.

## Tech Stack

* **Language:** Python 3.9+
* **Web Interface:** Streamlit
* **Data & Finance:** Pandas, NumPy, Yfinance
* **Visualization:** Plotly (Interactive charts), Matplotlib
* **Statistics:** SciPy

## Project Structure

```text
├── src/                # Modular source code
│   ├── data_loader.py  # Data fetching and cleaning
│   ├── indicators.py   # Financial metrics (Volatility, Drawdown, VaR)
│   ├── simulation.py   # Monte Carlo simulation engine (Bootstrapping)
│   └── strategies.py   # Portfolio backtesting logic
├── app.py              # Streamlit application entry point
├── requirements.txt    # Project dependencies
└── README.md           # Documentation
