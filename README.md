# Analyseur de Risque & Stratégies d'Investissement

> **Un outil Data-Driven pour visualiser l'incertitude des marchés financiers.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=Streamlit&logoColor=white)](https://streamlit.io/)

## Description :

Ce projet est une application interactive qui permet de mieux comprendre le couple **Rendement / Risque**. 

Cette application met l'accent sur :
1.  La **quantification du risque** (au-delà de la simple volatilité).
2.  La **simulation de scénarios futurs** (Monte Carlo) pour visualiser l'incertitude en utilisant une méthode de Bootstrapping.
3.  La **comparaison de stratégies** (DCA vs Investissement unique).

L'objectif n'est pas de *prédire* le prix futur d'un actif, mais d'analyser statistiquement son comportement passé et évaluer la meilleur stratégie d'investissement.
## Fonctionnalités Clés

* **Dashboard d'Analyse :** Récupération automatique des données (Yahoo Finance) et calcul des métriques financières (Rendements Log, Volatilité Glissante, Max Drawdown, VaR).
* **Laboratoire de Simulation :** Génération de scénarios futurs probables via des méthodes de Monte Carlo (Mouvement Brownien Géométrique) pour créer des cônes d'incertitude.
* **Comparateur de Stratégies :** Backtesting interactif :
    * *Lump Sum :* Investissement unique.
    * *DCA (Dollar Cost Averaging) :* Investissement programmé.
    * *Smart Exposure :* Stratégie adaptative basée sur la détection de régimes de risque par IA.

## Stack Technique

* **Langage :** Python 3.9+
* **Interface Web :** Streamlit
* **Data & Finance :** Pandas, NumPy, Yfinance
* **Visualisation :** Plotly (Graphiques interactifs), Matplotlib
* **Statistiques :** SciPy

## Structure du Projet

```text
├── data/               # Données locales (cache)
├── src/                # Code source modulaire
│   ├── data_loader.py  # Récupération et nettoyage des données
│   ├── indicators.py   # Calculs financiers (Volatilité, Drawdown, VaR)
│   ├── simulation.py   # Moteur de simulation Monte Carlo
│   └── strategies.py   # Logique de backtesting des portefeuilles
├── app.py              # Point d'entrée de l'application Streamlit
├── requirements.txt    # Dépendances du projet
└── README.md           # Documentation
