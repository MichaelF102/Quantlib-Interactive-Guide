import streamlit as st
import QuantLib as ql
import pandas as pd
import numpy as np

st.set_page_config(page_title="QuantLib - Pricing Engines", layout="wide")

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
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.5);
    }
</style>
""", unsafe_allow_html=True)

st.title("⚙️ Pricing Engines & Calculators")

# ===================================================
# 📚 TABLE OF CONTENTS
# ===================================================

st.markdown("## 📚 Table of Contents")

st.markdown("""
<div style="line-height:2; font-size:16px;">
🔹 <a href="#blackbach" target="_self">1. Black & Bachelier Engines</a><br>
🔹 <a href="#bond" target="_self">2. Bond Pricing Engines</a><br>
🔹 <a href="#capfloor" target="_self">3. Cap & Floor Engines</a><br>
🔹 <a href="#swap" target="_self">4. Swap & Swaption Engines</a><br>
🔹 <a href="#credit" target="_self">5. Credit Pricing Engines</a><br>
🔹 <a href="#option" target="_self">6. Option Pricing Engines</a><br>
🔹 <a href="#fx" target="_self">7. FX Specific Calculators</a><br>
</div>
""", unsafe_allow_html=True)

# ===================================================
# 📊 1. BLACK & BACHELIER
# ===================================================

st.markdown("---")
st.markdown('## <span id="blackbach">📊 1. Black & Bachelier</span>', unsafe_allow_html=True)

st.markdown("""
Black and Bachelier formulas are the bedrock of derivative valuation. 
- **Black (1976)**: Assumes lognormal dynamics (positive values only).
- **Bachelier (1900)**: Assumes normal dynamics (allows negative rates).
""")

# 🎮 INTERACTIVE: DUAL CALCULATOR
st.markdown("#### 🎮 Interactive Dual Calculator (Black vs Bachelier)")

col_calc1, col_calc2 = st.columns([1, 2])

with col_calc1:
    c_type = st.radio("Option Type", ["Call", "Put"], horizontal=True)
    c_forward = st.number_input("Forward Price/Rate", value=1.0, step=0.1)
    c_strike = st.number_input("Strike", value=1.0, step=0.1)
    c_vol = st.slider("Volatility (%)", 1, 100, 20) / 100.0
    c_tte = st.slider("Time to Expiration (Years)", 0.1, 10.0, 1.0)
    
    q_type = ql.Option.Call if c_type == "Call" else ql.Option.Put
    std_dev = c_vol * np.sqrt(c_tte)
    payoff = ql.PlainVanillaPayoff(q_type, c_strike)

with col_calc2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    # QuantLib Calculations
    black_calc = ql.BlackCalculator(payoff, c_forward, std_dev)
    bach_calc = ql.BachelierCalculator(payoff, c_forward, std_dev)
    
    res1, res2 = st.columns(2)
    with res1:
        st.subheader("Black (Lognormal)")
        st.metric("Price", f"{black_calc.value():.6f}")
        st.metric("Delta", f"{black_calc.deltaForward():.4f}")
    
    with res2:
        st.subheader("Bachelier (Normal)")
        st.metric("Price", f"{bach_calc.value():.6f}")
        st.metric("Delta", f"{bach_calc.deltaForward():.4f}")
        
    st.markdown('</div>', unsafe_allow_html=True)
    st.info("💡 **Insight**: Compare results when the Forward is near zero. The Bachelier model remains stable!")

# ===================================================
# 💸 2. BOND PRICING ENGINES
# ===================================================

st.markdown("---")
st.markdown('## <span id="bond">💸 2. Bond Pricing Engines</span>', unsafe_allow_html=True)

st.markdown("""
Bond engines transform a stream of cash flows into a present value. QuantLib provides engines for standard discounting, as well as complex optionality (Call/Put) using Black models or Trees.
""")

col_b1, col_b2 = st.columns(2)

with col_b1:
    st.markdown("### 📜 DiscountingBondEngine")
    st.markdown("The workhorse for standard Fixed and Floating rate bonds.")
    st.code("""
# 1. Setup Curve
today = ql.Date().todaysDate()
crv = ql.FlatForward(today, 0.0487, ql.Actual365Fixed())
yts = ql.YieldTermStructureHandle(crv)

# 2. Setup Engine
engine = ql.DiscountingBondEngine(yts)

# 3. Apply to Bond
bond.setPricingEngine(engine)
print(f"NPV: {bond.NPV()}")
""")

with col_b2:
    st.markdown("### 🍎 BlackCallableBondEngine")
    st.markdown("Prices bonds with embedded American/European call/put features using the Black model.")
    st.code("""
# 1. Setup Yield Volatility
vol = ql.QuoteHandle(ql.SimpleQuote(0.55))

# 2. Setup Engine
engine = ql.BlackCallableFixedRateBondEngine(vol, yts)

# 3. Apply
callableBond.setPricingEngine(engine)
""")

st.markdown("### 🌲 TreeCallableFixedRateBondEngine")
st.markdown("""
Lattice-based engine that uses a short-rate model (e.g., Vasicek, Hull-White) to price callable features. 
QuantLib supports four distinct ways to initialize this engine:
""")

ov1, ov2 = st.columns(2)

with ov1:
    st.markdown("**Overload 1: Model + Size + Curve**")
    st.code("""
model = ql.Vasicek()
engine = ql.TreeCallableFixedRateBondEngine(
    model, 10, yts
)
""")
    st.markdown("**Overload 2: Model + Size**")
    st.code("""
model = ql.Vasicek()
engine = ql.TreeCallableFixedRateBondEngine(model, 10)
""")

with ov2:
    st.markdown("**Overload 3: Model + TimeGrid + Curve**")
    st.code("""
grid = ql.TimeGrid(5, 10) # 5 years, 10 steps
engine = ql.TreeCallableFixedRateBondEngine(
    model, grid, yts
)
""")
    st.markdown("**Overload 4: Model + TimeGrid**")
    st.code("""
engine = ql.TreeCallableFixedRateBondEngine(model, grid)
""")

# ===================================================
# 🧢 3. CAP & FLOOR ENGINES
# ===================================================

st.markdown("---")
st.markdown('## <span id="capfloor">🧢 3. Cap & Floor Engines</span>', unsafe_allow_html=True)

st.markdown("""
Caps and Floors are standard IR derivatives valued using either constant volatility (Black/Bachelier) or dynamic short-rate models.
""")

cap_tab1, cap_tab2 = st.tabs(["⚡ Volatility Engines", "🌲 Model Engines"])

with cap_tab1:
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.markdown("### BlackCapFloorEngine")
        st.markdown("👉 Lognormal dynamics ($σ_{log}$).")
        st.code("""
vols = ql.QuoteHandle(ql.SimpleQuote(0.5472))
engine = ql.BlackCapFloorEngine(yts, vols)

# Using Volatility Structure
# engine = ql.BlackCapFloorEngine(yts, volStructure)
""")
    with col_v2:
        st.markdown("### BachelierCapFloorEngine")
        st.markdown("👉 Normal dynamics ($σ_{normal}$).")
        st.code("""
vols = ql.QuoteHandle(ql.SimpleQuote(0.0054))
engine = ql.BachelierCapFloorEngine(yts, vols)
""")

with cap_tab2:
    st.markdown("### 🏛️ AnalyticCapFloorEngine")
    st.markdown("Closed-form solutions for one-factor affine models (Hull-White, Vasicek).")
    st.code("""
models = [
    ql.HullWhite(yts, a=0.1, sigma=0.01),
    ql.Vasicek(r0=0.008, a=0.1, b=0.05, sigma=0.01)
]

for model in models:
    engine = ql.AnalyticCapFloorEngine(model, yts)
    cap.setPricingEngine(engine)
""")

    st.markdown("### 🌲 TreeCapFloorEngine")
    st.markdown("Lattice-based valuation for American/Bermudan or complex short-rate structures.")
    st.code("""
# Supported Models: 
# HullWhite, BlackKarasinski, Vasicek, G2

model = ql.G2(yts, a=0.1, sigma=0.01, b=0.1, eta=0.01, rho=-0.75)
treeEngine = ql.TreeCapFloorEngine(model, 60, yts)
""")
    
    with st.expander("🔍 View All Tree Overloads"):
        st.code("""
# 1. Model + Size + Curve
ql.TreeCapFloorEngine(model, 60, yts)
# 2. Model + Size
ql.TreeCapFloorEngine(model, 60)
# 3. Model + Size + TimeGrid + Curve
ql.TreeCapFloorEngine(model, 60, grid, yts)
""")

# ===================================================
# 🔁 4. SWAP & SWAPTION ENGINES
# ===================================================

st.markdown("---")
st.markdown('## <span id="swap">🔁 4. Swap & Swaption Engines</span>', unsafe_allow_html=True)

st.markdown("""
Standard Swaps are valued by discounting cashflows on both legs. Swaptions, however, require specialized engines to handle the optionality on the underlying swap.
""")

sw_tab1, sw_tab2 = st.tabs(["📊 Standard Engines", "🧪 Numerical Engines"])

with sw_tab1:
    st.markdown("### 📜 DiscountingSwapEngine")
    st.markdown("Standard engine for Vanilla, Basis, and Asset Swaps.")
    st.code("""
yts = ql.YieldTermStructureHandle(ql.FlatForward(2, ql.TARGET(), 0.05, ql.Actual360()))
engine = ql.DiscountingSwapEngine(yts)
swap.setPricingEngine(engine)
""")

    st.markdown("### 🍎 Black & Bachelier Swaption")
    st.markdown("Closed-form pricing using lognormal or normal volatility.")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.code("""
# Black (Lognormal)
vols = ql.QuoteHandle(ql.SimpleQuote(0.25))
blackEng = ql.BlackSwaptionEngine(yts, vols)

# With DayCounter & Displacement
# blackEng = ql.BlackSwaptionEngine(yts, vols, ql.Actual360(), 0.01)
""")
    with col_s2:
        st.code("""
# Bachelier (Normal)
vols_n = ql.QuoteHandle(ql.SimpleQuote(0.0055))
bachEng = ql.BachelierSwaptionEngine(yts, vols_n)
swaption.setPricingEngine(bachEng)
""")

with sw_tab2:
    st.markdown("### 🧩 Finite Difference & Analytic")
    st.markdown("Advanced engines for one and two-factor models.")
    
    col_sn1, col_sn2 = st.columns(2)
    with col_sn1:
        st.markdown("**FD Engines (Numerical)**")
        st.code("""
model_hw = ql.HullWhite(yts)
# FD Hull-White
fdHwEng = ql.FdHullWhiteSwaptionEngine(model_hw)

# FD G2
model_g2 = ql.G2(yts)
fdG2Eng = ql.FdG2SwaptionEngine(model_g2)
""")
    with col_sn2:
        st.markdown("**Analytic Engines**")
        st.code("""
# Jamshidian (One-Factor)
jamEng = ql.JamshidianSwaptionEngine(model_hw, yts)

# G2 Analytic
g2Eng = ql.G2SwaptionEngine(model_g2, 4, 4)
""")

    st.markdown("### 🌲 TreeSwaptionEngine")
    st.code("""
# Initialize using Market Model and Lattice Size
model = ql.HullWhite(yts)
treeEng = ql.TreeSwaptionEngine(model, 10) # 10 steps
swaption.setPricingEngine(treeEng)
""")

# ===================================================
# 🛡️ 5. CREDIT PRICING ENGINES
# ===================================================

st.markdown("---")
st.markdown('## <span id="credit">🛡️ 5. Credit Pricing Engines</span>', unsafe_allow_html=True)

st.markdown("""
Credit engines require both a **Yield Term Structure** (for discounting) and a **Default Probability Term Structure** (Hazard Rate).
""")

# Shared Setup Code Snippet
with st.expander("📝 View Shared Credit Setup (Hazard Rate)"):
    st.code("""
today = ql.Date().todaysDate()
# 1. Yield Curve
yts = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.05, ql.Actual360()))

# 2. Hazard Rate / Default Probability
prob = ql.DefaultProbabilityTermStructureHandle(
    ql.FlatHazardRate(today, ql.QuoteHandle(ql.SimpleQuote(0.01)), ql.Actual360())
)
recoveryRate = 0.4
""")

col_c1, col_c2 = st.columns(2)

with col_c1:
    st.markdown("### 🏛️ Standard CDS Engines")
    st.markdown("QuantLib supports standard ISDA models and simplified midpoint valuation.")
    st.code("""
# ISDA Engine (Market Standard)
isdaEng = ql.IsdaCdsEngine(prob, recoveryRate, yts)

# MidPoint Engine
midEng = ql.MidPointCdsEngine(prob, recoveryRate, yts)
""")

with col_c2:
    st.markdown("### 🧪 Numerical & Options")
    st.markdown("Numerical integration engines and Black-based CDS options.")
    st.code("""
# Integral Engine (Custom Step)
step = ql.Period('1d')
intEng = ql.IntegralCdsEngine(step, prob, recoveryRate, yts)

# Black CDS Option Engine
vol = ql.QuoteHandle(ql.SimpleQuote(0.2))
optEng = ql.BlackCdsOptionEngine(prob, recoveryRate, yts, vol)
""")


## ===================================================
# 🎰 6. OPTION PRICING ENGINES
# ===================================================

st.markdown("---")
st.markdown('## <span id="option">🎰 6. Option Pricing Engines</span>', unsafe_allow_html=True)

st.markdown("""Option engines are categorized by the payoff type (Vanilla, Asian, Barrier) and the numerical method (Analytic, Monte Carlo, Finite Difference).
""")

# 🎮 SIMULATION: ANALYTIC vs MONTE CARLO
st.markdown("#### 🎮 Simulation: Analytic vs Monte Carlo")

sim_col1, sim_col2 = st.columns([1, 2])

with sim_col1:
    s_paths = st.select_slider("MC Samples", options=[1000, 10000, 50000, 100000, 500000], value=50000)
    s_steps = st.number_input("Time Steps", value=1, min_value=1)
    
    if st.button("🚀 Run Comparison"):
        today = ql.Date().todaysDate()
        ql.Settings.instance().evaluationDate = today
        
        # Setup BSM Process
        spot = ql.QuoteHandle(ql.SimpleQuote(100))
        rTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.05, ql.Actual365Fixed()))
        dTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.0, ql.Actual365Fixed()))
        vTS = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today, ql.NullCalendar(), 0.20, ql.Actual365Fixed()))
        process = ql.BlackScholesMertonProcess(spot, dTS, rTS, vTS)
        
        # Instrument
        payoff = ql.PlainVanillaPayoff(ql.Option.Call, 100)
        exercise = ql.EuropeanExercise(today + ql.Period("1Y"))
        option = ql.VanillaOption(payoff, exercise)
        
        # 1. Analytic
        option.setPricingEngine(ql.AnalyticEuropeanEngine(process))
        a_npv = option.NPV()
        
        # 2. Monte Carlo
        option.setPricingEngine(ql.MCEuropeanEngine(process, "pseudorandom", s_steps, requiredSamples=s_paths, seed=42))
        m_npv = option.NPV()
        
        with sim_col2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            res1, res2 = st.columns(2)
            res1.metric("Analytic NPV", f"{a_npv:.4f}")
            res2.metric("Monte Carlo NPV", f"{m_npv:.4f}")
            diff = abs(a_npv - m_npv)
            st.write(f"**Convergence Error:** {diff/a_npv:.4%}")
            st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# 🏛️ EXHAUSTIVE ENGINE REGISTRY
opt_tabs = st.tabs(["🍎 Vanilla", "🛡️ Barrier", "🧬 Asian & Exotics"])

with opt_tabs[0]:
    st.markdown("### 🍎 Vanilla Options (European & American)")
    with st.expander("📝 View Analytic & MC Engines"):
        st.markdown("**AnalyticEuropeanEngine**: Standard closed-form BSM.")
        st.code("engine = ql.AnalyticEuropeanEngine(process)")
        st.markdown("**MCEuropeanEngine**: Path-dependent simulation.")
        st.code("engine = ql.MCEuropeanEngine(process, 'pseudorandom', steps, requiredSamples=paths)")
        st.markdown("**MCAmericanEngine**: Least-squares MC for American exercize.")
        st.code("engine = ql.MCAmericanEngine(process, 'pseudorandom', steps, requiredSamples=paths)")

    with st.expander("📝 View Finite Difference (FD) Engines"):
        st.info("💡 **Pro-Tip**: FD engines can price both American and European payoffs!")
        st.code("engine = ql.FdBlackScholesVanillaEngine(process, tGrid=2000, xGrid=200)")

    with st.expander("📝 View Heston Model Engines"):
        st.markdown("**AnalyticHestonEngine**: Heston semi-analytic pricer.")
        st.code("model = ql.HestonModel(hestonProcess); engine = ql.AnalyticHestonEngine(model)")
        st.markdown("**FdHestonVanillaEngine**: FD solution for Heston (supports SLV).")
        st.code("engine = ql.FdHestonVanillaEngine(hestonModel, tGrid, xGrid, vGrid)")

with opt_tabs[1]:
    st.markdown("### 🛡️ Barrier & Double Barrier Options")
    st.write("QuantLib supports single, double, binary, and partial-time barriers.")
    
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        st.markdown("**Single Barriers**")
        st.code("""
# Binomial
ql.BinomialBarrierEngine(bsm, 'crr', 200)

# Vanna-Volga (FX Standard)
ql.VannaVolgaBarrierEngine(atmVol, p25Vol, c25Vol, spot, usdTS, eurTS)

# Finite Difference
ql.FdBlackScholesBarrierEngine(bsm)
""")
    with col_b2:
        st.markdown("**Exotic Barriers**")
        st.code("""
# Double Barrier
ql.AnalyticDoubleBarrierEngine(bsm)

# Rebate Engine (FD)
ql.FdBlackScholesRebateEngine(bsm)

# Partial Time Barrier
ql.AnalyticPartialTimeBarrierOptionEngine(bsm)
""")

with opt_tabs[2]:
    st.markdown("### 🧬 Asian, Basket & Forward Options")
    
    with st.expander("🔭 View Asian Option Engines"):
        st.markdown("Supports Discrete/Continuous and Arithmetic/Geometric averaging.")
        st.code("""
# Analytic Geometric
ql.AnalyticDiscreteGeometricAveragePriceAsianEngine(process)

# MC Arithmetic (Most Common)
ql.MCDiscreteArithmeticAPEngine(process, 'pseudorandom', requiredSamples=100000)

# Turnbull-Wakeman
ql.TurnbullWakemanAsianEngine(process)
""")

    with st.expander("🔭 View Basket & Forward Engines"):
        st.code("""
# Basket (Multi-asset Correlation)
ql.MCEuropeanBasketEngine(stochasticProcessArray, 'pseudorandom', requiredSamples=500000)

# Forward Start / Cliquet
ql.ForwardEuropeanEngine(process) # Prices forward-starting vanilla
""")

# ===================================================
# 💱 7. FX SPECIFIC CALCULATORS
# ===================================================

st.markdown("---")
st.markdown('## <span id="fx">💱 7. FX Specific Calculators</span>', unsafe_allow_html=True)

st.markdown("""
The `BlackDeltaCalculator` is used to construct volatility smiles and quote FX options by delta.
""")

col_fx1, col_fx2 = st.columns([2, 1])

with col_fx1:
    st.code("""
# 1. Setup Calculator
stdDev = np.sqrt(maturity) * vol
calc = ql.BlackDeltaCalculator(ql.Option.Put, ql.DeltaVolQuote.Fwd, spot, domDf, forDf, stdDev)

# 2. Key Member Functions
strike = calc.strikeFromDelta(-0.25)
delta  = calc.deltaFromStrike(105)
atm    = calc.atmStrike(ql.DeltaVolQuote.AtmFwd)
""")

with col_fx2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.write("**Supported ATM Conventions:**")
    st.write("- `AtmSpot` / `AtmForward`")
    st.write("- `AtmDeltaNeutral`")
    st.write("- `AtmVegaMax` / `AtmGammaMax`")
    st.markdown('</div>', unsafe_allow_html=True)

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
    if st.button("⬅️ Previous: Math Tools"):
        st.switch_page("pages/07_Math_Tools.py")

with nav_col4:
    if st.button("➡️ Next: Pricing Models"):
        st.switch_page("pages/09_Pricing_Models.py")
