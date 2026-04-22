import streamlit as st
import QuantLib as ql
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import math

st.set_page_config(page_title="QuantLib - Term Structures", layout="wide")

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
</style>
""", unsafe_allow_html=True)

st.title("📉 Term Structures")

st.markdown("""
A term structure describes the evolution of a variable $X(t, T)$ indexed by current time $t$ and maturity $T$. 
In QuantLib, these structures are the backbone of all valuation engines.
""")

# ===================================================
# 📚 TABLE OF CONTENTS
# ===================================================

st.markdown("## 📚 Table of Contents")

st.markdown("""
<div style="line-height:2; font-size:16px;">
🔹 <a href="#yield" target="_self">1. Yield Term Structures</a><br>
🔹 <a href="#volatility" target="_self">2. Volatility Term Structures</a><br>
🔹 <a href="#credit" target="_self">3. Credit Term Structures</a><br>
🔹 <a href="#inflation" target="_self">4. Inflation Term Structures</a><br>
</div>
""", unsafe_allow_html=True)

# ===================================================
# 💸 1. YIELD TERM STRUCTURES
# ===================================================

st.markdown("---")
st.markdown('## <span id="yield">💸 1. Yield Term Structures</span>', unsafe_allow_html=True)

y_tab1, y_tab2, y_tab3 = st.tabs(["📜 Base API", "🌿 Common Curves", "🧩 Piecewise & Fitting"])

with y_tab1:
    st.markdown("### Interface: YieldTermStructure")
    st.markdown("All yield curves inherit methods for Discount Factors, Zero Rates, and Forwards.")
    st.code("""
# Discounting
df = curve.discount(date) # or time
# Zero Yield
zero = curve.zeroRate(date, dayCounter, ql.Continuous, ql.Annual)
# Forward Rate
fwd = curve.forwardRate(d1, d2, dayCounter, ql.Continuous)
""")
    st.info("💡 **Tip**: Use `jumpDates()` and `jumpTimes()` to inspect curve discontinuities.")

with y_tab2:
    col_y1, col_y2 = st.columns(2)
    with col_y1:
        st.markdown("#### FlatForward")
        st.code("ql.FlatForward(settlementDays, calendar, rate, dayCounter)")
        
        st.markdown("#### ZeroCurve")
        st.markdown("Interpolates zero-coupon yields.")
        st.code("ql.ZeroCurve(dates, yields, dayCounter, calendar)")
    
    with col_y2:
        st.markdown("#### DiscountCurve")
        st.markdown("Log-linear interpolation of discount factors.")
        st.code("ql.DiscountCurve(dates, dfs, dayCounter)")
        
        st.markdown("#### ForwardCurve")
        st.code("ql.ForwardCurve(dates, rates, dayCounter)")

with y_tab3:
    st.markdown("#### Bootstrapping: Piecewise Curves")
    st.code("""
helpers = [ql.DepositRateHelper(...), ql.SwapRateHelper(...)]
# Options: PiecewiseLogLinearDiscount, PiecewiseLinearZero, PiecewiseCubicZero, etc.
curve = ql.PiecewiseLogLinearDiscount(referenceDate, helpers, ql.Actual360())
""")
    
    st.markdown("#### Fitting: FittedBondDiscountCurve")
    st.markdown("Least-squares fitting of bond prices to a functional form.")
    st.code("""
method = ql.NelsonSiegelFitting() # or SvenssonFitting, CubicBSplinesFitting
curve = ql.FittedBondDiscountCurve(settlementDate, helpers, dayCounter, method)
""")

# 🎮 INTERACTIVE: YIELD CURVE VISUALIZER
st.markdown("#### 🎮 Interactive Yield Curve Visualizer")
y_slider = st.select_slider("Select Curve Shape", ["Flat", "Normal (Up)", "Inverted (Down)", "Humped"], value="Normal (Up)")

# Math for Visualizer
t = np.linspace(0.1, 30, 100)
if y_slider == "Flat": r = 0.05 * np.ones_like(t)
elif y_slider == "Normal (Up)": r = 0.02 + 0.04 * (1 - np.exp(-0.2 * t))
elif y_slider == "Inverted (Down)": r = 0.06 - 0.03 * (1 - np.exp(-0.2 * t))
else: r = 0.03 + 0.05 * t * np.exp(-0.3 * t)

fig_y = go.Figure()
fig_y.add_trace(go.Scatter(x=t, y=r*100, mode='lines', name='Zero Rate', line=dict(color='#00d4ff', width=3)))
fig_y.update_layout(title="Yield Curve Shape Simulation", xaxis_title="Maturity (Years)", yaxis_title="Rate (%)", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
st.plotly_chart(fig_y, use_container_width=True)

# ===================================================
# 🌪️ 2. VOLATILITY TERM STRUCTURES
# ===================================================

st.markdown("---")
st.markdown('## <span id="volatility">🌪️ 2. Volatility Term Structures</span>', unsafe_allow_html=True)

v_tab1, v_tab2, v_tab3 = st.tabs(["🎭 Smile Sections", "🧊 Vol Surfaces", "🧢 Cap & Swaption Vol"])

with v_tab1:
    st.markdown("### SmileSection Interface")
    st.markdown("Represents a horizontal slice of the vol surface at a fixed maturity.")
    st.code("""
smile.volatility(strike)
smile.variance(strike)
smile.optionPrice(strike, ql.Option.Call)
""")
    st.markdown("#### Model Parametrizations")
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.markdown("**SABR Smile**")
        st.code("ql.SabrSmileSection(time, forward, [alpha, beta, nu, rho])")
        st.markdown("**SVI Smile**")
        st.code("ql.SviSmileSection(time, forward, [a, b, sigma, rho, m])")
    with col_v2:
        st.markdown("**Kahale Regularizer**")
        st.markdown("Removes butterfly/calendar arbitrage from a source smile.")
        st.code("ql.KahaleSmileSection(source_smile)")

with v_tab2:
    st.markdown("#### Black Vol (Implied)")
    st.code("""
# Simplest: Constant Vol
ql.BlackConstantVol(refDate, calendar, 0.20, dayCounter)
# 2D Interpolated Surface
ql.BlackVarianceSurface(refDate, cal, expDates, strikes, volMatrix, dc)
""")
    st.markdown("#### Local Vol (Dupire)")
    st.code("ql.LocalVolSurface(blackVolHandle, ratesTs, divTs, spot)")

with v_tab3:
    st.markdown("#### Cap/Floor Volatility")
    st.code("ql.CapFloorTermVolSurface(settlementDays, cal, bdc, expuries, strikes, matrix)")
    st.markdown("#### Swaption Volatility Matrix")
    st.code("ql.SwaptionVolatilityMatrix(cal, bdc, optTenors, swapTenors, matrix, dc)")

# 🎮 INTERACTIVE: SABR SMILE PLAYGROUND
st.markdown("#### 🎮 Interactive SABR Smile Playground")
sv_c1, sv_c2 = st.columns([1, 2])
with sv_c1:
    s_alpha = st.slider("Alpha (Level)", 0.01, 1.0, 0.3)
    s_beta = st.slider("Beta (Backbone)", 0.0, 1.0, 0.8)
    s_nu = st.slider("Nu (Vol-of-Vol)", 0.0, 1.0, 0.4)
    s_rho = st.slider("Rho (Skew)", -0.99, 0.99, -0.5)

# Simplified SABR Approx (Strike-Dependent Smile)
strikes = np.linspace(70, 130, 60)
fwd = 100
T = 1.0

# Simple quadratic smile for visualization (Alpha: level, Nu: conv, Rho: skew)
atm_vol = s_alpha
skew = s_rho * s_nu * 0.5 
convexity = (s_nu**2) * (1 - s_beta + 0.1) * 2.0
z = (strikes - fwd) / fwd
vol = atm_vol + skew * z + convexity * (z**2)

fig_v = go.Figure()
fig_v.add_trace(go.Scatter(x=strikes, y=vol*100, mode='lines', name='SABR Smile', line=dict(color='#00ff88', width=3)))
fig_v.update_layout(title="SABR Implied Volatility Smile", xaxis_title="Strike", yaxis_title="Implied Vol (%)", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
with sv_c2:
    st.plotly_chart(fig_v, use_container_width=True)

# ===================================================
# 🛡️ 3. CREDIT TERM STRUCTURES
# ===================================================

st.markdown("---")
st.markdown('## <span id="credit">🛡️ 3. Credit Term Structures</span>', unsafe_allow_html=True)

col_cr1, col_cr2 = st.columns(2)

with col_cr1:
    st.markdown("### Default Probability Interface")
    st.markdown("Maps time to the probability of default or survival.")
    st.code("""
# Hazard Rate (Instantaneous)
prob.hazardRate(time)
# Survival Probability
prob.survivalProbability(time)
# Default Probability
prob.defaultProbability(time)
""")

with col_cr2:
    st.markdown("#### FlatHazardRate")
    st.code("ql.FlatHazardRate(settlementDays, calendar, rateQuote, dc)")
    
    st.markdown("#### SurvivalProbabilityCurve")
    st.code("ql.SurvivalProbabilityCurve(dates, probabilities, dc, cal)")

st.markdown("#### PiecewiseFlatHazardRate (Bootstrapped)")
st.code("""
# Bootstrapped from CDS spreads
helpers = [ql.SpreadCdsHelper(spread, tenor, ...) for spread in spreads]
curve = ql.PiecewiseFlatHazardRate(today, helpers, ql.Actual360())
""")

# ===================================================
# 🎈 4. INFLATION TERM STRUCTURES
# ===================================================

st.markdown("---")
st.markdown('## <span id="inflation">🎈 4. Inflation Term Structures</span>', unsafe_allow_html=True)

st.markdown("""
QuantLib handles both **Zero Inflation** (CPI indexes) and **Year-on-Year Inflation** curves.
""")

col_inf1, col_inf2 = st.columns(2)

with col_inf1:
    st.markdown("### Zero Inflation")
    st.code("""
# Base class for CPI-linked products
ql.ZeroInflationCurve(dates, rates, dayCounter...)

# Piecewise Bootstrapped
ql.PiecewiseZeroInflation(refDate, calendar, dc, lag, frequency, ...)
""")

with col_inf2:
    st.markdown("### YoY Inflation")
    st.code("""
# Represents Year-on-Year percentage change
ql.YoYInflationCurve(dates, rates, dayCounter...)
""")

# ===================================================
#  NAVIGATION
# ===================================================

st.markdown("---")

st.markdown("""
<style>
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) button {
        margin-left: auto;
        display: block;
    }
</style>
""", unsafe_allow_html=True)

nav_col1, nav_col2, nav_col3, nav_col4 = st.columns([1, 1, 1, 1])

with nav_col1:
    if st.button("⬅️ Previous: Stochastic Processes"):
        st.switch_page("pages/10_Stochastic_Processes.py")

with nav_col4:
    if st.button("➡️ Next: Helpers"):
        st.switch_page("pages/12_Helpers.py")
