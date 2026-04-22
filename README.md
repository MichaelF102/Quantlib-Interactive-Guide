# ⚖️ QuantLib Interactive Guide

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://quantlib-interactive-guide.streamlit.app/)
[![QuantLib](https://img.shields.io/badge/Library-QuantLib-blue.svg)](https://www.quantlib.org/)
[![Python](https://img.shields.io/badge/Python-3.9+-yellow.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

> **Master Quantitative Finance through high-performance simulations and interactive visualizations.**

Welcome to the **QuantLib Interactive Guide**, a comprehensive dashboard designed to demystify the complexities of quantitative finance. Built on top of the industry-standard **QuantLib** library, this application provides a hands-on learning experience for financial engineers, traders, and data scientists.

---
You Can access the Live Project At https://quantlibguide.streamlit.app/


## 🌟 Key Highlights

This project translates the abstract concepts of QuantLib into a visual, intuitive playground. Instead of just reading documentation, you can interact with market dynamics in real-time.

### 🏗️ Core Architecture
- **Evaluation Dynamics**: Live "Time Travel" through global evaluation date settings.
- **Reactive System**: Implementation of the **Observer/Observable** pattern to demonstrate automatic market data propagation.
- **Data Structures**: Interactive exploration of QuantLib Arrays, Matrices, and Quote Handles.

### 📈 Advanced Financial Modeling
- **Term Structures**: Visualizing Yield Curves (Nelson-Siegel, cubic splines) and Volatility Surfaces.
- **Stochastic Processes**: Simulating Geometric Brownian Motion, Ornstein-Uhlenbeck, and Hull-White paths.
- **Volatility Smiles**: Interactive **SABR Model** playground to visualize how Alpha, Beta, Rho, and Nu affect the smile.
- **Pricing Engines**: Comparative analysis of Analytic, Monte Carlo, and Finite Difference engines.

---

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/) (Glassmorphism UI / Custom CSS)
- **Engine**: [QuantLib-Python](https://pypi.org/project/QuantLib/)
- **Visuals**: [Plotly](https://plotly.com/), [Matplotlib](https://matplotlib.org/)
- **Data**: [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
- **Analysis**: [SciPy](https://scipy.org/)

---

## 📂 Project Structure

The guide is organized into **12 specialized modules**:

1.  **Basics** — Evaluation dates, Arrays, and Matrix operations.
2.  **Cashflows & Legs** — Building complex payment streams.
3.  **Currencies** — Handling FX and multi-currency valuation.
4.  **Dates & Conventions** — Calendars, Business days, and Day counters.
5.  **Indexes** — Libor, Euribor, and Overnight Index configurations.
6.  **Instruments** — Bonds, Swaps, Options, and more.
7.  **Math Tools** — Solvers, Optimizers, and Interpolations.
8.  **Pricing Engines** — The "How" of valuation.
9.  **Pricing Models** — Black-Scholes, Hull-White, and Heston.
10. **Stochastic Processes** — Simulating market random walks.
11. **Term Structures** — Bootstrapping and Curve fitting.
12. **Calibration Helpers** — Fitting models to market market prices.

---

## 🚀 Quick Start

1. **Clone the Repository**
   ```bash
   git clone https://github.com/MichaelF102/Quantlib-Interactive-Guide.git
   cd Quantlib-Interactive-Guide
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Dashboard**
   ```bash
   streamlit run Introduction.py
   ```

---

## 👨‍💻 About the Author

**Michael Fernandes**  
*Quantitative Finance Enthusiast & Data Science Developer*

I am a passionate developer dedicated to building automation systems and interactive tools that simplify complex financial concepts. My work focuses on the intersection of **Software Engineering** and **Quantitative Finance**, utilizing Python's robust ecosystem to create professional-grade analytical platforms.

**Connect with me:**
- 💼 [LinkedIn](https://www.linkedin.com/in/michael-fernandes-7a3b6227a/)
- 📧 [Email](mailto:michael.fernandes@example.com)
- 🐙 [GitHub Profile](https://github.com/MichaelF102)

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---
