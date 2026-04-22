import streamlit as st
import QuantLib as ql
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="QuantLib - Pricing Models", layout="wide")

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
    .stButton>button {
        background: linear-gradient(90deg, #00d4ff, #0055ff);
        color: white;
        border: none;
        padding: 10px 25px;
        border-radius: 8px;
        font-weight: bold;
        transition: 0.3s;
    }
</style>
""", unsafe_allow_html=True)

st.title("📈 Pricing Models")

# ===================================================
# 📚 TABLE OF CONTENTS
# ===================================================

st.markdown("## 📚 Table of Contents")

st.markdown("""
<div style="line-height:2; font-size:16px;">
🔹 <a href="#equity" target="_self">1. Equity Models</a><br>
🔹 <a href="#onefactor" target="_self">2. Short Rate: One-Factor Models</a><br>
🔹 <a href="#twofactor" target="_self">3. Short Rate: Two-Factor Models</a><br>
🔹 <a href="#sim" target="_self">4. Interactive Vasicek Simulation</a><br>
</div>
""", unsafe_allow_html=True)

# ===================================================
# 🍎 1. EQUITY MODELS
# ===================================================

st.markdown("---")
st.markdown('## <span id="equity">🍎 1. Equity Models</span>', unsafe_allow_html=True)

eq_tab1, eq_tab2 = st.tabs(["🔥 Heston Model", "🧬 Bates & PTD"])

with eq_tab1:
    st.markdown("### Standard Heston Model")
    st.markdown("Captures volatility skew/smile by modeling volatility as a stochastic process.")
    st.code("""
# Parameters: v0, kappa, theta, sigma, rho
v0, kappa, theta, sigma, rho = 0.005, 0.6, 0.01, 0.4, -0.15

hestonProcess = ql.HestonProcess(riskFreeTS, dividendTS, s0, v0, kappa, theta, sigma, rho)
hestonModel = ql.HestonModel(hestonProcess)
""")

with eq_tab2:
    st.markdown("### Piecewise Time-Dependent Heston")
    st.markdown("Allows parameters to vary over different time intervals.")
    st.code("""
times = [1.0, 2.0, 3.0]
grid = ql.TimeGrid(times)

# Setup Parameter TS
kappaTS = ql.PiecewiseConstantParameter(times[:-1], ql.PositiveConstraint())
# ... setParam(i, val) for each parameter ...

model = ql.PiecewiseTimeDependentHestonModel(
    riskFreeTS, dividendTS, s0, v0, thetaTS, kappaTS, sigmaTS, rhoTS, grid
)
""")
    st.markdown("### Bates Model")
    st.info("Heston model extended with jump processes. (API: `ql.BatesModel`)")

# ===================================================
# 🏛️ 2. ONE-FACTOR MODELS
# ===================================================

st.markdown("---")
st.markdown('## <span id="onefactor">🏛️ 2. Short Rate: One-Factor Models</span>', unsafe_allow_html=True)

col_f1, col_f2 = st.columns(2)

with col_f1:
    st.markdown("### Vasicek Model")
    st.markdown("Classic mean-reverting model. $dr_t = a(b-r_t)dt + \sigma dW_t$")
    st.code("model = ql.Vasicek(r0=0.05, a=0.1, b=0.05, sigma=0.01)")

    st.markdown("### Black-Karasinski")
    st.markdown("Log-normal short rate model ($r_t$ always positive).")
    st.code("model = ql.BlackKarasinski(yts, a=0.1, sigma=0.1)")

with col_f2:
    st.markdown("### Hull-White")
    st.markdown("Extended Vasicek model that fits the initial term structure exactly.")
    st.code("model = ql.HullWhite(yts, a=0.1, sigma=0.01)")

    st.markdown("### GSR Model")
    st.markdown("One-factor GSR model (Forward measure).")
    st.code("model = ql.Gsr(yts, volDates, vols, reversions)")

# ===================================================
# 🛡️ 3. TWO-FACTOR MODELS
# ===================================================

st.markdown("---")
st.markdown('## <span id="twofactor">🛡️ 3. Short Rate: Two-Factor Models</span>', unsafe_allow_html=True)

st.markdown("### G2 Model")
st.markdown("A two-factor model that allows for more realistic yield curve dynamics and decorrelation.")
st.code("""
# Parameters: a, sigma, b, eta, rho
model = ql.G2(yts, a=0.1, sigma=0.01, b=0.1, eta=0.01, rho=-0.75)
""")

# ===================================================
# 🎮 4. INTERACTIVE SIMULATION
# ===================================================

st.markdown("---")
st.markdown('## <span id="sim">🎮 4. Interactive Simulation Playground</span>', unsafe_allow_html=True)

st.markdown("""
Compare how different short-rate models evolve over time. 
- **Vasicek**: Linear mean reversion ($r_t$ can be negative).
- **Black-Karasinski**: Mean reversion in $\ln(r_t)$ (always positive).
- **Hull-White**: Time-dependent mean reversion (fits yield curve).
- **GSR**: One-factor Gaussian Short Rate.
""")

sc1, sc2 = st.columns([1, 2])

with sc1:
    m_choice = st.selectbox("Select Model", ["Vasicek", "Black-Karasinski", "Hull-White", "GSR"])
    v_r0 = st.slider("Initial Rate ($r_0$)", 0.0, 0.10, 0.05, step=0.005)
    v_a = st.slider("Reversion Speed ($a$)", 0.0, 2.0, 0.1)
    
    if m_choice == "Black-Karasinski":
         v_b = st.slider("Long-term Mean ($\ln(b)$)", -5.0, -1.0, -3.0) # Using log scale for BK
         v_sigma = st.slider("Volatility ($\sigma$)", 0.0, 0.5, 0.1, step=0.01)
    else:
         v_b = st.slider("Long-term Mean ($b$)", 0.0, 0.10, 0.05, step=0.005)
         v_sigma = st.slider("Volatility ($\sigma$)", 0.0, 0.05, 0.01, step=0.001)
         
    n_paths = st.number_input("Paths", 1, 50, 10)

with sc2:
    # Simulation Logic (Euler-Maruyama)
    T = 5.0
    dt = 1/252
    steps = int(T/dt)
    t = np.linspace(0, T, steps)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor('none')
    ax.set_facecolor('none')
    
    for i in range(n_paths):
        r = np.zeros(steps)
        
        if m_choice == "Black-Karasinski":
            x = np.zeros(steps)
            x[0] = np.log(v_r0) if v_r0 > 0 else -10 # Safety
            for j in range(1, steps):
                dx = v_a * (v_b - x[j-1]) * dt + v_sigma * np.sqrt(dt) * np.random.normal()
                x[j] = x[j-1] + dx
            r = np.exp(x)
        else:
            # Vasicek, Hull-White, GSR (Simplification for constant b)
            r[0] = v_r0
            for j in range(1, steps):
                dr = v_a * (v_b - r[j-1]) * dt + v_sigma * np.sqrt(dt) * np.random.normal()
                r[j] = r[j-1] + dr
                
        ax.plot(t, r, alpha=0.6)
    
    if m_choice != "Black-Karasinski":
        ax.axhline(v_b, color='red', linestyle='--', label=f'Mean (b={v_b})')
    else:
        ax.axhline(np.exp(v_b), color='red', linestyle='--', label=f'Mean (e^b={np.exp(v_b):.4f})')
        
    ax.set_title(f"{m_choice} Model Paths", color='white')
    ax.set_xlabel("Time (Years)", color='white')
    ax.set_ylabel("Short Rate", color='white')
    ax.tick_params(colors='white')
    ax.legend()
    st.pyplot(fig)

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
    if st.button("⬅️ Previous: Engines"):
        st.switch_page("pages/08_Pricing_Engines.py")

with nav_col4:
    if st.button("➡️ Next: Term Structures"):
        st.switch_page("pages/09_Term_Structures.py")
