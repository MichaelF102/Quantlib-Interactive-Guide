import streamlit as st
import QuantLib as ql
import pandas as pd
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
st.title("💸 CashFlows, Legs & Interest Rates")

# ===================================================
# 📚 TABLE OF CONTENTS
# ===================================================

st.markdown("## 📚 Table of Contents")

st.markdown("""
<div style="line-height:2; font-size:16px;">
🔹 <a href="#interest" target="_self">Interest Rates</a><br>
🔹 <a href="#cashflows" target="_self">CashFlows</a><br>
🔹 <a href="#coupons" target="_self">Coupons</a><br>
🔹 <a href="#legs" target="_self">Legs</a><br>
🔹 <a href="#pricers" target="_self">Pricers</a><br >
🔹 <a href="#analytics" target="_self">CashFlow Analytics</a><br>
🔹 <a href="#summary" target="_self">Summary</a><br >
</div>
""", unsafe_allow_html=True)

# ===================================================
# 📈 1. INTEREST RATE
# ===================================================

st.markdown("---")
st.markdown('## <span id="interest">📈 1. InterestRate</span>', unsafe_allow_html=True)

st.markdown("""
### 🧠 What is InterestRate?

Encapsulates **compounding, discounting, and rate conventions**.

👉 Used everywhere in:
- Bond pricing  
- Swap valuation  
- Discounting cashflows  
""")

# ---------------------------------------------------
# 🎮 Interactive Setup
# ---------------------------------------------------

rate_val = st.slider("Interest Rate", 0.0, 0.2, 0.05, key="ir_slider_1")

rate = ql.InterestRate(
    rate_val,
    ql.Actual360(),
    ql.Compounded,
    ql.Annual
)

st.success(f"Rate: {rate.rate():.4f}")

# ---------------------------------------------------
# 📅 Dates
# ---------------------------------------------------

d1 = ql.Date(15,6,2020)
d2 = ql.Date(15,6,2021)

# ---------------------------------------------------
# 📊 Core Outputs
# ---------------------------------------------------

st.markdown("### 📊 Core Calculations")

col1, col2 = st.columns(2)

with col1:
    st.write("📉 Discount Factor:", rate.discountFactor(d1, d2))
    st.write("📈 Compound Factor:", rate.compoundFactor(d1, d2))

with col2:
    st.write("📅 Day Counter:", rate.dayCounter())
    st.write("⚙️ Compounding:", rate.compounding())
    st.write("🔁 Frequency:", rate.frequency())

# ---------------------------------------------------
# 🔄 Equivalent Rate
# ---------------------------------------------------

st.markdown("### 🔄 Equivalent Rate")

eq_rate = rate.equivalentRate(
    ql.Actual360(),
    ql.Compounded,
    ql.Semiannual,
    d1,
    d2
)

st.success(f"Equivalent Rate (Semiannual): {eq_rate.rate():.4f}")

# ---------------------------------------------------
# 🔁 Implied Rate
# ---------------------------------------------------

st.markdown("### 🔁 Implied Rate")

factor = rate.compoundFactor(d1, d2)

implied = rate.impliedRate(
    factor,
    ql.Actual360(),
    ql.Continuous,
    ql.Annual,
    d1,
    d2
)

st.success(f"Implied Rate (Continuous): {implied.rate():.4f}")

# ---------------------------------------------------
# 💻 Code Equivalent
# ---------------------------------------------------

st.markdown("#### 💻 Code Equivalent")

st.code("""
rate = ql.InterestRate(0.05, ql.Actual360(), ql.Compounded, ql.Annual)

# Basic info
rate.rate()
rate.dayCounter()
rate.compounding()
rate.frequency()

# Discounting
rate.discountFactor(d1, d2)
rate.compoundFactor(d1, d2)

# Equivalent rate
rate.equivalentRate(ql.Actual360(), ql.Compounded, ql.Semiannual, d1, d2)

# Implied rate
factor = rate.compoundFactor(d1, d2)
rate.impliedRate(factor, ql.Actual360(), ql.Continuous, ql.Annual, d1, d2)
""")

# ---------------------------------------------------
# 🧠 Deep Insight
# ---------------------------------------------------

st.info("""
💡 **Quant Insight**

InterestRate is not just a number — it defines:

- How time is measured (day count)
- How interest grows (compounding)
- How payments are spaced (frequency)

👉 Changing compounding or frequency can significantly change valuation.
""")
# ===================================================
# 💰 2. CASHFLOWS
# ===================================================

st.markdown("---")
st.markdown('## <span id="cashflows">💰 2. CashFlows</span>', unsafe_allow_html=True)

st.markdown("### 🧠 What are CashFlows?")

st.markdown("""
CashFlows represent **payments over time**.

👉 A single number is meaningless unless tied to:
- Time period
- Interest calculation
- Type of payment
""")

# ---------------------------------------------------
# 📅 Date Selection
# ---------------------------------------------------

st.markdown("### 📅 Select Period")

col1, col2 = st.columns(2)

with col1:
    start_year = st.slider("Start Year", 2020, 2030, 2024, key="start_year_1")
with col2:
    end_year = st.slider("End Year", 2025, 2040, 2030, key="end_year_1")

start = ql.Date(15, 6, start_year)
end = ql.Date(15, 6, end_year)

# ---------------------------------------------------
# 💰 Inputs
# ---------------------------------------------------

st.markdown("### 💰 Inputs")

nominal = st.slider("Principal (Nominal)", 100, 1000, 100, key="nominal_1")
rate_valo = st.slider("Interest Rate", 0.0, 0.2, 0.05, key="ir_slider_2")

day_count = ql.Actual360()

# ---------------------------------------------------
# 📊 Interest Calculation
# ---------------------------------------------------

year_fraction = day_count.yearFraction(start, end)
interest = nominal * rate_valo * year_fraction

# ---------------------------------------------------
# 💰 CashFlow Types
# ---------------------------------------------------

st.markdown("### 💰 CashFlow Types")

simple_cf = ql.SimpleCashFlow(nominal + interest, end)
redemption = ql.Redemption(nominal, end)
amort = ql.AmortizingPayment(nominal / 2, end)  # partial repayment example


st.markdown("#### 📌 SimpleCashFlow")
st.success(f"{simple_cf.amount():.2f}")
st.caption("Principal + Interest")


st.markdown("#### 🏦 Redemption")
st.success(f"{redemption.amount():.2f}")
st.caption("Only principal repayment")


st.markdown("#### 📉 AmortizingPayment")
st.success(f"{amort.amount():.2f}")
st.caption("Partial principal repayment")

# ---------------------------------------------------
# 📊 Details
# ---------------------------------------------------

st.markdown("### 📊 CashFlow Breakdown")

st.write("📅 Start Date:", start)
st.write("📅 End Date:", end)
st.write("⏳ Year Fraction:", round(year_fraction, 4))
st.write("💰 Interest Earned:", round(interest, 2))

# ---------------------------------------------------
# 💻 Code
# ---------------------------------------------------

st.markdown("#### 💻 Code Equivalent")

st.code("""
start = ql.Date(15,6,2024)
end   = ql.Date(15,6,2030)

year_fraction = ql.Actual360().yearFraction(start, end)

interest = nominal * rate * year_fraction

simple_cf = ql.SimpleCashFlow(nominal + interest, end)
redemption = ql.Redemption(nominal, end)
amort = ql.AmortizingPayment(nominal/2, end)
""")

# ---------------------------------------------------
# 🧠 Insight
# ---------------------------------------------------

st.info("""
💡 **Quant Insight**

Now the differences make sense:

- SimpleCashFlow → full payoff (principal + interest)
- Redemption → only principal
- AmortizingPayment → partial repayment

👉 Real instruments combine these over time.
""")

# ===================================================
# 🎟️ 3. COUPONS
# ===================================================

st.markdown("---")
st.markdown('## <span id="coupons">🎟️ 3. Coupons</span>', unsafe_allow_html=True)

st.markdown("""
### 🧠 What are Coupons?

Coupons are **interest payments over time**.

👉 Types:
- Fixed → constant rate  
- Floating → market-linked  
- Structured → engineered payoffs  
""")

# ===================================================
# 📌 FIXED RATE COUPON
# ===================================================

st.markdown("### 📌 FixedRateCoupon")
st.markdown("👉 Pays fixed interest over a period.")

st.code("""
coupon = ql.FixedRateCoupon(
    paymentDate, nominal, rate, dayCounter, startDate, endDate
)
""")

# ===================================================
# 📈 IBOR COUPON
# ===================================================

st.markdown("### 📈 IborCoupon")
st.markdown("👉 Floating rate coupon based on an index (e.g., Euribor, LIBOR).")

st.code("""
index = ql.Euribor6M()

coupon = ql.IborCoupon(
    paymentDate, nominal, startDate, endDate, fixingDays, index
)
""")

# ===================================================
# 🌙 OVERNIGHT COUPON
# ===================================================

st.markdown("### 🌙 OvernightIndexedCoupon")
st.markdown("👉 Uses daily compounding of overnight rates (OIS products).")

st.code("""
coupon = ql.OvernightIndexedCoupon(
    paymentDate, nominal, startDate, endDate, overnightIndex
)
""")

# ===================================================
# 🔒 CAPPED / FLOORED COUPON
# ===================================================

st.markdown("### 🔒 CappedFlooredCoupon")
st.markdown("👉 Limits floating rate between a cap and floor.")

st.code("""
capped = ql.CappedFlooredCoupon(
    floatingCoupon,
    cap=0.06,
    floor=0.02
)
""")

# ===================================================
# 🔁 CMS COUPON
# ===================================================

st.markdown("### 🔁 CmsCoupon")
st.markdown("👉 Based on swap rates (Constant Maturity Swap).")

st.code("""
swapIndex = ql.EuriborSwapIsdaFixA(ql.Period("2Y"))

cms = ql.CmsCoupon(
    paymentDate, nominal, startDate, endDate, fixingDays, swapIndex
)
""")

# ===================================================
# 🔒 CAPPED CMS COUPON
# ===================================================

st.markdown("### 🔒 CappedFlooredCmsCoupon")
st.markdown("👉 CMS coupon with cap/floor applied.")

st.code("""
cms = ql.CmsCoupon(...)
capped = ql.CappedFlooredCmsCoupon(
    paymentDate, nominal, startDate, endDate, fixingDays, swapIndex, rate, spread
)
""")

# ===================================================
# 📊 CMS SPREAD COUPON
# ===================================================

st.markdown("### 📊 CmsSpreadCoupon")
st.markdown("👉 Based on spread between two swap rates (e.g., 10Y - 2Y).")

st.code("""
swapIndex1 = ql.EuriborSwapIsdaFixA(ql.Period("10Y"))
swapIndex2 = ql.EuriborSwapIsdaFixA(ql.Period("2Y"))

spreadIndex = ql.SwapSpreadIndex("CMS 10Y-2Y", swapIndex1, swapIndex2)

coupon = ql.CmsSpreadCoupon(
    paymentDate, nominal, startDate, endDate, fixingDays, spreadIndex
)
""")

# ===================================================
# 🔒 CAPPED CMS SPREAD COUPON
# ===================================================

st.markdown("### 🔒 CappedFlooredCmsSpreadCoupon")
st.markdown("👉 CMS spread with cap/floor and adjustments.")

st.code("""
coupon = ql.CappedFlooredCmsSpreadCoupon(
    paymentDate,
    nominal,
    startDate,
    endDate,
    fixingDays,
    spreadIndex,
    gearing=1,
    spread=0,
    cap=0.05,
    floor=0.01
)
""")


st.markdown("---")
st.markdown("## 🎟️ Coupon Simulator")

st.markdown("""
Interactively explore different coupon types and see how payments are calculated.
""")

# ---------------------------------------------------
# 📌 Select Coupon Type
# ---------------------------------------------------

coupon_type = st.selectbox(
    "Select Coupon Type",
    [
        "FixedRateCoupon",
        "IborCoupon (Floating)",
        "OvernightIndexedCoupon",
        "Capped/Floored Coupon"
    ]
)

# ---------------------------------------------------
# 📅 Dates
# ---------------------------------------------------

col1, col2 = st.columns(2)

with col1:
    start_year = st.slider("Start Year", 2020, 2030, 2024, key="start_year_2")
with col2:
    end_year = st.slider("End Year", 2025, 2040, 2025, key="end_year_2")

start = ql.Date(15, 6, start_year)
end = ql.Date(15, 6, end_year)

# ---------------------------------------------------
# 💰 Inputs
# ---------------------------------------------------

nominal = st.slider("Nominal", 100, 1000, 100, key="nominal_2")
rate_val = st.slider("Rate", 0.0, 0.2, 0.05, key="rate_val_sim")

day_counter = ql.Actual360()
year_fraction = day_counter.yearFraction(start, end)

st.markdown(f"⏳ Year Fraction: **{year_fraction:.4f}**")

# ---------------------------------------------------
# 🎯 COUPON LOGIC
# ---------------------------------------------------

st.markdown("### 💰 Coupon Result")

if coupon_type == "FixedRateCoupon":

    coupon = ql.FixedRateCoupon(
        end, nominal, rate_val, day_counter, start, end
    )

    st.success(f"Fixed Coupon: {coupon.amount():.2f}")
    st.caption("Formula: Nominal × Rate × Time")

elif coupon_type == "IborCoupon (Floating)":

    st.info("Uses market index (e.g., Euribor). No fixing → simulated.")

    simulated_rate = rate_val + 0.01  # fake market shift

    amount = nominal * simulated_rate * year_fraction

    st.success(f"Floating Coupon (Simulated): {amount:.2f}")
    st.caption("Formula: Nominal × Market Rate × Time")

elif coupon_type == "OvernightIndexedCoupon":

    st.info("Uses daily compounding of overnight rates.")

    compounded_rate = (1 + rate_val / 360) ** (360 * year_fraction) - 1
    amount = nominal * compounded_rate

    st.success(f"Overnight Coupon: {amount:.2f}")

elif coupon_type == "Capped/Floored Coupon":

    cap = st.slider("Cap", 0.0, 0.2, 0.08, key="cap_slider")
    floor = st.slider("Floor", 0.0, 0.2, 0.02, key="floor_slider")

    effective_rate = max(min(rate_val, cap), floor)

    amount = nominal * effective_rate * year_fraction

    st.success(f"Capped/Floored Coupon: {amount:.2f}")
    st.caption(f"Effective Rate: {effective_rate:.4f}")

# ---------------------------------------------------
# 📊 Breakdown
# ---------------------------------------------------

st.markdown("### 📊 Breakdown")

st.write("📅 Start Date:", start)
st.write("📅 End Date:", end)
st.write("💰 Nominal:", nominal)
st.write("📈 Input Rate:", rate_val)

# ---------------------------------------------------
# 🧠 Insight
# ---------------------------------------------------
# ===================================================
# 🧠 FINAL INSIGHT
# ===================================================

st.info("""
💡 **Quant Insight**

All coupons follow the same structure:

Coupon = Nominal × Rate × Time

👉 What changes is **how the rate is determined**:

- Fixed → constant  
- Ibor → market index  
- CMS → swap rates  
- Spread → difference between rates  
- Capped/Floored → risk-controlled  

👉 Complex derivatives are just combinations of these.
""")

# ===================================================
# 🧩 4. LEGS
# ===================================================


st.markdown("---")
st.markdown('## <span id="legs">🧩 4. Legs</span>', unsafe_allow_html=True)

st.markdown("""
### 🧠 What is a Leg?

A **Leg** is a sequence of cashflows.

👉 Used in:
- Bonds → fixed coupons  
- Swaps → fixed vs floating  
- OIS → overnight compounding  

---

### ⚙️ Structure

Leg = [CashFlow₁, CashFlow₂, ..., CashFlowₙ]
""")

# ===================================================
# 🎮 SELECT LEG TYPE
# ===================================================

leg_type = st.selectbox(
    "Select Leg Type",
    ["Manual Leg", "FixedRateLeg", "IborLeg (Floating)", "OvernightLeg"]
)

# ===================================================
# 📅 SCHEDULE
# ===================================================

st.markdown("### 📅 Schedule")

start_year = st.slider("Start Year", 2020, 2030, 2024, key="start_year_leg")
end_year = st.slider("End Year", 2025, 2040, 2026, key="end_year_leg")

freq = st.selectbox("Frequency", ["3M", "6M", "1Y"])

start = ql.Date(15, 6, start_year)
end = ql.Date(15, 6, end_year)

schedule = ql.MakeSchedule(start, end, ql.Period(freq))

# ===================================================
# 💰 INPUTS
# ===================================================

st.markdown("### 💰 Inputs")

nominal = st.slider("Nominal", 100, 1000, 100, key="nominal_leg_4")
rate_val = st.slider("Rate", 0.0, 0.2, 0.05, key="rate_leg")
spread = st.slider("Spread", -0.02, 0.02, 0.0, key="spread_leg")
gearing = st.slider("Gearing", 0.5, 2.0, 1.0, key="gearing_leg")

day_count = ql.Actual360()

# ===================================================
# 🧩 LEG CREATION
# ===================================================

st.markdown("### 🧩 Generated Leg")

leg = []
data = []

# ---------------------------
# 1. Manual Leg
# ---------------------------
if leg_type == "Manual Leg":

    st.info("👉 Manual Leg: user-defined fixed cashflows")

    today = ql.Date().todaysDate()

    cf1 = ql.SimpleCashFlow(5.0, today + 365)
    cf2 = ql.SimpleCashFlow(5.0, today + 365*2)
    cf3 = ql.SimpleCashFlow(105.0, today + 365*3)

    leg = ql.Leg([cf1, cf2, cf3])

    for cf in leg:
        data.append({"Date": cf.date(), "Amount": cf.amount()})

# ---------------------------
# 2. Fixed Rate Leg
# ---------------------------
elif leg_type == "FixedRateLeg":

    st.info("👉 Fixed Leg: pays constant interest each period")

    leg = ql.FixedRateLeg(schedule, day_count, [nominal], [rate_val])

    for cf in leg:
        data.append({
            "Date": cf.date(),
            "Amount": round(cf.amount(), 2)
        })

# ---------------------------
# 3. Ibor Leg (Floating)
# ---------------------------
elif leg_type == "IborLeg (Floating)":

    st.info("👉 Floating Leg: rate depends on market index (simulated here)")

    # simulate floating rate
    simulated_rate = rate_val + spread

    dates = list(schedule)

    for i in range(1, len(dates)):
        yf = day_count.yearFraction(dates[i-1], dates[i])
        amount = nominal * simulated_rate * yf * gearing

        data.append({
            "Date": dates[i],
            "Amount": round(amount, 2)
        })

# ---------------------------
# 4. Overnight Leg
# ---------------------------
elif leg_type == "OvernightLeg":

    st.info("👉 Overnight Leg: daily compounding (simulated)")

    dates = list(schedule)

    for i in range(1, len(dates)):
        yf = day_count.yearFraction(dates[i-1], dates[i])

        # approximate compounding
        compounded = (1 + rate_val/360)**(360*yf) - 1
        amount = nominal * compounded * gearing

        data.append({
            "Date": dates[i],
            "Amount": round(amount, 2)
        })

# ===================================================
# 📊 DISPLAY
# ===================================================

df = pd.DataFrame(data)

st.markdown("### 📊 CashFlow Table")
st.dataframe(df, use_container_width=True)

# ===================================================
# 📈 VISUALIZATION
# ===================================================

if len(df) > 0:
    st.markdown("### 📈 CashFlow Timeline")
    st.line_chart(df.set_index("Date")["Amount"])

# ===================================================
# 📊 SUMMARY
# ===================================================

st.markdown("### 📊 Summary")

total = df["Amount"].sum() if len(df) > 0 else 0

col1, col2 = st.columns(2)

with col1:
    st.metric("Number of Cashflows", len(df))
with col2:
    st.metric("Total Cashflow", f"{total:.2f}")

# ===================================================
# 💻 CODE
# ===================================================

st.markdown("#### 💻 Code Equivalent")

st.code("""
# Fixed Leg
ql.FixedRateLeg(schedule, dayCount, [nominal], [rate])

# Floating Leg (needs index fixings in real use)
ql.IborLeg([nominal], schedule, index)

# Overnight Leg (needs curve)
ql.OvernightLeg([nominal], schedule, overnightIndex)
""")

# ===================================================
# 🧠 INSIGHT
# ===================================================

st.info("""
💡 **Quant Insight**

Why we simulated floating legs:

- Real QuantLib needs market data (fixings + curves)
- Without them → values = 0 ❌

👉 So we approximate to build intuition

---

Real systems:
Quote → Index → Curve → Leg → Pricing Engine
""")

st.markdown("---")
st.markdown('## <span id="pricers">📊 5. Pricers</span>', unsafe_allow_html=True)
st.markdown("""
### 🧠 What are Pricers?

Pricers compute the **value of cashflows or coupons**.

👉 They define *how* a payment is valued given:
- Volatility
- Interest rates
- Model assumptions

---

### ⚙️ Pipeline

Coupon → Pricer → Model → NPV
""")

# ===================================================
# 🎮 SELECT PRICER
# ===================================================

pricer_type = st.selectbox(
    "Select Pricer",
    [
        "BlackIborCouponPricer",
        "LinearTsrPricer (CMS)",
        "Hagan Pricers (Concept)"
    ]
)

# ===================================================
# 📅 COMMON SETUP
# ===================================================

st.markdown("### 📅 Setup")

rate_val = st.slider("Interest Rate", -0.05, 0.1, 0.02, key="ir_slider_pricer")
volatility = st.slider("Volatility", 0.01, 0.5, 0.10, key="vol_pricer")

nominal = 100

# Yield curve
crv = ql.FlatForward(0, ql.TARGET(), rate_val, ql.Actual360())
yts = ql.YieldTermStructureHandle(crv)

schedule = ql.MakeSchedule(
    ql.Date(15,6,2021),
    ql.Date(15,6,2024),
    ql.Period('6M')
)

# ===================================================
# 1. BLACK IBOR PRICER
# ===================================================

if pricer_type == "BlackIborCouponPricer":

    st.markdown("### 📈 BlackIborCouponPricer")

    st.markdown("""
👉 Used for **floating rate coupons with volatility**.

- Based on Black model  
- Requires volatility surface  
- Used in cap/floor pricing  
""")

    # Index with curve
    index = ql.Euribor3M(yts)

    # Build leg
    leg = ql.IborLeg(
        [nominal],
        schedule,
        index,
        ql.Actual360(),
        ql.ModifiedFollowing,
        isInArrears=True
    )

    # Vol structure
    vol = ql.ConstantOptionletVolatility(
        2,
        ql.TARGET(),
        ql.Following,
        volatility,
        ql.Actual360()
    )

    pricer = ql.BlackIborCouponPricer(
        ql.OptionletVolatilityStructureHandle(vol)
    )

    ql.setCouponPricer(leg, pricer)

    npv = ql.CashFlows.npv(leg, yts, True)

    st.success(f"💰 Leg NPV: {npv:.2f}")

    st.code("""
vol = ql.ConstantOptionletVolatility(...)
pricer = ql.BlackIborCouponPricer(handle)

ql.setCouponPricer(leg, pricer)
npv = ql.CashFlows.npv(leg, yts, True)
""")

# ===================================================
# 2. LINEAR TSR PRICER (CMS)
# ===================================================

elif pricer_type == "LinearTsrPricer (CMS)":

    st.markdown("### 🔁 LinearTsrPricer")

    st.markdown("""
👉 Used for **CMS (Constant Maturity Swap) coupons**

- Depends on swaption volatility  
- Used in structured products  
""")

    volQuote = ql.QuoteHandle(ql.SimpleQuote(volatility))

    swaptionVol = ql.ConstantSwaptionVolatility(
        0,
        ql.TARGET(),
        ql.ModifiedFollowing,
        volQuote,
        ql.Actual365Fixed()
    )

    swvol_handle = ql.SwaptionVolatilityStructureHandle(swaptionVol)

    mean_reversion = ql.QuoteHandle(ql.SimpleQuote(0.01))

    cms_pricer = ql.LinearTsrPricer(swvol_handle, mean_reversion)

    st.success("CMS Pricer created successfully")

    st.code("""
cms_pricer = ql.LinearTsrPricer(
    swaptionVolatilityStructure,
    meanReversion
)
""")

# ===================================================
# 3. HAGAN PRICERS (CONCEPT)
# ===================================================

elif pricer_type == "Hagan Pricers (Concept)":

    st.markdown("### 🧪 Hagan Pricers")

    st.markdown("""
👉 Advanced models for CMS pricing:

- **AnalyticHaganPricer** → fast, closed-form  
- **NumericHaganPricer** → more accurate  
- **LognormalCmsSpreadPricer** → spread-based  

---

### ⚠️ Note

These require:
- Full market data
- Calibration
- Vol surfaces

👉 Not directly usable without full setup
""")

    st.warning("⚠️ These pricers need advanced market setup")

    st.code("""
ql.AnalyticHaganPricer(...)
ql.NumericHaganPricer(...)
ql.LognormalCmsSpreadPricer(...)
""")

# ===================================================
# 🧠 INSIGHT
# ===================================================

st.info("""
💡 **Quant Insight**

Pricers define the *mathematics* of valuation:

- Black → lognormal assumption  
- TSR → interest rate models  
- Hagan → advanced CMS modeling  

👉 Same cashflow + different pricer = different price
""")

# ===================================================
# 📊 5. ANALYTICS
# ===================================================



st.markdown("---")
st.markdown('## <span id="analytics">📊 6. CashFlow Analytics</span>', unsafe_allow_html=True)

st.markdown("""
### 🧠 What can we compute?

- NPV  
- BPS (sensitivity)  
- Duration (Simple, Macaulay, Modified)  
- Convexity  
- Yield (IRR)  
- Z-Spread  
""")

# ===================================================
# 📅 SETUP LEG (ENSURE NON-ZERO VALUES)
# ===================================================

start = ql.Date(15,6,2024)
end = ql.Date(15,6,2028)

schedule = ql.MakeSchedule(start, end, ql.Period('6M'))

nominal = st.slider("Nominal", 100, 1000, 100, key="nominal_analytics_5")
rate_val = st.slider("Coupon Rate", 0.0, 0.2, 0.05, key="coupon_rate_analytics")

day_count = ql.Actual360()

leg = ql.FixedRateLeg(schedule, day_count, [nominal], [rate_val])

# ===================================================
# 📈 YIELD CURVE
# ===================================================

curve_rate = st.slider("Discount Rate", 0.0, 0.1, 0.05, key="discount_rate_analytics")

curve = ql.FlatForward(0, ql.TARGET(), curve_rate, ql.Actual360())
yts = ql.YieldTermStructureHandle(curve)

rate = ql.InterestRate(curve_rate, ql.Actual360(), ql.Compounded, ql.Annual)

# ===================================================
# 📅 DATE INSPECTORS
# ===================================================

st.markdown("### 📅 Date Inspectors")

st.write("Start Date:", ql.CashFlows.startDate(leg))
st.write("Maturity Date:", ql.CashFlows.maturityDate(leg))

# ===================================================
# 🔍 CASHFLOW INSPECTORS
# ===================================================

st.markdown("### 🔍 CashFlow Inspectors")

st.write("Previous CF:", ql.CashFlows.previousCashFlowDate(leg, True))
st.write("Next CF:", ql.CashFlows.nextCashFlowDate(leg, True))

# ===================================================
# 💰 NPV
# ===================================================

st.markdown("### 💰 NPV")

npv = ql.CashFlows.npv(leg, yts, True)
st.success(f"NPV: {npv:.2f}")

# ===================================================
# 📊 BPS
# ===================================================

st.markdown("### 📊 BPS (Sensitivity)")

bps = ql.CashFlows.bps(leg, yts, True)
st.success(f"BPS: {bps:.4f}")

# ===================================================
# 🎯 ATM RATE
# ===================================================

st.markdown("### 🎯 ATM Rate")

atm = ql.CashFlows.atmRate(leg, curve, True)
st.success(f"ATM Rate: {atm:.4f}")

# ===================================================
# ⏳ DURATION
# ===================================================

st.markdown("### ⏳ Duration")

simple_dur = ql.CashFlows.duration(leg, rate, ql.Duration.Simple, False)
mac_dur = ql.CashFlows.duration(leg, rate, ql.Duration.Macaulay, False)
mod_dur = ql.CashFlows.duration(leg, rate, ql.Duration.Modified, False)

col1, col2, col3 = st.columns(3)

col1.metric("Simple", f"{simple_dur:.4f}")
col2.metric("Macaulay", f"{mac_dur:.4f}")
col3.metric("Modified", f"{mod_dur:.4f}")

# ===================================================
# 📈 CONVEXITY
# ===================================================

st.markdown("### 📈 Convexity")

conv = ql.CashFlows.convexity(leg, rate, False)
st.success(f"Convexity: {conv:.4f}")

# ===================================================
# 💸 YIELD / IRR
# ===================================================

st.markdown("### 💸 Yield (IRR)")

try:
    irr = ql.CashFlows.yieldRate(
        leg,
        npv,
        ql.Actual360(),
        ql.Compounded,
        ql.Annual,
        True
    )
    st.success(f"Yield: {irr:.4f}")
except:
    st.warning("Yield calculation failed (try different inputs)")

# ===================================================
# 📉 Z-SPREAD
# ===================================================

st.markdown("### 📉 Z-Spread")

try:
    z = ql.CashFlows.zSpread(
        leg,
        npv,
        curve,
        ql.Actual360(),
        ql.Compounded,
        ql.Annual,
        True
    )
    st.success(f"Z-Spread: {z:.6f}")
except:
    st.warning("Z-spread calculation failed")

# ===================================================
# 📊 CASHFLOW TABLE
# ===================================================

st.markdown("### 📊 CashFlow Table")

data = []

for cf in leg:
    data.append({
        "Date": cf.date(),
        "Amount": round(cf.amount(), 2)
    })

df = pd.DataFrame(data)
st.dataframe(df, use_container_width=True)

# ===================================================
# 📈 VISUALIZATION
# ===================================================

st.markdown("### 📈 CashFlow Timeline")
st.line_chart(df.set_index("Date")["Amount"])

# ===================================================
# 🧠 INSIGHT
# ===================================================

st.info("""
💡 **Quant Insight**

CashFlow Analytics = Risk + Pricing:

- NPV → value  
- BPS → sensitivity  
- Duration → rate risk  
- Convexity → curvature risk  
- Yield → return  
- Z-spread → credit risk  

👉 This is exactly what fixed-income desks compute daily.
""")

# ===================================================
# 🧠 FINAL INSIGHT
# ===================================================

st.info("""
💡 **Quant Insight**

Everything reduces to cashflows:

Leg → CashFlows → Discounting → NPV

👉 Bonds, swaps, and derivatives are just structured cashflow streams.
""")

st.markdown("---")
st.markdown('## <span id="summary">📈 7. Summary</span>', unsafe_allow_html=True)

st.markdown("""

👉 This section gives you **quick recall of all core concepts**.
""")

# ===================================================
# 📌 1. INTEREST RATE
# ===================================================

# ===================================================
# 📈 1. INTEREST RATE
# ===================================================

st.markdown("### 📈 InterestRate")

st.markdown("""
👉 Defines how interest grows over time (compounding + conventions)
""")

st.code("""
# Setup
d1 = ql.Date(15,6,2020)
d2 = ql.Date(15,6,2021)

rate = ql.InterestRate(
    0.05,
    ql.Actual360(),
    ql.Compounded,
    ql.Annual
)

# Discounting / Compounding
rate.discountFactor(d1, d2)
rate.compoundFactor(d1, d2)

# Equivalent rate (change compounding/frequency)
rate.equivalentRate(
    ql.Actual360(),
    ql.Compounded,
    ql.Semiannual,
    d1,
    d2
)

# Implied rate from factor
factor = rate.compoundFactor(d1, d2)

rate.impliedRate(
    factor,
    ql.Actual360(),
    ql.Continuous,
    ql.Annual,
    d1,
    d2
)
""")

# ===================================================
# 💰 2. CASHFLOWS
# ===================================================

st.markdown("### 💰 CashFlows")

st.markdown("""
👉 Individual payments at specific dates
""")

st.code("""
date = ql.Date(15,6,2025)

# Full payment (principal + interest)
ql.SimpleCashFlow(105, date)

# Principal repayment
ql.Redemption(100, date)

# Partial repayment
ql.AmortizingPayment(50, date)
""")

# ===================================================
# 🎟️ 3. COUPONS
# ===================================================

st.markdown("### 🎟️ Coupons")

st.markdown("""
👉 Interest-generating cashflows
""")

st.code("""
start = ql.Date(15,12,2024)
end   = ql.Date(15,6,2025)

# Fixed coupon
ql.FixedRateCoupon(
    end, 100, 0.05, ql.Actual360(), start, end
)

# Floating coupon (Ibor)
index = ql.Euribor6M()
ql.IborCoupon(end, 100, start, end, 2, index)

# Overnight coupon
ql.OvernightIndexedCoupon(
    end, 100, start, end, ql.Eonia()
)

# Capped/Floored
floating = ql.IborCoupon(end, 100, start, end, 2, index)
ql.CappedFlooredCoupon(floating, cap=0.06, floor=0.02)

# CMS coupon
swapIndex = ql.EuriborSwapIsdaFixA(ql.Period("2Y"))
ql.CmsCoupon(end, 100, start, end, 2, swapIndex)

# CMS Spread coupon
swapIndex1 = ql.EuriborSwapIsdaFixA(ql.Period("10Y"))
swapIndex2 = ql.EuriborSwapIsdaFixA(ql.Period("2Y"))
spreadIndex = ql.SwapSpreadIndex("CMS 10Y-2Y", swapIndex1, swapIndex2)

ql.CmsSpreadCoupon(end, 100, start, end, 2, spreadIndex)
""")

# ===================================================
# 🧩 4. LEGS
# ===================================================

st.markdown("### 🧩 Legs")

st.markdown("""
👉 Collection of cashflows (building blocks of instruments)
""")

st.code("""
schedule = ql.MakeSchedule(
    ql.Date(15,6,2024),
    ql.Date(15,6,2026),
    ql.Period("6M")
)

# Manual leg
cf1 = ql.SimpleCashFlow(5, ql.Date(15,6,2025))
cf2 = ql.SimpleCashFlow(105, ql.Date(15,6,2026))
ql.Leg([cf1, cf2])

# Fixed leg
ql.FixedRateLeg(schedule, ql.Actual360(), [100], [0.05])

# Floating leg
index = ql.Euribor3M()
ql.IborLeg([100], schedule, index)

# Overnight leg
ql.OvernightLeg([100], schedule, ql.Eonia())
""")

# ===================================================
# ⚙️ 5. PRICERS
# ===================================================

st.markdown("### ⚙️ Pricers")

st.markdown("""
👉 Define how cashflows are valued
""")

st.code("""
# Yield curve
curve = ql.FlatForward(0, ql.TARGET(), 0.02, ql.Actual360())
yts = ql.YieldTermStructureHandle(curve)

# Floating leg
index = ql.Euribor3M(yts)

schedule = ql.MakeSchedule(
    ql.Date(15,6,2021),
    ql.Date(15,6,2024),
    ql.Period("6M")
)

leg = ql.IborLeg([100], schedule, index)

# Black pricer
vol = ql.ConstantOptionletVolatility(
    2, ql.TARGET(), ql.Following, 0.10, ql.Actual360()
)

pricer = ql.BlackIborCouponPricer(
    ql.OptionletVolatilityStructureHandle(vol)
)

ql.setCouponPricer(leg, pricer)

# NPV
ql.CashFlows.npv(leg, yts, True)

# CMS pricer
swaptionVol = ql.ConstantSwaptionVolatility(
    0, ql.TARGET(), ql.ModifiedFollowing,
    ql.QuoteHandle(ql.SimpleQuote(0.2)),
    ql.Actual365Fixed()
)

ql.LinearTsrPricer(
    ql.SwaptionVolatilityStructureHandle(swaptionVol),
    ql.QuoteHandle(ql.SimpleQuote(0.01))
)
""")

# ===================================================
# 📊 6. ANALYTICS
# ===================================================

st.markdown("### 📊 CashFlow Analytics")

st.markdown("""
👉 Risk + valuation metrics
""")

st.code("""
# Curve
curve = ql.FlatForward(0, ql.TARGET(), 0.05, ql.Actual360())
yts = ql.YieldTermStructureHandle(curve)

rate = ql.InterestRate(0.05, ql.Actual360(), ql.Compounded, ql.Annual)

# NPV & sensitivity
ql.CashFlows.npv(leg, yts, True)
ql.CashFlows.bps(leg, yts, True)

# Duration
ql.CashFlows.duration(leg, rate, ql.Duration.Modified, False)

# Convexity
ql.CashFlows.convexity(leg, rate, False)

# Yield (IRR)
ql.CashFlows.yieldRate(
    leg,
    100,
    ql.Actual360(),
    ql.Compounded,
    ql.Annual,
    True
)

# Z-Spread
ql.CashFlows.zSpread(
    leg,
    100,
    curve,
    ql.Actual360(),
    ql.Compounded,
    ql.Annual,
    True
)
""")

# Navigation Buttons
st.markdown("""
    <style>
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) button {
        margin-left: auto;
        display: block;
    }
    </style>
    """, unsafe_allow_html=True)

nav_col1, nav_col2, nav_col3 , nav_col4 = st.columns([1, 1, 1, 1])
with nav_col1:
    if st.button("⬅️ Previous: Basics"):
        st.switch_page("pages/01_Basics.py")
with nav_col4:
    if st.button("➡️ Next: Currencies"):
        st.switch_page("pages/03_Currencies.py")

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