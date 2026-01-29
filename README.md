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

## Tech Stack

* **Language:** Python 3.9+
* **Web Interface:** Streamlit
* **Data & Finance:** Pandas, NumPy, Yfinance
* **Visualization:** Plotly (Interactive charts), Matplotlib
* **Statistics:** SciPy

## Project Structure

```text
├── data/               # Local data storage (cache)
├── src/                # Modular source code
│   ├── data_loader.py  # Data fetching and cleaning
│   ├── indicators.py   # Financial metrics (Volatility, Drawdown, VaR, Beta)
│   ├── simulation.py   # Monte Carlo simulation engine (Bootstrapping)
│   └── strategies.py   # Portfolio backtesting logic
├── app.py              # Streamlit application entry point
├── requirements.txt    # Project dependencies
└── README.md           # Documentation
