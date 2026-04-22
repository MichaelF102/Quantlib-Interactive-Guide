import streamlit as st
import QuantLib as ql
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="QuantLib - Helpers", layout="wide")

# Custom CSS for Premium Design
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #ffffff;
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }
    h1, h2, h3 {
        color: #00d4ff !important;
    }
    .stExpander {
        background: rgba(255, 255, 255, 0.03) !important;
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("🛠️ Helpers & Bootstrapping")

st.markdown("""
Helpers are the building blocks in QuantLib used to **bootstrap** or **calibrate** term structures. 
They represent market instruments (Deposits, Swaps, Bonds) and ensure that the resulting curve correctly reprices these instruments.
""")

# ===================================================
# 📚 TABLE OF CONTENTS
# ===================================================

st.markdown("## 📚 Table of Contents")

st.markdown("""
<div style="line-height:2; font-size:16px;">
🔹 <a href="#interest_rate" target="_self">1. Interest Rate Helpers</a><br>
🔹 <a href="#vol_helpers" target="_self">2. Volatility Calibration Helpers</a><br>
🔹 <a href="#credit_helpers" target="_self">3. Credit Helpers</a><br>
🔹 <a href="#inflation_helpers" target="_self">4. Inflation Helpers</a><br>
🔹 <a href="#bootstrap_demo" target="_self">🧪 Bootstrapping Simulation</a><br>
</div>
""", unsafe_allow_html=True)

# ===================================================
# 🏦 1. INTEREST RATE HELPERS
# ===================================================

st.markdown("---")
st.markdown('## <span id="interest_rate">🏦 1. Interest Rate Helpers</span>', unsafe_allow_html=True)

tab_ir1, tab_ir2, tab_ir3 = st.tabs(["💰 Cash & FRAs", "📈 Swaps & OIS", "📅 Futures & IMM"])

with tab_ir1:
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.markdown("### DepositRateHelper")
        st.markdown("For short-term cash rates (Libor/Euribor/Overnight).")
        st.code("""
# ql.DepositRateHelper(rate, tenor, fixingDays, calendar, convention, eom, dc)
h1 = ql.DepositRateHelper(0.05, ql.Period('6M'), 2, ql.TARGET(), ql.ModifiedFollowing, False, ql.Actual360())

# Simplified (using index)
h2 = ql.DepositRateHelper(0.05, ql.Euribor6M())
""")
    with col_c2:
        st.markdown("### FraRateHelper")
        st.markdown("Forward Rate Agreements.")
        st.code("""
# ql.FraRateHelper(rate, monthsToStart, index)
h3 = ql.FraRateHelper(0.05, 1, ql.Euribor6M())

# Comprehensive signature
h4 = ql.FraRateHelper(quote, monthsToStart, monthsToEnd, fixingDays, calendar, convention, eom, dc)
""")

with tab_ir2:
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown("### SwapRateHelper")
        st.markdown("The standard for bootstrapping the long end of the curve.")
        st.code("""
# Using Swap Index
h = ql.SwapRateHelper(0.05, ql.EuriborSwapIsdaFixA(ql.Period('10y')))

# Detail params
h = ql.SwapRateHelper(rate, tenor, calendar, fixedFreq, fixedConv, fixedDC, iborIndex)
""")
        st.markdown("### OISRateHelper")
        st.markdown("Overnight Indexed Swaps.")
        st.code("h = ql.OISRateHelper(2, ql.Period('2y'), rate, overnightIndex)")
        
    with col_s2:
        st.markdown("### Bond Helpers")
        st.code("""
# ql.FixedRateBondHelper(price, settlementDays, faceAmount, schedule, coupons, dc)
h = ql.FixedRateBondHelper(ql.QuoteHandle(ql.SimpleQuote(105)), 2, 100, schedule, [0.05], dc)

# ql.BondHelper(cleanPrice, bondObject)
h = ql.BondHelper(quote, bond)
""")
        st.markdown("### FX Swap Helper")
        st.code("ql.FxSwapRateHelper(fwdPoints, spot, tenor, fixingDays, calendar, convention, eom, isCollateral, ytsCurve)")

with tab_ir3:
    st.markdown("### FuturesRateHelper")
    st.code("""
# ql.FuturesRateHelper(price, iborStartDate, iborIndex, convexityAdjustment=0.0)
h = ql.FuturesRateHelper(99.5, ql.Date(17,6,2020), ql.Euribor3M())

# SOFR/Overnight Futures
h = ql.SofrFutureRateHelper(99.9, 3, 2024, ql.Quarterly, ql.Sofr())
""")
    st.markdown("### IMM Dates (Utility)")
    st.code("""
ql.IMM.date('M0') # Current IMM
ql.IMM.code(ql.Date(16,12,2020)) # returns 'Z0'
ql.IMM.nextDate(ql.Date().todaysDate())
""")

# ===================================================
# 🌪️ 2. VOLATILITY HELPERS
# ===================================================

st.markdown("---")
st.markdown('## <span id="vol_helpers">🌪️ 2. Volatility Calibration Helpers</span>', unsafe_allow_html=True)

st.markdown("""
Calibration helpers ensure a stochastic model (like Black, Heston, or SABR) matches market prices of Caps, Swaptions, or Vanilla Options.
""")

col_v1, col_v2 = st.columns(2)

with col_v1:
    st.markdown("### Cap & Swaption")
    st.code("""
# CapHelper
h = ql.CapHelper(ql.Period('2y'), volQuote, index, ql.Semiannual, dc, False, yts)

# SwaptionHelper
h = ql.SwaptionHelper(maturity, length, vol, index, fixedTenor, fixedDC, floatDC, yts)
""")

with col_v2:
    st.markdown("### Heston & Model calibration")
    st.code("""
# HestonModelHelper handles spot, strike, vol, and IR/Div curves
h = ql.HestonModelHelper(tenor, calendar, spot, strike, vol, riskFreeTS, divTS)
""")

# ===================================================
# 🛡️ 3. CREDIT & INFLATION
# ===================================================

st.markdown("---")
col_c1, col_inf1 = st.columns(2)

with col_c1:
    st.markdown('## <span id="credit_helpers">🛡️ 3. Credit Helpers</span>', unsafe_allow_html=True)
    st.code("""
# ql.SpreadCdsHelper(runningSpread, tenor, settlementDays, calendar, frequency, ...)
h = ql.SpreadCdsHelper(spread, ql.Period('5Y'), 2, ql.TARGET(), ql.Quarterly, ql.Following, ...)
""")

with col_inf1:
    st.markdown('## <span id="inflation_helpers">🎈 4. Inflation Helpers</span>', unsafe_allow_html=True)
    st.code("""
# ql.ZeroCouponInflationSwapHelper(quote, period, date, calendar, convention, dc, index, interpl, yts)
h = ql.ZeroCouponInflationSwapHelper(quote, ql.Period('1Y'), today, ql.TARGET(), ql.ModifiedFollowing, dc, index, ql.CPI, yts)
""")

# ===================================================
# 🧪 BOOTSTRAPPING SIMULATION
# ===================================================

st.markdown("---")
st.markdown('## <span id="bootstrap_demo">🧪 Bootstrapping Simulation</span>', unsafe_allow_html=True)

st.markdown("""
This demo simulates **Curve Stripping**. Adjust the market rates below to see how the interpolated Zero Curve matches the inputs.
""")

b_col1, b_col2 = st.columns([1, 2])

with b_col1:
    st.markdown("### Market Input Quotes")
    depo_6m = st.slider("6M Deposit Rate (%)", 1.0, 8.0, 3.5, step=0.1)
    swap_2y = st.slider("2Y Swap Rate (%)", 1.0, 8.0, 4.0, step=0.1)
    swap_5y = st.slider("5Y Swap Rate (%)", 1.0, 8.0, 4.2, step=0.1)
    swap_10y = st.slider("10Y Swap Rate (%)", 1.0, 8.0, 4.5, step=0.1)
    
    st.markdown("### Curve Properties")
    interpl_choice = st.radio("Interpolation", ["LinearZero", "LogLinearDiscount", "CubicZero"])

with b_col2:
    # Logic for Bootstrap demo
    today = ql.Date().todaysDate()
    ql.Settings.instance().evaluationDate = today
    
    helpers = []
    helpers.append(ql.DepositRateHelper(depo_6m / 100, ql.Euribor6M()))
    helpers.append(ql.SwapRateHelper(swap_2y / 100, ql.EuriborSwapIsdaFixA(ql.Period('2y'))))
    helpers.append(ql.SwapRateHelper(swap_5y / 100, ql.EuriborSwapIsdaFixA(ql.Period('5y'))))
    helpers.append(ql.SwapRateHelper(swap_10y / 100, ql.EuriborSwapIsdaFixA(ql.Period('10y'))))
    
    if interpl_choice == "LogLinearDiscount":
        curve = ql.PiecewiseLogLinearDiscount(today, helpers, ql.Actual360())
    elif interpl_choice == "CubicZero":
        curve = ql.PiecewiseCubicZero(today, helpers, ql.Actual360())
    else:
        curve = ql.PiecewiseLinearZero(today, helpers, ql.Actual360())
    
    # Enable extrapolation to avoid out-of-range errors
    curve.enableExtrapolation()
    
    # Generate points for plotting - match the 10Y max maturity
    times = np.linspace(0.1, 10, 100)
    zeros = [curve.zeroRate(t, ql.Continuous).rate() * 100 for t in times]
    
    # Plotting
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor('none')
    ax.set_facecolor('none')
    
    ax.plot(times, zeros, label=f"Interpolated Zero Curve ({interpl_choice})", color='#00d4ff', linewidth=2)
    
    # Mark input points
    input_times = [0.5, 2.0, 5.0, 10.0]
    input_rates = [depo_6m, swap_2y, swap_5y, swap_10y]
    ax.scatter(input_times, input_rates, color='#ffd700', zorder=5, label="Market Fixings")
    
    ax.set_title("Bootstrap Result: Zero Yield Curve", color='white')
    ax.set_xlabel("Time to Maturity (Years)", color='white')
    ax.set_ylabel("Yield (%)", color='white')
    ax.tick_params(colors='white')
    ax.legend()
    ax.grid(alpha=0.2)
    
    st.pyplot(fig)

# ===================================================
#  NAVIGATION
# ===================================================

st.markdown("---")

nav_col1, nav_col2, nav_nav3, nav_col4 = st.columns([1, 1, 1, 1])

with nav_col1:
    if st.button("⬅️ Previous: Term Structures"):
        st.switch_page("pages/11_Term_Structures.py")

with nav_col4:
    st.markdown("""
<style>
    div[data-testid="stHorizontalBlock"] > div:nth-child(4) button {
        margin-left: auto;
        display: block;
    }
</style>
""", unsafe_allow_html=True)
    if st.button("➡️ Next: Fixed Income"):
        st.switch_page("pages/13_Fixed_Income.py")
