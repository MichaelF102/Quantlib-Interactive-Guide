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


st.title("📘 Basics in QuantLib")

st.markdown("## 📚 Table of Contents")

st.markdown("""
<div style="line-height:2; font-size:16px;">

🔹 <a href="#evaluation" target="_self">Evaluation Date</a><br>
🔹 <a href="#array" target="_self">Array</a><br>
🔹 <a href="#matrix" target="_self">Matrix</a><br>
🔹 <a href="#observer" target="_self">Observable & Observer</a><br>
🔹 <a href="#quotes" target="_self">Quotes</a><br>
🔹 <a href="#handles" target="_self">Handles</a><br>
🔹 <a href="#summary" target="_self">Summary</a><br>
</div>
""", unsafe_allow_html=True)
# ---------------------------------------------------
# 🧠 1. Evaluation Date (MOST IMPORTANT CONCEPT)
# ---------------------------------------------------

st.markdown("---")

st.markdown('## <span id="evaluation">🗓️ 1. Evaluation Date</span>', unsafe_allow_html=True)


st.markdown("""
### 🧠 Why Evaluation Date Matters

In QuantLib, **every calculation is anchored to a single date** called the **evaluation date**.

👉 It answers the question:  
**“As of what date are we valuing this financial instrument?”**

---

### ⚙️ What it affects

- 📉 **NPV (Net Present Value)**  
- 📊 **Discount factors & yield curves**  
- 📅 **Cashflow timing**  
- 📈 **Forward rates & risk measures**

---

### ⚠️ Important Insight

Changing the evaluation date is like **moving forward or backward in time** —  
all prices and risk metrics will update accordingly.
""")

st.markdown("#### 📥 Set Evaluation Date")

day = st.number_input("Day", 1, 31, 15)
month = st.number_input("Month", 1, 12, 6)
year = st.number_input("Year", 2000, 2035, 2020)

today = ql.Date(day, month, year)
ql.Settings.instance().evaluationDate = today


st.markdown("#### 📤 Current Evaluation Date")
st.success(f"{today}")

# Code snippet
st.markdown("#### 💻 Code Equivalent")
st.code("""
import QuantLib as ql

today = ql.Date(15, 6, 2020)
ql.Settings.instance().evaluationDate = today
""")

# Extra insight box
st.info("""
💡 **Pro Tip:**  
Always set the evaluation date **before** building curves, instruments, or pricing engines.  
Otherwise, results may be inconsistent or incorrect.
""")


# ---------------------------------------------------
# 📊 2. Array
# ---------------------------------------------------

st.markdown("---")

st.markdown('## <span id="array">📊 2. Array</span>', unsafe_allow_html=True)

st.markdown("""
### 🧠 What is a QuantLib Array?

A **QuantLib Array** is a lightweight numerical container used internally for:

- 📐 Numerical methods  
- 📊 Model parameters  
- ⚙️ Optimization & calibration  

It behaves similarly to a Python list or NumPy array, but is optimized for QuantLib's C++ backend.
""")


st.markdown("#### ⚙️ Configure Array")

size = st.slider("Array Size", 1, 10, 5)
value = st.slider("Initial Value", 0.0, 10.0, 1.0)
increment = st.slider("Increment", 0.0, 5.0, 0.5)

# Create base array
arr = ql.Array(size)

# Fill manually
for i in range(size):
    arr[i] = value + i * increment


st.markdown("#### 📤 Generated Array")

st.success(list(arr))

# Code snippet
st.markdown("#### 💻 Code Equivalent")
st.code("""
# Create array with constant values
ql.Array(size, value)

# Create array with increment
ql.Array(size, value, increment)
""")

# Deep insight
st.info("""
💡 **Quant Insight:**  
Arrays are heavily used inside pricing engines and models (e.g., storing grid values in finite difference methods or simulation paths in Monte Carlo).
""")


st.markdown("---")  

st.markdown('## <span id="matrix">📐 3. Matrix</span>', unsafe_allow_html=True)
st.markdown("""
### 🧠 What is a QuantLib Matrix?

A **QuantLib Matrix** is a 2D numerical structure used in:

- 📐 Linear algebra computations  
- 🧮 Finite Difference Methods (PDE grids)  
- ⚙️ Optimization & calibration problems  

👉 It is heavily used behind th e scenes in pricing engines.
""")


st.markdown("#### ⚙️ Configure Matrix")

rows = st.slider("Rows", 1, 6, 3)
cols = st.slider("Columns", 1, 6, 3)
value = st.slider("Initial Value", 0.0, 5.0, 0.5)

matrix = ql.Matrix(rows, cols, value)

# ---------------------------------------------------
# 🎯 Interactive Editing (VERY COOL FEATURE)
# ---------------------------------------------------

st.markdown("#### ✏️ Modify Matrix Values")

for i in range(rows):
    cols_input = st.columns(cols)
    for j in range(cols):
        matrix[i][j] = cols_input[j].number_input(
            f"M[{i},{j}]",
            value=float(matrix[i][j]),
            key=f"{i}-{j}"
        )

updated_matrix = [[matrix[i][j] for j in range(cols)] for i in range(rows)]
st.write("Updated Matrix:")

df = pd.DataFrame(updated_matrix)

st.dataframe(df, use_container_width=True)

# ---------------------------------------------------
# 💻 Code
# ---------------------------------------------------

st.markdown("#### 💻 Code Equivalent Syntax")

st.code("""
# Create matrix
matrix = ql.Matrix(rows, columns, value)

# Access element
matrix[i][j]

# Modify element
matrix[i][j] = new_value
""")

# ---------------------------------------------------
# 🧠 Insight
# ---------------------------------------------------

st.info("""
💡 **Quant Insight**

Matrices are fundamental in QuantLib:

- Finite difference grids for option pricing  
- Covariance matrices in risk models  
- Optimization problems in calibration  

👉 Almost every advanced pricing model relies on matrix computations internally.
""")
# ---------------------------------------------------
# 🔄 4. Observable (Reactive System)
# ---------------------------------------------------

st  .markdown("---")

st.markdown('## <span id="observer">🔄 4. Observable & Observer</span>', unsafe_allow_html=True)
    
st.markdown("""
### 🧠 What is the Observer Pattern?

QuantLib is built on a **reactive architecture**.

👉 When market data changes, all dependent objects are **automatically updated**.

---

### ⚙️ Real-World Analogy

- 📈 Stock price changes  
- 📊 Option price updates automatically  
- ⚡ No manual recalculation needed  

This is how real trading systems work.
""")

# ---------------------------------------------------
# 🎮 Interactive Demo
# ---------------------------------------------------

st.markdown("### 🧪 Interactive Demo")

col1, col2 = st.columns([1, 1])

# shared flag state
if "observer_flag" not in st.session_state:
    st.session_state.observer_flag = 0

def raise_flag():
    st.session_state.observer_flag = 1

# create quote + observer
quote = ql.SimpleQuote(0.0)
observer = ql.Observer(raise_flag)
observer.registerWith(quote)


st.markdown("#### 📥 Update Market Data")

new_value = st.slider("Change Quote Value", 0.0, 10.0, 5.0)

if st.button("Update Quote"):
    st.session_state.observer_flag = 0  # reset
    quote.setValue(new_value)


st.markdown("#### 📤 Observer Status")

if st.session_state.observer_flag:
    st.success("Observer notified of change ✅")
else:
    st.warning("No update detected yet ⏳")

# ---------------------------------------------------
# 🔄 Live Value Display
# ---------------------------------------------------

st.markdown("#### 📊 Current Quote Value")
st.info(f"{quote.value()}")

# ---------------------------------------------------
# 💻 Code Reference
# ---------------------------------------------------

st.markdown("#### 💻 Code Equivalent")
st.code("""
quote = ql.SimpleQuote(0.0)

def callback():
    print("Updated!")

observer = ql.Observer(callback)
observer.registerWith(quote)

quote.setValue(5.0)
""")

# ---------------------------------------------------
# 🧠 Deep Insight
# ---------------------------------------------------

st.info("""
💡 **Quant Insight**

This mechanism powers the entire QuantLib pipeline:

Quote → Handle → Term Structure → Instrument → Pricing Engine

👉 Changing a single input automatically propagates through the system.

This is why QuantLib is extremely efficient for:
- Real-time pricing
- Risk systems
- Portfolio revaluation
""")

# ---------------------------------------------------
# 💰 5. Quotes
# ---------------------------------------------------

st.markdown("---")

st.markdown('## <span id="quotes">💰 5. Quotes</span>', unsafe_allow_html=True)

st.markdown("""
### 🧠 What are Quotes in QuantLib?

A **Quote** represents a single piece of **market data**.

👉 Examples:
- 📈 Stock prices  
- 📉 Interest rates  
- 📊 Volatility  

---

### ⚙️ Why Quotes Matter

Quotes are the **entry point of the pricing pipeline**:

Quote → Handle → Term Structure → Instrument → Engine → Price

👉 Any change propagates automatically.
""")

# ===================================================
# 🧪 1. SimpleQuote
# ===================================================

st.markdown("## 🧪 SimpleQuote")

st.markdown("👉 Basic container for a single market value.")

val = st.slider("SimpleQuote Value", 0.0, 1.0, 0.05)
s = ql.SimpleQuote(val)

st.success(f"Value: {s.value()}")

if st.button("Update to 0.1"):
    s.setValue(0.1)

st.write("Updated Value:", s.value())
st.write("Is Valid:", s.isValid())

st.code("""
s = ql.SimpleQuote(0.01)

s.value()
s.setValue(0.05)
s.isValid()
""")

# ===================================================
# 🧪 2. DerivedQuote
# ===================================================

st.markdown("## 🧪 DerivedQuote")

st.markdown("👉 Quote derived from another quote via a function.")

base_val = st.slider("Base Quote", 0.0, 1.0, 0.06)
d1 = ql.SimpleQuote(base_val)

d2 = ql.DerivedQuote(ql.QuoteHandle(d1), lambda x: 10 * x)

st.write("Base Value:", d1.value())
st.success(f"Derived Value (×10): {d2.value()}")

st.code("""
d1 = ql.SimpleQuote(0.06)
d2 = ql.DerivedQuote(ql.QuoteHandle(d1), lambda x: 10*x)
""")

# ===================================================
# 🧪 3. CompositeQuote
# ===================================================

st.markdown("## 🧪 CompositeQuote")

st.markdown("👉 Combines multiple quotes using a function.")

c1_val = st.slider("Quote 1", 0.0, 1.0, 0.02)
c2_val = st.slider("Quote 2", 0.0, 1.0, 0.03)

c1 = ql.SimpleQuote(c1_val)
c2 = ql.SimpleQuote(c2_val)

c3 = ql.CompositeQuote(
    ql.QuoteHandle(c1),
    ql.QuoteHandle(c2),
    lambda x, y: x + y
)

st.write("Quote 1:", c1.value())
st.write("Quote 2:", c2.value())
st.success(f"Combined (Sum): {c3.value()}")

st.code("""
c1 = ql.SimpleQuote(0.02)
c2 = ql.SimpleQuote(0.03)

c3 = ql.CompositeQuote(
    ql.QuoteHandle(c1),
    ql.QuoteHandle(c2),
    lambda x,y: x+y
)
""")

# ===================================================
# 🧪 4. DeltaVolQuote (ADVANCED)
# ===================================================

st.markdown("## 🧪 DeltaVolQuote (FX Vol Quotes)")

st.markdown("""
👉 Used in FX markets where volatility is quoted by **delta + maturity**.

Example:
- ATM Vol
- 25 Delta Call / Put
""")

vol_atm = st.slider("ATM Vol", 0.01, 0.2, 0.08)
vol_call = st.slider("25Δ Call Vol", 0.01, 0.2, 0.075)
vol_put = st.slider("25Δ Put Vol", 0.01, 0.2, 0.095)

deltaType = ql.DeltaVolQuote.Fwd
atmType = ql.DeltaVolQuote.AtmFwd
maturity = 1.0

atm_quote = ql.DeltaVolQuote(
    ql.QuoteHandle(ql.SimpleQuote(vol_atm)),
    deltaType,
    maturity,
    atmType
)

call_quote = ql.DeltaVolQuote(
    0.25,
    ql.QuoteHandle(ql.SimpleQuote(vol_call)),
    maturity,
    deltaType
)

put_quote = ql.DeltaVolQuote(
    -0.25,
    ql.QuoteHandle(ql.SimpleQuote(vol_put)),
    maturity,
    deltaType
)

st.success(f"ATM Vol: {vol_atm}")
st.success(f"25Δ Call: {vol_call}")
st.success(f"25Δ Put: {vol_put}")

st.code("""
atm = ql.DeltaVolQuote(ql.QuoteHandle(ql.SimpleQuote(vol)), deltaType, maturity, atmType)

call = ql.DeltaVolQuote(0.25, ql.QuoteHandle(ql.SimpleQuote(vol)), maturity, deltaType)
put  = ql.DeltaVolQuote(-0.25, ql.QuoteHandle(ql.SimpleQuote(vol)), maturity, deltaType)
""")

# ===================================================
# 🧠 FINAL INSIGHT
# ===================================================

st.info("""
💡 **Quant Insight**

Quotes are not just numbers — they are **live data objects**.

Types:
- Simple → raw data  
- Derived → transformation  
- Composite → combination  
- DeltaVol → market convention  

👉 Together, they allow building complex market structures dynamically.
""")

# ---------------------------------------------------
# 🔗 6. Handles (VERY IMPORTANT)
# ---------------------------------------------------

st.markdown("---")

st.markdown('## <span id="handles">🔗 6. Handles</span>', unsafe_allow_html=True)

st.markdown("""
### 🧠 What are Handles in QuantLib?

A **Handle** is a wrapper around an object (like a quote or curve) that allows:

👉 **dynamic updates without rebuilding the system**

---

### ⚙️ Why Handles Matter

Instead of passing raw values, QuantLib uses handles so that:

- 📈 Market data changes automatically propagate  
- 🔄 No need to recreate instruments or models  
- ⚡ Efficient real-time pricing  

---

### 🧩 Types of Handles

- **Handle** → fixed reference (read-only style)  
- **RelinkableHandle** → can switch underlying object dynamically  
""")

# ---------------------------------------------------
# 🎮 Interactive Demo
# ---------------------------------------------------

st.markdown("### 🧪 Interactive Handle Demo")

# Persist state
if "spot_quote" not in st.session_state:
    st.session_state.spot_quote = ql.SimpleQuote(100)

spot = st.session_state.spot_quote
handle = ql.QuoteHandle(spot)

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("#### 📥 Update Spot Price")

    new_spot = st.slider("Spot Price", 50, 200, int(spot.value()))

    if st.button("Update Spot"):
        spot.setValue(new_spot)

with col2:
    st.markdown("#### 📤 Values")

    st.success(f"Direct Quote Value: {spot.value():.2f}")
    st.info(f"Handle Value: {handle.value():.2f}")

# ---------------------------------------------------
# 🔄 Relinkable Handle Demo (VERY IMPORTANT)
# ---------------------------------------------------

st.markdown("### 🔄 Relinkable Handle Demo")

if "handle_link" not in st.session_state:
    h = ql.RelinkableQuoteHandle()
    h.linkTo(ql.SimpleQuote(100))
    st.session_state.handle_link = h

rel_handle = st.session_state.handle_link

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("#### 🔁 Switch Underlying Quote")

    if st.button("Switch to 200"):
        rel_handle.linkTo(ql.SimpleQuote(200))

    if st.button("Switch to 50"):
        rel_handle.linkTo(ql.SimpleQuote(50))

with col2:
    st.markdown("#### 📤 Current Linked Value")
    st.success(f"{rel_handle.value():.2f}")

# ---------------------------------------------------
# 📊 Visualization
# ---------------------------------------------------

st.markdown("### 📊 Handle Behavior")

import pandas as pd

values = [spot.value(), handle.value(), rel_handle.value()]
labels = ["Quote", "Handle", "Relinkable"]

df = pd.DataFrame({"Value": values}, index=labels)
st.bar_chart(df)

# ---------------------------------------------------
# 💻 Code
# ---------------------------------------------------

st.markdown("#### 💻 Code Equivalent")
st.code("""
spot = ql.SimpleQuote(100)

# Standard handle
handle = ql.QuoteHandle(spot)

# Relinkable handle
rel = ql.RelinkableQuoteHandle()
rel.linkTo(ql.SimpleQuote(200))

spot.setValue(120)  # propagates automatically
""")

# ---------------------------------------------------
# 🧠 Deep Insight
# ---------------------------------------------------

st.info("""
💡 **Quant Insight**

Handles are the backbone of QuantLib’s architecture:

Quote → Handle → Term Structure → Instrument → Engine

👉 Without handles, every market update would require rebuilding the entire system.

This design enables:
- Real-time pricing systems  
- Efficient risk calculations  
- Clean dependency management  
""")
# ---------------------------------------------------
# 🧠 Key Insight
# ---------------------------------------------------


st.markdown('## <span id="summary">🗓️ Summary </span>', unsafe_allow_html=True)
    # ---------------------------------------------------
    # Evaluation Date
    # ---------------------------------------------------
st.markdown("#### 🗓️ Evaluation Date")
st.markdown("👉 Sets the 'current time' for all pricing calculations.")
st.code("""
ql.Settings.instance().evaluationDate = ql.Date(15,6,2020)
""")

# ---------------------------------------------------
# Array
# ---------------------------------------------------
st.markdown("#### 📊 Array")
st.markdown("👉 1D numerical container used in models and computations.")
st.code("""
arr = ql.Array(5)
for i in range(5):
arr[i] = i
""")

# ---------------------------------------------------
# Matrix
# ---------------------------------------------------
st.markdown("#### 📐 Matrix")
st.markdown("👉 2D numerical structure used in PDE, optimization, and linear algebra.")
st.code("""
matrix = ql.Matrix(3,3,0.5)
matrix[0][0] = 1.0
""")

# ---------------------------------------------------
# Observer
# ---------------------------------------------------
st.markdown("#### 🔄 Observer")
st.markdown("👉 Watches for changes in market data and triggers updates.")
st.code("""
def callback():
print("Updated!")

observer = ql.Observer(callback)
observer.registerWith(quote)
""")

# ---------------------------------------------------
# Quotes
# ---------------------------------------------------
st.markdown("#### 💰 Quotes")

st.markdown("""
👉 Represents **market data objects** used throughout QuantLib.

Types:
- **SimpleQuote** → raw value (price, rate, vol)  
- **DerivedQuote** → transformation of another quote  
- **CompositeQuote** → combination of multiple quotes  
- **DeltaVolQuote** → FX-style volatility quotes (delta-based)  

👉 All quotes are **observable**, so changes automatically propagate.
""")

st.code("""
# SimpleQuote (basic market data)
q = ql.SimpleQuote(0.05)
q.setValue(0.1)

# DerivedQuote (transform)
d = ql.DerivedQuote(ql.QuoteHandle(q), lambda x: 10*x)

# CompositeQuote (combine)
c = ql.CompositeQuote(
    ql.QuoteHandle(q),
    ql.QuoteHandle(ql.SimpleQuote(0.02)),
    lambda x,y: x+y
)

# DeltaVolQuote (FX volatility)
atm = ql.DeltaVolQuote(
    ql.QuoteHandle(ql.SimpleQuote(0.08)),
    ql.DeltaVolQuote.Fwd,
    1.0,
    ql.DeltaVolQuote.AtmFwd
)
""")

# ---------------------------------------------------
# Handle
# ---------------------------------------------------
st.markdown("#### 🔗 Handle")
st.markdown("👉 Wraps objects to allow dynamic updates across system.")
st.code("""
spot = ql.SimpleQuote(100)
handle = ql.QuoteHandle(spot)
""")

# ---------------------------------------------------
# Relinkable Handle
# ---------------------------------------------------
st.markdown("#### 🔄 Relinkable Handle")
st.markdown("👉 Allows switching underlying object without rebuilding system.")
st.code("""
rel = ql.RelinkableQuoteHandle()
rel.linkTo(ql.SimpleQuote(200))
""")

# ---------------------------------------------------
# NPV
# ---------------------------------------------------
st.markdown("#### 📉 NPV")
st.markdown("👉 Computes present value of future cashflows.")
st.code("""
ql.CashFlows.npv(leg, rate, False)
""")

# ---------------------------------------------------
# Interest Rate
# ---------------------------------------------------
st.markdown("#### 📈 InterestRate")
st.markdown("👉 Encapsulates compounding and discounting logic.")
st.code("""
rate = ql.InterestRate(0.05, ql.Actual360(), ql.Compounded, ql.Annual)
""")

# ---------------------------------------------------
# Schedule
# ---------------------------------------------------
st.markdown("#### 📅 Schedule")
st.markdown("👉 Generates payment dates for instruments.")
st.code("""
schedule = ql.MakeSchedule(start, end, ql.Period('6M'))
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

_, nav_col = st.columns([1, 1])
with nav_col:
    if st.button("➡️ Next: Cashflows & Legs"):
        st.switch_page("pages/02_Cashflows_Legs.py")