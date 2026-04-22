import streamlit as st
import QuantLib as ql
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

st.set_page_config(
    page_title="QuantLib · Stochastic Processes",
    layout="wide",
    initial_sidebar_state="collapsed",
)
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
# ───────────────────────────────────────────────
#  GLOBAL CSS
# ───────────────────────────────────────────────


# ───────────────────────────────────────────────
#  HEADER
# ───────────────────────────────────────────────

st.title("Stochastic Processes")
st.markdown('<p class="subtitle">A comprehensive reference for every process in QuantLib — from simple GBM to calibrated Heston-SLV, organised by model family with runnable simulations.</p>', unsafe_allow_html=True)

# ===================================================
# 📚 TABLE OF CONTENTS
# ===================================================

st.markdown("## 📚 Table of Contents")

st.markdown("""
<div style="line-height:2; font-size:16px;">
🔹 <a href="#sec01" target="_self">1. Brownian & Black-Scholes Family</a><br>
🔹 <a href="#sec02" target="_self">2. Mean Reversion & Jump Processes</a><br>
🔹 <a href="#sec03" target="_self">3. Advanced Equity (Merton, VG, GK)</a><br>
🔹 <a href="#sec04" target="_self">4. Stochastic Volatility (Heston, Bates, SLV)</a><br>
🔹 <a href="#sec05" target="_self">5. Interest Rate (Hull-White, GSR, G2)</a><br>
🔹 <a href="#sec06" target="_self">6. Multi-Asset Arrays</a><br>
🔹 <a href="#playground" target="_self">🧪 Simulation Playground</a><br>
</div>
""", unsafe_allow_html=True)

# ───────────────────────────────────────────────
#  SECTION 01 — BROWNIAN & BLACK-SCHOLES
# ───────────────────────────────────────────────
st.markdown('<a name="sec01"></a>', unsafe_allow_html=True)
st.markdown("## 01 — Brownian & Black-Scholes Family")
st.markdown('<p class="subtitle">The foundation of equity and FX modelling. GBM drives the classic Black-Scholes PDE; the four process variants below differ only in what additional yield curves they consume.</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="medium")

with col1:
    st.markdown('<div class="card card-accent-blue">', unsafe_allow_html=True)
    st.markdown("### GeometricBrownianMotion")
    st.markdown('<span class="process-tag">ql.GeometricBrownianMotionProcess</span>', unsafe_allow_html=True)
    st.code("""initialValue = 100
mu, sigma = 0.01, 0.2
process = ql.GeometricBrownianMotionProcess(
    initialValue, mu, sigma
)""", language="python")
    st.markdown("Simplest process. Drift `mu` and diffusion `sigma` are constants. No yield curve required.", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card card-accent-blue">', unsafe_allow_html=True)
    st.markdown("### BlackScholesProcess")
    st.markdown('<span class="process-tag">ql.BlackScholesProcess</span>', unsafe_allow_html=True)
    st.code("""initialValue = ql.QuoteHandle(ql.SimpleQuote(100))
today  = ql.Date().todaysDate()
riskFreeTS = ql.YieldTermStructureHandle(
    ql.FlatForward(today, 0.05, ql.Actual365Fixed()))
volTS = ql.BlackVolTermStructureHandle(
    ql.BlackConstantVol(today, ql.NullCalendar(),
                        0.2, ql.Actual365Fixed()))

process = ql.BlackScholesProcess(
    initialValue, riskFreeTS, volTS
)""", language="python")
    st.markdown("Adds a risk-free curve. No dividend yield (i.e. implicitly zero).")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card card-accent-blue">', unsafe_allow_html=True)
    st.markdown("### BlackScholesMertonProcess")
    st.markdown('<span class="process-tag">ql.BlackScholesMertonProcess</span>', unsafe_allow_html=True)
    st.code("""dividendTS = ql.YieldTermStructureHandle(
    ql.FlatForward(today, 0.01, ql.Actual365Fixed()))

process = ql.BlackScholesMertonProcess(
    initialValue, dividendTS, riskFreeTS, volTS
)""", language="python")
    st.markdown("The industry-standard process for equity options — adds continuous dividend yield.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card card-accent-blue">', unsafe_allow_html=True)
    st.markdown("### GeneralizedBlackScholesProcess")
    st.markdown('<span class="process-tag">ql.GeneralizedBlackScholesProcess</span><span class="process-tag">ql.BlackProcess</span>', unsafe_allow_html=True)
    st.code("""# Full signature — same as BSM
process = ql.GeneralizedBlackScholesProcess(
    initialValue, dividendTS, riskFreeTS, volTS
)

# Black's model (futures / forward prices)
process = ql.BlackProcess(
    initialValue, riskFreeTS, volTS
)""", language="python")
    st.markdown("`GeneralizedBlackScholesProcess` is the abstract base; `BlackProcess` is for futures/forwards where the spot IS the forward.")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ───────────────────────────────────────────────
#  SECTION 02 — MEAN REVERSION & JUMPS
# ───────────────────────────────────────────────
st.markdown('<a name="sec02"></a>', unsafe_allow_html=True)
st.markdown("## 02 — Mean Reversion & Jump Processes")
st.markdown('<p class="subtitle">Ornstein-Uhlenbeck variants model variables that revert to a long-run mean — essential for interest rates, energy prices, and commodity spreads.</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="medium")

with col1:
    st.markdown('<div class="card card-accent-purple">', unsafe_allow_html=True)
    st.markdown("### ExtendedOrnsteinUhlenbeckProcess")
    st.markdown('<span class="process-tag">ql.ExtendedOrnsteinUhlenbeckProcess</span>', unsafe_allow_html=True)
    st.code("""x0       = 0.0     # initial value
speed    = 1.0     # mean reversion speed κ
volatility = 0.1  # diffusion σ

# Mean level supplied as a callable
process = ql.ExtendedOrnsteinUhlenbeckProcess(
    speed, volatility, x0,
    lambda x: x0          # constant mean = x0
)""", language="python")
    st.markdown("The `lambda` allows a **time-varying mean** — pass a callable `f(t)` for any term structure of mean levels.")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card card-accent-purple">', unsafe_allow_html=True)
    st.markdown("### ExtOUWithJumpsProcess")
    st.markdown('<span class="process-tag">ql.ExtOUWithJumpsProcess</span>', unsafe_allow_html=True)
    st.code("""x0, x1       = 0.0, 0.0
beta         = 4.0   # jump mean-reversion speed
eta          = 4.0   # jump size (exponential)
jumpIntensity = 1.0  # Poisson intensity λ

ouProcess = ql.ExtendedOrnsteinUhlenbeckProcess(
    speed, volatility, x0, lambda x: x0
)
process = ql.ExtOUWithJumpsProcess(
    ouProcess, x1, beta, jumpIntensity, eta
)""", language="python")
    st.markdown("Combines diffusive mean-reversion with Poisson jump arrivals — popular in **power & gas spot models** (Kluge/Burger).")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ───────────────────────────────────────────────
#  SECTION 03 — ADVANCED EQUITY
# ───────────────────────────────────────────────
st.markdown('<a name="sec03"></a>', unsafe_allow_html=True)
st.markdown("## 03 — Advanced Equity — Merton 76, Variance Gamma, Garman-Kohlhagen")
st.markdown('<p class="subtitle">Models that incorporate price jumps or non-normal return distributions to capture market skew, kurtosis, and FX-specific rate structures.</p>', unsafe_allow_html=True)

tab_m76, tab_vg, tab_gk = st.tabs(["📈 Merton 76 (Jump-Diffusion)", "⚡ Variance Gamma", "💱 Garman-Kohlhagen (FX)"])

with tab_m76:
    col1, col2 = st.columns([3, 2], gap="medium")
    with col1:
        st.markdown('<div class="card card-accent-pink">', unsafe_allow_html=True)
        st.markdown("### Merton76Process")
        st.markdown('<span class="process-tag">ql.Merton76Process</span>', unsafe_allow_html=True)
        st.code("""initialValue = ql.QuoteHandle(ql.SimpleQuote(100))
today  = ql.Date().todaysDate()
sigma  = 0.2

dividendTS = ql.YieldTermStructureHandle(
    ql.FlatForward(today, 0.01, ql.Actual365Fixed()))
riskFreeTS = ql.YieldTermStructureHandle(
    ql.FlatForward(today, 0.05, ql.Actual365Fixed()))
volTS = ql.BlackVolTermStructureHandle(
    ql.BlackConstantVol(today, ql.NullCalendar(),
                        sigma, ql.Actual365Fixed()))

jumpIntensity = ql.QuoteHandle(ql.SimpleQuote(1.0))
jumpVol = sigma * np.sqrt(0.25 / 1.0)
jumpVolatility = ql.QuoteHandle(ql.SimpleQuote(jumpVol))
meanLogJump    = ql.QuoteHandle(
    ql.SimpleQuote(-jumpVol**2))        # ensures E[jump]=0

process = ql.Merton76Process(
    initialValue, dividendTS, riskFreeTS, volTS,
    jumpIntensity, meanLogJump, jumpVolatility
)""", language="python")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="card" style="margin-top:1.5rem">', unsafe_allow_html=True)
        st.markdown("**Key Parameters**")
        st.markdown("""
| Symbol | Meaning |
|--------|---------|
| `jumpIntensity` | Poisson rate λ (jumps/yr) |
| `meanLogJump` | Mean of log-jump size μ_J |
| `jumpVolatility` | Std-dev of log-jump σ_J |
        """)
        st.markdown("Set `meanLogJump = -0.5 * σ_J²` to ensure the **compensated jump** has zero expectation under the risk-neutral measure.")
        st.markdown('</div>', unsafe_allow_html=True)

with tab_vg:
    col1, col2 = st.columns([3, 2], gap="medium")
    with col1:
        st.markdown('<div class="card card-accent-pink">', unsafe_allow_html=True)
        st.markdown("### VarianceGammaProcess")
        st.markdown('<span class="process-tag">ql.VarianceGammaProcess</span>', unsafe_allow_html=True)
        st.code("""initialValue = ql.QuoteHandle(ql.SimpleQuote(100))
today      = ql.Date().todaysDate()
riskFreeTS = ql.YieldTermStructureHandle(
    ql.FlatForward(today, 0.05, ql.Actual365Fixed()))
dividendTS = ql.YieldTermStructureHandle(
    ql.FlatForward(today, 0.01, ql.Actual365Fixed()))

sigma = 0.2   # volatility of Brownian component
nu    = 1.0   # variance rate of Gamma time-change
theta = 1.0   # drift of Brownian in Gamma-time (skew)

process = ql.VarianceGammaProcess(
    initialValue, dividendTS, riskFreeTS,
    sigma, nu, theta
)""", language="python")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="card" style="margin-top:1.5rem">', unsafe_allow_html=True)
        st.markdown("**Intuition**")
        st.markdown("VG subordinates a drifted Brownian motion to a Gamma random clock. It captures **fat tails** (`ν` large) and **skew** (`θ ≠ 0`) without continuous diffusion noise — returns are purely jump-driven in the limit.")
        st.markdown('</div>', unsafe_allow_html=True)

with tab_gk:
    col1, col2 = st.columns([3, 2], gap="medium")
    with col1:
        st.markdown('<div class="card card-accent-pink">', unsafe_allow_html=True)
        st.markdown("### GarmanKohlagenProcess")
        st.markdown('<span class="process-tag">ql.GarmanKohlagenProcess</span>', unsafe_allow_html=True)
        st.code("""initialValue = ql.QuoteHandle(ql.SimpleQuote(1.10))  # EUR/USD spot
today        = ql.Date().todaysDate()

domesticTS = ql.YieldTermStructureHandle(       # USD
    ql.FlatForward(today, 0.05, ql.Actual365Fixed()))
foreignTS  = ql.YieldTermStructureHandle(       # EUR
    ql.FlatForward(today, 0.03, ql.Actual365Fixed()))
volTS = ql.BlackVolTermStructureHandle(
    ql.BlackConstantVol(today, ql.NullCalendar(),
                        0.08, ql.Actual365Fixed()))

process = ql.GarmanKohlagenProcess(
    initialValue, foreignTS, domesticTS, volTS
)""", language="python")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="card" style="margin-top:1.5rem">', unsafe_allow_html=True)
        st.markdown("**BSM analogy for FX**")
        st.markdown("The **foreign risk-free rate** plays the role of the dividend yield. The drift of the spot under the domestic risk-neutral measure is `r_d − r_f`.")
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ───────────────────────────────────────────────
#  SECTION 04 — STOCHASTIC VOLATILITY
# ───────────────────────────────────────────────
st.markdown('<a name="sec04"></a>', unsafe_allow_html=True)
st.markdown("## 04 — Stochastic Volatility — Heston, Bates & SLV")
st.markdown('<p class="subtitle">Two-factor models where variance itself follows a diffusion, producing realistic volatility smiles and term structures.</p>', unsafe_allow_html=True)

tab_h, tab_b, tab_slv = st.tabs(["⚡ HestonProcess", "🔀 BatesProcess", "🎯 HestonSLVProcess"])

with tab_h:
    col1, col2 = st.columns([3, 2], gap="medium")
    with col1:
        st.markdown('<div class="card card-accent-green">', unsafe_allow_html=True)
        st.markdown("### HestonProcess")
        st.markdown('<span class="process-tag">ql.HestonProcess</span>', unsafe_allow_html=True)
        st.code("""today      = ql.Date().todaysDate()
riskFreeTS = ql.YieldTermStructureHandle(
    ql.FlatForward(today, 0.05, ql.Actual365Fixed()))
dividendTS = ql.YieldTermStructureHandle(
    ql.FlatForward(today, 0.01, ql.Actual365Fixed()))

s0    = ql.QuoteHandle(ql.SimpleQuote(100))
v0    = 0.04    # initial variance
kappa = 2.0     # mean-reversion speed
theta = 0.04    # long-run variance
sigma = 0.3     # vol-of-vol
rho   = -0.7    # spot-vol correlation

process = ql.HestonProcess(
    riskFreeTS, dividendTS, s0,
    v0, kappa, theta, sigma, rho
)""", language="python")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="card" style="margin-top:1.5rem">', unsafe_allow_html=True)
        st.markdown("**Feller condition**")
        st.markdown("For variance to stay strictly positive: `2κθ > σ²`. Violating it allows variance to hit zero — QuantLib still runs but CIR discretisation artefacts appear.")
        st.markdown("")
        st.markdown("**Calibration tip:** `rho < 0` tilts the smile left (equity skew). Increase `sigma` to widen wings.")
        st.markdown('</div>', unsafe_allow_html=True)

with tab_b:
    col1, col2 = st.columns([3, 2], gap="medium")
    with col1:
        st.markdown('<div class="card card-accent-green">', unsafe_allow_html=True)
        st.markdown("### BatesProcess")
        st.markdown('<span class="process-tag">ql.BatesProcess</span>', unsafe_allow_html=True)
        st.code("""# Bates = Heston + log-normal jumps in the spot
# Extra params vs Heston:
#   lambda  — Poisson jump intensity
#   nu      — mean log-jump size
#   delta   — std-dev of log-jump

lambda_ = 0.5      # ~0.5 jumps/year
nu      = -0.10    # average -10% jump
delta   = 0.15     # jump-size std-dev

process = ql.BatesProcess(
    riskFreeTS, dividendTS, s0,
    v0, kappa, theta, sigma, rho,
    lambda_, nu, delta
)""", language="python")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="card" style="margin-top:1.5rem">', unsafe_allow_html=True)
        st.markdown("**When to prefer Bates over Heston**")
        st.markdown("Short-dated skew that Heston alone cannot reproduce — the jumps fill in near-term smile curvature while Heston handles the long end.")
        st.markdown('</div>', unsafe_allow_html=True)

with tab_slv:
    st.markdown('<div class="card card-accent-green">', unsafe_allow_html=True)
    st.markdown("### HestonSLVProcess — Stochastic Local Volatility")
    st.markdown('<span class="process-tag">ql.HestonSLVProcess</span><span class="process-tag">ql.HestonSLVMCModel</span>', unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1], gap="medium")
    with col1:
        st.code("""# ── 1. Local vol surface ──────────────────────────────
periods = [ql.Period(p) for p in ["3M","6M","12M","24M"]]
expDates = [today + p for p in periods]
strikes  = [90, 95, 100, 105, 110]
data = [
    [0.075, 0.076, 0.078, 0.080],  # K=90
    [0.071, 0.072, 0.074, 0.078],  # K=95
    [0.071, 0.072, 0.073, 0.077],  # K=100
    [0.075, 0.075, 0.075, 0.077],  # K=105
    [0.081, 0.080, 0.078, 0.078],  # K=110
]
impliedVols = ql.Matrix(data)
lvSurface = ql.BlackVarianceSurface(
    today, ql.NullCalendar(), expDates, strikes,
    impliedVols, ql.Actual365Fixed())
lvHandle = ql.BlackVolTermStructureHandle(lvSurface)
localVol  = ql.LocalVolSurface(
    lvHandle, riskFreeTS, dividendTS, s0)
localVol.enableExtrapolation()

# ── 2. Calibrate leverage function via MC ─────────────
endDate   = today + ql.Period("2Y")
generator = ql.MTBrownianGeneratorFactory()
hestonModel     = ql.HestonModel(hestonProcess)
stochLocalModel = ql.HestonSLVMCModel(
    localVol, hestonModel, generator, endDate,
    365,   # timeStepsPerYear
    201,   # nBins
    2**15, # calibrationPaths
    [],    # mandatoryDates
    0.9    # mixingFactor
)
leverageFct = stochLocalModel.leverageFunction()

# ── 3. Instantiate process ────────────────────────────
process = ql.HestonSLVProcess(
    hestonProcess, leverageFct, mixingFactor=0.9
)""", language="python")
    with col2:
        st.markdown("**mixingFactor α**")
        st.markdown("- `α = 1.0` → pure local vol\n- `α = 0.0` → pure Heston\n- `α = 0.9` → typical SLV blend")
        st.markdown("")
        st.markdown("The **leverage function L(S,t)** is calibrated so the marginal distribution of the SLV process exactly matches market-implied densities — guaranteeing perfect vanilla smile fit with realistic dynamics.")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ───────────────────────────────────────────────
#  SECTION 05 — INTEREST RATE
# ───────────────────────────────────────────────
st.markdown('<a name="sec05"></a>', unsafe_allow_html=True)
st.markdown("## 05 — Interest Rate Processes — Hull-White, GSR & G2")
st.markdown('<p class="subtitle">Short-rate and forward-rate processes used to price interest rate derivatives — caps, floors, swaptions, and exotic rate products.</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="medium")

with col1:
    st.markdown('<div class="card card-accent-orange">', unsafe_allow_html=True)
    st.markdown("### HullWhiteProcess & HullWhiteForwardProcess")
    st.markdown('<span class="process-tag">ql.HullWhiteProcess</span><span class="process-tag">ql.HullWhiteForwardProcess</span>', unsafe_allow_html=True)
    st.code("""today      = ql.Date().todaysDate()
riskFreeTS = ql.YieldTermStructureHandle(
    ql.FlatForward(today, 0.05, ql.Actual365Fixed()))

a     = 0.001   # mean-reversion speed
sigma = 0.01    # short-rate volatility

# Risk-neutral (spot) measure
hwProcess = ql.HullWhiteProcess(riskFreeTS, a, sigma)

# T-forward measure — required for some engines
hwFwdProcess = ql.HullWhiteForwardProcess(
    riskFreeTS, a, sigma
)
hwFwdProcess.setForwardMeasureTime(2.0)  # set horizon T""", language="python")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card card-accent-orange">', unsafe_allow_html=True)
    st.markdown("### GsrProcess")
    st.markdown('<span class="process-tag">ql.GsrProcess</span>', unsafe_allow_html=True)
    st.code("""today = ql.Date().todaysDate()

# Piecewise σ(t) and κ(t) — allows term structure
times     = [1.0, 2.0, 3.0, 5.0, 7.0, 10.0]
sigmas    = [0.010, 0.011, 0.012, 0.011, 0.010, 0.010, 0.009]
reversions = [0.01]    # single constant reversion

process = ql.GsrProcess(times, sigmas, reversions)""", language="python")
    st.markdown("`len(sigmas) == len(times) + 1` — the last sigma applies beyond the last time. GSR is the generalised one-factor Gaussian model, matching a fitted term structure of vol.")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card card-accent-orange">', unsafe_allow_html=True)
    st.markdown("### G2Process & G2ForwardProcess")
    st.markdown('<span class="process-tag">ql.G2Process</span><span class="process-tag">ql.G2ForwardProcess</span>', unsafe_allow_html=True)
    st.code("""# G2++ two-factor Gaussian short-rate model
# r(t) = x(t) + y(t) + φ(t)
# dx = -a*x dt + σ dW1
# dy = -b*y dt + η dW2
#  corr(W1,W2) = ρ

a     = 0.1     # mean-reversion speed factor 1
sigma = 0.01    # vol factor 1
b     = 0.2     # mean-reversion speed factor 2
eta   = 0.01    # vol factor 2
rho   = -0.75   # factor correlation

process = ql.G2Process(a, sigma, b, eta, rho)

# T-Forward variant (used with path-dependent engines)
process = ql.G2ForwardProcess(a, sigma, b, eta, rho)""", language="python")
    st.markdown("G2++ is the two-factor extension of Hull-White, producing **humped vol term structures** and better fit to co-terminal swaption matrices.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card" style="background:rgba(251,146,60,0.05); border:1px solid rgba(251,146,60,0.2);">', unsafe_allow_html=True)
    st.markdown("**Model selection guide**")
    st.markdown("""
| Need | Model |
|---|---|
| Exact fit to initial curve | HW / GSR |
| Humped vol surface | G2++ |
| Piecewise σ(t) | GSR |
| Swaption matrix calibration | G2++ |
| Path-dep, Bermudan swaptions | GSR (Markov) |
    """)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ───────────────────────────────────────────────
#  SECTION 06 — MULTI-ASSET
# ───────────────────────────────────────────────
st.markdown('<a name="sec06"></a>', unsafe_allow_html=True)
st.markdown("## 06 — Multi-Asset Process Arrays")
st.markdown('<p class="subtitle">Combine individual processes into a correlated array for basket options, worst-of payoffs, and multi-currency products.</p>', unsafe_allow_html=True)

col1, col2 = st.columns([3, 2], gap="medium")
with col1:
    st.markdown('<div class="card card-accent-blue">', unsafe_allow_html=True)
    st.markdown("### StochasticProcessArray")
    st.markdown('<span class="process-tag">ql.StochasticProcessArray</span>', unsafe_allow_html=True)
    st.code("""today    = ql.Date().todaysDate()
dayCount = ql.Actual365Fixed()
calendar = ql.NullCalendar()

riskFreeTS = ql.YieldTermStructureHandle(
    ql.FlatForward(today, 0.0, dayCount))
dividendTS = ql.YieldTermStructureHandle(
    ql.FlatForward(today, 0.0, dayCount))

spots = [100.0, 105.0, 98.0, 110.0, 95.0]
vols  = [0.10,  0.12,  0.13, 0.09,  0.11]

# 5×5 correlation matrix
corrMatrix = [
    [1.00, 0.10,-0.10, 0.00, 0.00],
    [0.10, 1.00, 0.00, 0.00, 0.20],
    [-0.10,0.00, 1.00, 0.00, 0.00],
    [0.00, 0.00, 0.00, 1.00, 0.15],
    [0.00, 0.20, 0.00, 0.15, 1.00],
]

processes = [
    ql.BlackScholesMertonProcess(
        ql.QuoteHandle(ql.SimpleQuote(s)),
        dividendTS, riskFreeTS,
        ql.BlackVolTermStructureHandle(
            ql.BlackConstantVol(today, calendar, v, dayCount))
    )
    for s, v in zip(spots, vols)
]

multiProcess = ql.StochasticProcessArray(
    processes, corrMatrix
)""", language="python")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card" style="margin-top:1.5rem">', unsafe_allow_html=True)
    st.markdown("**Cholesky decomposition**")
    st.markdown("QuantLib decomposes the correlation matrix internally via Cholesky — the matrix must be positive semi-definite. Use `ql.checkPositiveSemiDefiniteness()` to validate first.")
    st.markdown("")
    st.markdown("**Typical use-cases**")
    st.markdown("- Rainbow / worst-of options\n- Basket options\n- Multi-currency hybrids\n- Spread options (energy, equity)")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ───────────────────────────────────────────────
#  INTERACTIVE SIMULATION PLAYGROUND
# ───────────────────────────────────────────────
st.markdown('<a name="playground"></a>', unsafe_allow_html=True)
st.markdown("## 🧪 Simulation Playground")
st.markdown('<p class="subtitle">Generate Monte Carlo paths for any process family. Adjust parameters and see the effect in real time.</p>', unsafe_allow_html=True)

# Control panel
ctrl_col1, ctrl_col2 = st.columns([1.2, 1.2], gap="medium")

with ctrl_col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    process_choice = st.selectbox(
        "Process Family",
        [
            "Geometric Brownian Motion",
            "Black-Scholes (const vol)",
            "OU / Mean Reversion",
            "OU with Jumps",
            "Merton 76 (Jump-Diffusion)",
            "Heston (Stochastic Vol)",
            "Variance Gamma",
            "Multi-Asset GBM (3 assets)",
        ],
        index=0
    )
    n_paths = st.slider("Paths", 2, 40, 8, step=2)
    T_years = st.slider("Horizon (years)", 0.5, 5.0, 2.0, step=0.5)
    seed = st.number_input("Random Seed", min_value=0, max_value=999, value=42)
    st.markdown('</div>', unsafe_allow_html=True)

with ctrl_col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    S0 = st.number_input("Spot S₀", value=100.0, step=5.0)
    sigma = st.slider("Volatility σ", 0.05, 0.80, 0.20, step=0.01)
    mu    = st.slider("Drift / Rate μ", -0.05, 0.15, 0.05, step=0.01)

    show_extra = process_choice in [
        "OU / Mean Reversion", "OU with Jumps",
        "Merton 76 (Jump-Diffusion)", "Heston (Stochastic Vol)",
        "Multi-Asset GBM (3 assets)"
    ]
    if show_extra:
        if "OU" in process_choice or "Mean" in process_choice:
            kappa_ou = st.slider("Mean-rev speed κ", 0.1, 10.0, 2.0, step=0.1)
        elif "Heston" in process_choice:
            kappa_h  = st.slider("Vol mean-rev κ", 0.5, 5.0, 2.0, step=0.1)
            rho_h    = st.slider("Spot-vol corr ρ", -0.95, 0.95, -0.70, step=0.05)
        elif "Merton" in process_choice:
            jump_lam = st.slider("Jump intensity λ", 0.0, 5.0, 1.5, step=0.1)
            jump_mu  = st.slider("Mean log-jump μ_J", -0.30, 0.10, -0.08, step=0.01)
    st.markdown('</div>', unsafe_allow_html=True)

# ── SIMULATION ──────────────────────────────────
np.random.seed(int(seed))
dt    = 1/252
steps = max(2, int(T_years / dt))
t     = np.linspace(0, T_years, steps)

# Colour palettes
PALETTES = {
    "Geometric Brownian Motion":   plt.cm.Blues,
    "Black-Scholes (const vol)":   plt.cm.Blues,
    "OU / Mean Reversion":         plt.cm.Purples,
    "OU with Jumps":               plt.cm.RdPu,
    "Merton 76 (Jump-Diffusion)":  plt.cm.Oranges,
    "Heston (Stochastic Vol)":     plt.cm.cool,
    "Variance Gamma":              plt.cm.YlOrRd,
    "Multi-Asset GBM (3 assets)":  None,
}

def make_gbm_path(S0, mu, sigma, dt, steps):
    path = np.empty(steps); path[0] = S0
    for j in range(1, steps):
        path[j] = path[j-1] * np.exp((mu - 0.5*sigma**2)*dt + sigma*np.sqrt(dt)*np.random.normal())
    return path

def make_ou_path(x0, kappa, sigma, dt, steps):
    path = np.empty(steps); path[0] = x0
    for j in range(1, steps):
        path[j] = path[j-1] + kappa*(x0 - path[j-1])*dt + sigma*np.sqrt(dt)*np.random.normal()
    return path

def make_ou_jumps_path(x0, kappa, sigma, dt, steps, lam=1.0):
    path = np.empty(steps); path[0] = x0
    for j in range(1, steps):
        jump = np.random.exponential(1.0) if np.random.rand() < lam*dt else 0.0
        path[j] = path[j-1] + kappa*(x0 - path[j-1])*dt + sigma*np.sqrt(dt)*np.random.normal() + jump
    return path

def make_merton_path(S0, mu, sigma, dt, steps, lam, mu_j):
    path = np.empty(steps); path[0] = S0
    sigma_j = abs(mu_j) * 0.8 + 0.05
    for j in range(1, steps):
        jmp = np.random.normal(mu_j, sigma_j) if np.random.rand() < lam*dt else 0.0
        path[j] = path[j-1] * np.exp((mu - 0.5*sigma**2)*dt + sigma*np.sqrt(dt)*np.random.normal() + jmp)
    return path

def make_heston_paths(S0, mu, sigma, dt, steps, kappa, rho):
    S = np.empty(steps); S[0] = S0
    V = np.empty(steps); V[0] = sigma**2
    theta = sigma**2; vol_of_vol = 0.3
    for j in range(1, steps):
        z1 = np.random.normal(); z2 = np.random.normal()
        w1 = z1; w2 = rho*z1 + np.sqrt(1-rho**2)*z2
        S[j] = S[j-1] * np.exp((mu - 0.5*V[j-1])*dt + np.sqrt(max(V[j-1],1e-8)*dt)*w1)
        V[j] = max(1e-6, V[j-1] + kappa*(theta - V[j-1])*dt + vol_of_vol*np.sqrt(max(V[j-1],1e-8)*dt)*w2)
    return S, V

def make_vg_path(S0, mu, sigma, dt, steps):
    nu = 0.3; theta_vg = -0.1
    path = np.empty(steps); path[0] = S0
    omega = np.log(1 - theta_vg*nu - 0.5*sigma**2*nu) / nu
    for j in range(1, steps):
        g = np.random.gamma(dt/nu, nu)
        dX = theta_vg*g + sigma*np.sqrt(g)*np.random.normal()
        path[j] = path[j-1] * np.exp((mu + omega)*dt + dX)
    return path


is_heston = process_choice == "Heston (Stochastic Vol)"
is_multi  = process_choice == "Multi-Asset GBM (3 assets)"

if is_heston:
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                        vertical_spacing=0.05, 
                        subplot_titles=("Spot Price Path", "Stochastic Variance"),
                        row_heights=[0.7, 0.3])
else:
    fig = go.Figure()

cmap_colors = ["#38bdf8", "#818cf8", "#a78bfa", "#f472b6", "#fb923c", "#fbbf24", "#34d399"]
asset_colors = ["#38bdf8", "#a78bfa", "#f472b6"]

for i in range(n_paths):
    color = cmap_colors[i % len(cmap_colors)]

    if process_choice in ("Geometric Brownian Motion", "Black-Scholes (const vol)"):
        path = make_gbm_path(S0, mu, sigma, dt, steps)
        fig.add_trace(go.Scatter(x=t, y=path, mode='lines', line=dict(width=1.5, color=color), opacity=0.7, showlegend=False))

    elif process_choice == "OU / Mean Reversion":
        path = make_ou_path(S0, kappa_ou, sigma*10, dt, steps)
        fig.add_trace(go.Scatter(x=t, y=path, mode='lines', line=dict(width=1.5, color=color), opacity=0.7, showlegend=False))
        if i == 0:
            fig.add_hline(y=S0, line_dash="dash", line_color="#7dd3fc", annotation_text="Long-run Mean")

    elif process_choice == "OU with Jumps":
        k = kappa_ou if 'kappa_ou' in dir() else 2.0
        path = make_ou_jumps_path(S0, k, sigma*10, dt, steps)
        fig.add_trace(go.Scatter(x=t, y=path, mode='lines', line=dict(width=1.5, color=color), opacity=0.7, showlegend=False))
        if i == 0:
            fig.add_hline(y=S0, line_dash="dash", line_color="#7dd3fc", annotation_text="Mean Level")

    elif process_choice == "Merton 76 (Jump-Diffusion)":
        lam_v  = jump_lam if 'jump_lam' in dir() else 1.5
        mu_j_v = jump_mu  if 'jump_mu'  in dir() else -0.08
        path = make_merton_path(S0, mu, sigma, dt, steps, lam_v, mu_j_v)
        fig.add_trace(go.Scatter(x=t, y=path, mode='lines', line=dict(width=1.5, color=color), opacity=0.7, showlegend=False))

    elif process_choice == "Heston (Stochastic Vol)":
        kv  = kappa_h if 'kappa_h' in dir() else 2.0
        rhov = rho_h  if 'rho_h'  in dir() else -0.70
        S, V = make_heston_paths(S0, mu, sigma, dt, steps, kv, rhov)
        fig.add_trace(go.Scatter(x=t, y=S, mode='lines', line=dict(width=1.5, color='#38bdf8'), opacity=0.6, showlegend=False), row=1, col=1)
        fig.add_trace(go.Scatter(x=t, y=np.sqrt(V)*100, mode='lines', line=dict(width=1, color='#fb923c'), opacity=0.4, showlegend=False), row=2, col=1)

    elif process_choice == "Variance Gamma":
        path = make_vg_path(S0, mu, sigma, dt, steps)
        fig.add_trace(go.Scatter(x=t, y=path, mode='lines', line=dict(width=1.5, color=color), opacity=0.7, showlegend=False))

    elif process_choice == "Multi-Asset GBM (3 assets)":
        if i == 0: # Only one path per asset in multi-asset demo for clarity
            for k, (spot_k, vol_k, c_k) in enumerate(zip([S0, S0*0.9, S0*1.1], [sigma, sigma*0.8, sigma*1.2], asset_colors)):
                path = make_gbm_path(spot_k, mu, vol_k, dt, steps)
                fig.add_trace(go.Scatter(x=t, y=path, mode='lines', name=f"Asset {k+1} (σ={vol_k:.0%})", line=dict(width=2, color=c_k)))

# Formatting
fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=20, r=20, t=40, b=20),
    height=550,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

if is_heston:
    fig.update_yaxes(title_text="Spot Price", row=1, col=1)
    fig.update_yaxes(title_text="Vol (%)", row=2, col=1)
    fig.update_xaxes(title_text="Time (Years)", row=2, col=1)
else:
    fig.update_xaxes(title_text="Time (Years)")
    fig.update_yaxes(title_text="Price / Level")

st.plotly_chart(fig, use_container_width=True)

# ── PROCESS SUMMARY TABLE ────────────────────────
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown("## Quick Reference — All Processes")

summary_data = {
    "Process": [
        "GeometricBrownianMotion", "BlackScholesProcess", "BlackScholesMertonProcess",
        "GeneralizedBlackScholesProcess", "BlackProcess",
        "ExtendedOrnsteinUhlenbeck", "ExtOUWithJumpsProcess",
        "Merton76Process", "VarianceGammaProcess", "GarmanKohlagenProcess",
        "HestonProcess", "BatesProcess", "HestonSLVProcess",
        "HullWhiteProcess", "HullWhiteForwardProcess", "GsrProcess",
        "G2Process", "G2ForwardProcess", "StochasticProcessArray"
    ],
    "Family": [
        "BS","BS","BS","BS","BS",
        "MR","MR",
        "Adv-Eq","Adv-Eq","FX",
        "SV","SV","SV",
        "IR","IR","IR","IR","IR",
        "Multi"
    ],
    "Key Use": [
        "Teaching / quick MC", "Equity (no dividend)", "Equity + dividend",
        "Abstract base class", "Futures / forwards",
        "OU/energy/rates", "Power & gas spot",
        "Equity + price jumps", "Fat tails & skew", "FX options",
        "Equity smile", "Smile + jumps", "Smile (exact fit)",
        "Rates (spot measure)", "Rates (fwd measure)", "Piecewise σ(t)",
        "2-factor rates", "2-factor (fwd)", "Basket / worst-of"
    ],
    "Extra Params": [
        "μ, σ", "r, σ(t)", "r, q, σ(t)",
        "r, q, σ(t)", "r, σ(t)",
        "κ, σ, mean(t)", "κ, σ, β, λ, η",
        "λ, μ_J, σ_J", "σ, ν, θ", "r_f, r_d, σ(t)",
        "v₀, κ, θ, σ_v, ρ", "+λ, ν, δ", "+leverage L(S,t)",
        "a, σ", "a, σ, T*", "σᵢ(t), κᵢ(t)",
        "a, σ, b, η, ρ", "a, σ, b, η, ρ, T*", "Corr matrix"
    ]
}

import pandas as pd
df = pd.DataFrame(summary_data)
family_colors = {"BS":"#38bdf8","MR":"#a78bfa","Adv-Eq":"#f472b6",
                 "FX":"#fb923c","SV":"#34d399","IR":"#fbbf24","Multi":"#e879f9"}

def color_family(val):
    c = family_colors.get(val, "#94a3b8")
    return f"color: {c}; font-weight:600; font-family: 'DM Mono', monospace; font-size:0.78rem"

styled = (df.style
          .applymap(color_family, subset=["Family"])
          .set_properties(**{
              "background-color": "rgba(255,255,255,0.02)",
              "color": "#c8cfe8",
              "font-family": "DM Sans, sans-serif",
              "font-size": "0.83rem",
              "border": "1px solid rgba(125,211,252,0.08)",
          })
          .set_table_styles([{
              "selector": "th",
              "props": [("background","rgba(125,211,252,0.06)"),
                        ("color","#7dd3fc"),
                        ("font-family","Syne, sans-serif"),
                        ("font-size","0.78rem"),
                        ("letter-spacing","0.05em"),
                        ("border","1px solid rgba(125,211,252,0.12)")]
          }])
         )
st.dataframe(styled, use_container_width=True, height=540)

# ───────────────────────────────────────────────
#  NAVIGATION
# ───────────────────────────────────────────────
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
nav1, _, nav4 = st.columns([1, 4, 1])
with nav1:
    if st.button("← Pricing Models"):
        st.switch_page("pages/09_Pricing_Models.py")
with nav4:
    if st.button("Term Structures →"):
        st.switch_page("pages/11_Term_Structures.py")