import streamlit as st
import QuantLib as ql
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="QuantLib - Indexes", layout="wide")

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

st.title("📈 Indexes & Index Management")

# ===================================================
# 📚 TABLE OF CONTENTS
# ===================================================

st.markdown("## 📚 Table of Contents")

st.markdown("""
<div style="line-height:2; font-size:16px;">
🔹 <a href="#index" target="_self">1. The Index Base Class</a><br>
🔹 <a href="#manager" target="_self">2. IndexManager (Global Repository)</a><br>
🔹 <a href="#interestrate" target="_self">3. Interest Rate Indexes (IBOR, Overnight, Swap)</a><br>
🔹 <a href="#inflation" target="_self">4. Inflation Indexes (Zero, YoY)</a><br>
</div>
""", unsafe_allow_html=True)

# ===================================================
# 🏛️ 1. INDEX BASE CLASS
# ===================================================

st.markdown("---")
st.markdown('## <span id="index">🏛️ 1. The Index Base Class</span>', unsafe_allow_html=True)

st.markdown("""
### 🧠 What is an Index?
The `Index` class is a purely abstract base class in QuantLib that defines the interface for all financial indexes. 
It provides the structure for managing **Fixings** — historical price or rate data used by instruments.

👉 **Key Methods Inherited by All Subclasses:**
- `name()`: Returns the unique identifier of the index.
- `fixingCalendar()`: The calendar used to determine valid fixing dates.
- `fixing(date)`: Returns the fixing value (historical or forecasted).
- `addFixing(date, value)`: Stores a historical fixing.
- `isValidFixingDate(date)`: Checks against the holiday calendar.
""")

# ---------------------------------------------------
# 🎮 INTERACTIVE: FIXING TESTER
# ---------------------------------------------------
st.markdown("### 🎮 Interactive Fixing Tester")

col1, col2 = st.columns(2)

with col1:
    test_idx = ql.Euribor3M()
    st.write(f"**Index:** {test_idx.name()}")
    st.write(f"**Fixing Calendar:** {test_idx.fixingCalendar()}")
    
    fixing_date = st.date_input("Select Fixing Date", datetime(2024, 6, 15))
    ql_fixing_date = ql.Date(fixing_date.day, fixing_date.month, fixing_date.year)
    
    fixing_value = st.number_input("Fixing Value (%)", value=3.5, step=0.1) / 100.0

    if st.button("➕ Add Fixing to Global Manager"):
        ql.IndexManager.instance().clearHistories() # Clear for demo purposes
        test_idx.addFixing(ql_fixing_date, fixing_value)
        st.success(f"Stored {fixing_value:.4%} for {test_idx.name()} on {ql_fixing_date}")

with col2:
    st.markdown("#### 🔍 Fixing Status")
    has_fixing = test_idx.hasHistoricalFixing(ql_fixing_date)
    st.write(f"**Has historical fixing?** {'✅ Yes' if has_fixing else '❌ No'}")
    
    if has_fixing:
        st.info(f"**Retrieved Fixing:** {test_idx.fixing(ql_fixing_date):.4%}")
    else:
        st.warning("Fixing not found in memory.")

# ===================================================
# 🗃️ 2. INDEXMANAGER
# ===================================================

st.markdown("---")
st.markdown('## <span id="manager">🗃️ 2. IndexManager (Global Repository)</span>', unsafe_allow_html=True)

st.markdown("""
### 🧠 The Global Hub
To ensure consistency across the entire library, QuantLib uses a unique global repository: the `IndexManager`. 
It stores time-series data for every index registered.

👉 **Common Usage:**
```python
# Access the instance
manager = ql.IndexManager.instance()

# See which indexes have histories
list_of_names = manager.histories()

# Clear all data
manager.clearHistories()
```
""")

if st.button("📋 Refresh Index Histories"):
    histories = ql.IndexManager.instance().histories()
    if histories:
        st.write("Stored Indexes:", list(histories))
    else:
        st.info("No histories currently stored in the global manager.")

# ===================================================
# 📈 3. INTEREST RATE INDEXES
# ===================================================

st.markdown("---")
st.markdown('## <span id="interestrate">🔢 3. Interest Rate Indexes</span>', unsafe_allow_html=True)

st.markdown("""
### 🧠 IBOR, Overnight & Swap Indexes
These are the building blocks for bonds, swaps, and floaters.
""")

with st.expander("📝 Types of Interest Rate Indexes"):
    st.markdown("""
    - **IborIndex**: Interbank Offered Rates (e.g., EURIBOR, LIBOR).
    - **OvernightIndex**: Compounded daily rates (e.g., SOFR, SONIA, €STR).
    - **SwapIndex**: Forward-looking swap rates used for CMS (Constant Maturity Swaps).
    - **SwapSpreadIndex**: The difference between two swap rates (e.g., 10Y - 2Y).
    """)

# ---------------------------------------------------
# 🎮 EXPLORER: COMMON IR INDEXES
# ---------------------------------------------------
st.markdown("### 🔍 Explorer: Common IR Indexes")

ir_idx_map = {
    "Euribor 6M": ql.Euribor6M(),
    "USD Libor 3M": ql.USDLibor(ql.Period("3M")),
    "SOFR (Overnight)": ql.Sofr(),
    "SONIA (Overnight)": ql.Sonia(),
    "Euribor Swap 10Y": ql.EuriborSwapIsdaFixA(ql.Period("10Y"))
}

sel_ir = st.selectbox("Select an Index to Inspect", list(ir_idx_map.keys()))
idx_obj = ir_idx_map[sel_ir]

col_ir1, col_ir2 = st.columns(2)

with col_ir1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.write(f"**Family Name:** {idx_obj.familyName()}")
    st.write(f"**Tenor:** {idx_obj.tenor() if hasattr(idx_obj, 'tenor') else 'Overnight'}")
    st.write(f"**Currency:** {idx_obj.currency()}")
    st.write(f"**Fixing Days:** {idx_obj.fixingDays()}")
    st.markdown('</div>', unsafe_allow_html=True)

with col_ir2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.write(f"**Day Counter:** {idx_obj.dayCounter()}")
    st.write(f"**Fixing Calendar:** {idx_obj.fixingCalendar()}")
    
    ref_date = ql.Date.todaysDate()
    try:
        st.write(f"**Value Date for Today:** {idx_obj.valueDate(ref_date)}")
        st.write(f"**Maturity for Today:** {idx_obj.maturityDate(idx_obj.valueDate(ref_date))}")
    except:
        st.write("Dates: Dependent on Curve linking.")
    st.markdown('</div>', unsafe_allow_html=True)

# ===================================================
# 🎈 4. INFLATION INDEXES
# ===================================================

st.markdown("---")
st.markdown('## <span id="inflation">🎈 4. Inflation Indexes</span>', unsafe_allow_html=True)

st.markdown("""
### 🧠 Zero & YoY Inflation
QuantLib supports complex inflation modeling for indexed bonds and derivatives.

- **ZeroInflationIndex**: Measures absolute price levels (CPI/HICP).
- **YoYInflationIndex**: Measures year-on-year percentage change.
""")

col_inf1, col_inf2 = st.columns(2)

with col_inf1:
    inf_sel = st.selectbox("Common Inflation Indexes", ["UK RPI", "US CPI", "EU HICP"])
    inf_obj = {"UK RPI": ql.UKRPI, "US CPI": ql.USCPI, "EU HICP": ql.EUHICP}[inf_sel]
    
    # We instantiate a dummy version for inspection
    # Params: familyName, region, revised, frequency, availabilityLag, currency
    st.markdown("#### 💻 Code Snippet")
    st.code(f"""
# Accessing {inf_sel}
idx = ql.{inf_obj.__name__}()
print(idx.name())
print(idx.availabilityLag())
    """)

with col_inf2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown(f"**Types in QuantLib:**")
    st.write("- `ZeroInflationIndex` (Base Level)")
    st.write("- `YoYInflationIndex` (Growth Rate)")
    st.write("- `ZeroInflationTermStructureHandle` (Linking to Curves)")
    st.markdown('</div>', unsafe_allow_html=True)

# ===================================================
# 📝 SUMMARY
# ===================================================

st.markdown("---")
st.info("""
💡 **Quant Insight**

Indexes are **stateless metadata providers**. They don't know the rate for "6 months from now" unless you link them to a **YieldTermStructure** (Curve).

👉 **The Flow:**
1. Create Index (e.g. `Euribor3M`)
2. Link to Curve (using `relinkableHandle`)
3. Use Index in Instrument (Bond, Swap)
4. Valuation engine calls `index.fixing(date)`

---
*Next up: Instruments — where we put these indexes to work!*
""")

# ===================================================
#  NAVIGATION
# ===================================================

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
    if st.button("⬅️ Previous: Dates"):
        st.switch_page("pages/04_Dates_Conventions.py")

with nav_col4:
    if st.button("➡️ Next: Instruments"):
        st.switch_page("pages/06_Instruments.py")
