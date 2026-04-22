import streamlit as st
import QuantLib as ql
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="QuantLib - Instruments", layout="wide")

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

st.title("🎸 Financial Instruments")

# ===================================================
# 📚 TABLE OF CONTENTS
# ===================================================

st.markdown("## 📚 Table of Contents")

st.markdown("""
<div style="line-height:2; font-size:16px;">
🔹 <a href="#fixedincome" target="_self">1. Fixed Income (Forwards, Bonds, Swaps)</a><br>
🔹 <a href="#inflation" target="_self">2. Inflation Instruments</a><br>
🔹 <a href="#credit" target="_self">3. Credit Instruments</a><br>
🔹 <a href="#options" target="_self">4. Options (Vanilla & Exotics)</a><br>
</div>
""", unsafe_allow_html=True)

# ===================================================
# 🏦 1. FIXED INCOME
# ===================================================

st.markdown("---")
st.markdown('## <span id="fixedincome">🏦 1. Fixed Income</span>', unsafe_allow_html=True)

st.markdown("""
QuantLib provides a robust framework for interest-rate-sensitive products. From simple Forward Rate Agreements to complex Callable Bonds and Multi-leg Swaps.
""")

col_fi1, col_fi2 = st.columns(2)

with col_fi1:
    st.markdown("### ⏩ Forwards & FRAs")
    st.markdown("Lock in a rate or a bond price for a future date.")
    st.code("""
# Forward Rate Agreement
fra = ql.ForwardRateAgreement(
    valueDate, maturityDate, position, 
    strike, notional, iborIndex, yts
)

# Bond Forward
fwd = ql.FixedRateBondForward(
    vDate, mDate, pos, strike, 
    settleDays, dc, cal, bdc, bond, yts
)
""")

with col_fi2:
    st.markdown("### 🏛️ Bond Classes")
    st.markdown("QuantLib's bond system calculates flows automatically.")
    st.code("""
# Fixed Rate Bond
bond = ql.FixedRateBond(
    settlementDays, faceAmount, 
    schedule, [coupon], dayCounter
)

# Zero Coupon Bond
z_bond = ql.ZeroCouponBond(
    settlementDays, calendar, 
    faceAmount, maturityDate
)
""")

# ---------------------------------------------------
# 🎮 INTERACTIVE: BOND ANALYZER
# ---------------------------------------------------
st.markdown("#### 🎮 Interactive Bond Analyzer")

col_ba1, col_ba2 = st.columns([1, 2])

with col_ba1:
    b_face = st.number_input("Face Amount", value=100.0, key="b_face")
    b_coupon = st.slider("Coupon Rate (%)", 0.0, 15.0, 5.0, key="b_coupon") / 100.0
    b_tenor = st.selectbox("Tenor", ["1Y", "5Y", "10Y", "30Y"], index=1, key="b_tenor")
    b_yc = st.slider("Market Yield (%)", 0.0, 15.0, 4.0, key="b_yc") / 100.0
    
    # Setup Dates
    today = ql.Date.todaysDate()
    maturity = today + ql.Period(b_tenor)
    schedule = ql.MakeSchedule(today, maturity, ql.Period("1Y"))
    
    # Corrected constructor: (settlementDays, faceAmount, schedule, coupons, dayCounter)
    try:
        bond = ql.FixedRateBond(
            2,                 # settlementDays
            float(b_face),     # faceAmount
            schedule,          # schedule
            [float(b_coupon)], # coupons
            ql.Actual360()     # accrualDayCounter
        )
        
        # Setup Yield Curve (Flat) for pricing
        crv = ql.FlatForward(2, ql.TARGET(), b_yc, ql.Actual360())
    except Exception as e:
        st.error(f"Constructor Error: {e}")
        bond = None

with col_ba2:
    if bond:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 📊 Bond Metrics")
        
        c1, c2 = st.columns(2)
        with c1:
            clean_price = ql.BondFunctions.cleanPrice(bond, crv)
            dirty_price = ql.BondFunctions.dirtyPrice(bond, crv)
            st.metric("Clean Price", f"{clean_price:.2f}")
            st.metric("Dirty Price", f"{dirty_price:.2f}")
            
        with c2:
            bps = ql.BondFunctions.bps(bond, crv)
            dur = ql.BondFunctions.duration(bond, ql.InterestRate(b_yc, ql.Actual360(), ql.Compounded, ql.Annual))
            st.metric("BPS (PV01)", f"{bps:.4f}")
            st.metric("Mod. Duration", f"{dur:.2f}")
            
        st.markdown('</div>', unsafe_allow_html=True)
        st.info(f"📅 **Maturity:** {ql.BondFunctions.maturityDate(bond)}")

st.markdown("---")

# ---------------------------------------------------
# 🔁 Section: Swaps
# ---------------------------------------------------
st.markdown("### 🔁 Swaps & Swaptions")

col_sw1, col_sw2 = st.columns(2)

with col_sw1:
    st.markdown("#### Vanilla Swap")
    st.code("""
swap = ql.VanillaSwap(
    ql.VanillaSwap.Payer, nominal,
    fixedSchedule, fixedRate, fixedDC,
    floatSchedule, iborIndex, spread, floatDC
)
""")

with col_sw2:
    st.markdown("#### Swaptions")
    st.code("""
# Exercise
exercise = ql.EuropeanExercise(date)
# Swaption Wrapper
swaption = ql.Swaption(
    vanilla_swap, exercise,
    ql.Settlement.Physical
)
""")

# 🎮 INTERACTIVE: SWAP BUILDER
st.markdown("#### 🎮 Interactive Swap Builder")

s_col1, s_col2 = st.columns(2)

with s_col1:
    s_nominal = st.number_input("Notional", value=1e6, step=1e5, key="s_nom")
    s_fix_rate = st.slider("Fixed Rate (%)", 0.0, 10.0, 2.5, step=0.1, key="s_rate") / 100.0
    
with s_col2:
    s_tenor = st.selectbox("Tenor (Years)", [2, 5, 10, 30], index=1, key="s_tenor")
    s_type = st.radio("Type", ["Payer", "Receiver"], horizontal=True, key="s_type")
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.write(f"**Leg 1:** Fixed @ {s_fix_rate:.2%}")
    st.write(f"**Leg 2:** Euribor 6M Floating")
    st.write(f"**Side:** {s_type}")
    st.markdown('</div>', unsafe_allow_html=True)

# ===================================================
# 🎈 2. INFLATION
# ===================================================

st.markdown("---")
st.markdown('## <span id="inflation">🎈 2. Inflation Instruments</span>', unsafe_allow_html=True)

st.markdown("""
Instruments tied to price indexes (CPI, RPI, HICP). These protect against the erosion of purchasing power.
""")

col_inf1, col_inf2 = st.columns(2)

with col_inf1:
    st.markdown("#### 📜 CPI-Linked Bond")
    st.code("""
bond = ql.CPIBond(
    settleDays, nominal, growthOnly, 
    baseCPI, lag, index, 
    interp, schedule, rates, dc, bdc
)
""")

with col_inf2:
    st.markdown("#### 🔁 Zero Coupon Inflation Swap")
    st.code("""
swap = ql.ZeroCouponInflationSwap(
    type, nominal, start, maturity, 
    cal, bdc, dc, fixedRate, 
    z_index, obsLag
)
""")

# ===================================================
# 🛡️ 3. CREDIT
# ===================================================

st.markdown("---")
st.markdown('## <span id="credit">🛡️ 3. Credit Instruments</span>', unsafe_allow_html=True)

st.markdown("""
Default protection using Credit Default Swaps (CDS).
""")

st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown("#### 🛡️ Credit Default Swap (CDS)")
st.code("""
# Side: Protection Seller or Payer
side = ql.Protection.Seller 

cds = ql.CreditDefaultSwap(
    side, nominal, spread, 
    cds_schedule, ql.Following, ql.Actual360()
)

# Option to exercise into a CDS
opt = ql.CdsOption(cds, ql.EuropeanExercise(expiry))
""")
st.markdown('</div>', unsafe_allow_html=True)

# ===================================================
# 🎰 4. OPTIONS
# ===================================================

st.markdown("---")
st.markdown('## <span id="options">🎰 4. Options & Exotics</span>', unsafe_allow_html=True)

st.markdown("""
Derivatives that provide the right, but not the obligation, to trade an underlying asset.
""")

col_o1, col_o2 = st.columns(2)

with col_o1:
    st.markdown("### 🍎 Vanilla Options")
    st.markdown("- **European**: One-time exercise.")
    st.markdown("- **American**: Flexible exercise.")
    st.code("""
payoff = ql.PlainVanillaPayoff(ql.Option.Call, strike)
exercise = ql.EuropeanExercise(maturity)
option = ql.VanillaOption(payoff, exercise)
""")

with col_o2:
    st.markdown("### 🧬 Exotic Library")
    st.markdown("- **Barrier**: Knock-in / Knock-out.")
    st.markdown("- **Asian**: Average-based payoff.")
    st.code("""
# Barrier Example
barrierOpt = ql.BarrierOption(
    ql.Barrier.UpOut, barrier, 
    rebate, payoff, exercise
)
""")

# 🎮 INTERACTIVE: OPTION PRICER
st.markdown("#### 🎮 Interactive Option Pricer")

o_col1, o_col2 = st.columns([1, 2])

with o_col1:
    o_spot = st.number_input("Underlying Spot", value=100.0, key="o_spot")
    o_strike = st.number_input("Strike Price", value=100.0, key="o_strike")
    o_vol = st.slider("Volatility (%)", 5, 80, 20, key="o_vol") / 100.0
    o_rate = st.slider("Risk-free Rate (%)", 0.0, 10.0, 3.0, key="o_rate") / 100.0

with o_col2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("#### 💵 Configuration Preview")
    st.write(f"**Strike/Spot:** {o_strike} / {o_spot}")
    st.write(f"**Vol/Rate:** {o_vol:.0%} / {o_rate:.2%}")
    st.write("---")
    st.write("🔧 *Pricing requires linking to a Black-Scholes process.*")
    st.code("""
process = ql.BlackScholesProcess(spot_h, curve_h, vol_h)
engine = ql.AnalyticEuropeanEngine(process)
option.setPricingEngine(engine)
    """)
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
    if st.button("⬅️ Previous: Indexes"):
        st.switch_page("pages/05_Indexes.py")

with nav_col4:
    if st.button("➡️ Next: Math Tools"):
        st.switch_page("pages/07_Math_Tools.py")
