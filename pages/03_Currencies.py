import streamlit as st
import QuantLib as ql
import pandas as pd

st.set_page_config(page_title="QuantLib - Currencies", layout="wide")

# Custom CSS for Premium Design

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

st.title("💱 Currencies, Money & Exchange Rates")

# ===================================================
# 📚 TABLE OF CONTENTS
# ===================================================

st.markdown("## 📚 Table of Contents")

st.markdown("""
<div style="line-height:2; font-size:16px;">
🔹 <a href="#currency" target="_self">Currency Class</a><br>
🔹 <a href="#money" target="_self">Money Class</a><br>
🔹 <a href="#exchangerate" target="_self">Exchange Rates</a><br>
🔹 <a href="#simulator" target="_self">Currency & FX Simulator</a><br>
🔹 <a href="#summary" target="_self">Summary Cheat Sheet</a><br>
</div>
""", unsafe_allow_html=True)

# ===================================================
# 📈 1. CURRENCY
# ===================================================

st.markdown("---")
st.markdown('## <span id="currency">🏛️ 1. Currency Class</span>', unsafe_allow_html=True)

st.markdown("""
### 🧠 What is a Currency?

In QuantLib, a `Currency` object describes a specific ISO 4217 financial currency. It handles metadata like codes, symbols, and rounding rules.

👉 **Key Member Functions:**
- `name()`: Full name (e.g., "U.S. dollar")
- `code()`: ISO 4217 code (e.g., "USD")
- `symbol()`: Real-world symbol (e.g., "$")
- `fractionsPerUnit()`: Sub-units per main unit (usually 100)
- `rounding()`: The default rounding rule for that currency
""")

st.markdown("### 🎮 Interactive Explorer")

currency_map = {
    "USD - US Dollar": ql.USDCurrency(),
    "EUR - Euro": ql.EURCurrency(),
    "GBP - British Pound": ql.GBPCurrency(),
    "JPY - Japanese Yen": ql.JPYCurrency(),
    "INR - Indian Rupee": ql.INRCurrency(),
    "CHF - Swiss Franc": ql.CHFCurrency(),
    "CNY - Chinese Yuan": ql.CNYCurrency()
}

selected_cur_name = st.selectbox("Select a Currency to Inspect", list(currency_map.keys()))
cur = currency_map[selected_cur_name]

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.write(f"**Name:** {cur.name()}")
    st.write(f"**Code (ISO):** {cur.code()}")
    
    # Safely handle symbol that might cause UnicodeEncodeError (surrogates)
    try:
        sym = cur.symbol()
        st.write(f"**Symbol:** {sym}")
    except:
        st.write("**Symbol:** [Encoding Issue]")
        
    st.write(f"**Numeric Code:** {cur.numericCode()}")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.write(f"**Fractions per Unit:** {cur.fractionsPerUnit()}")
    
    # Safely handle fraction symbol
    try:
        fsym = cur.fractionSymbol()
        st.write(f"**Fraction Symbol:** {fsym}")
    except:
        st.write("**Fraction Symbol:** [Encoding Issue]")
        
    st.write(f"**Is Empty?** {cur.empty()}")
    st.markdown('</div>', unsafe_allow_html=True)

st.code(f"""
# Code Example
cur = ql.{selected_cur_name.split(' ')[0]}Currency()
print(cur.name())   # {cur.name()}
print(cur.code())   # {cur.code()}
""")

# ===================================================
# 💰 2. MONEY
# ===================================================

st.markdown("---")
st.markdown('## <span id="money">💰 2. Money Class</span>', unsafe_allow_html=True)

st.markdown("""
### 🧠 Doing Math with Currencies

To perform algebraic calculations (addition, multiplication) in QuantLib, you wrap a value and a currency into a `Money` object.

👉 **Important Syntax:**
- `ql.Money(value, currency)`
- You can also multiply a number directly by a currency object! (`100 * cur`)
""")

st.markdown("### 🎮 Multiplication Simulator")

amount = st.number_input("Enter Amount", value=100.0, step=10.0, key="money_amount")
cur_obj = currency_map[selected_cur_name]

# QuantLib calculation
m = amount * cur_obj

st.success(f"Result: **{m.value():.2f} {cur_obj.code()}**")

st.code(f"""
cur = ql.{cur_obj.code()}Currency()
balance = {amount} * cur
print(f"{{balance.value()}} {{balance.currency().code()}}")
""")

# ===================================================
# 📈 3. EXCHANGE RATE
# ===================================================

st.markdown("---")
st.markdown('## <span id="exchangerate">🔀 3. Exchange Rates</span>', unsafe_allow_html=True)

st.markdown("""
### 🧠 Converting Currencies

`ExchangeRate` defines the conversion logic between a source and a target currency.

- **Direct Rate**: Constructed manually with a fixed rate.
- **Derived Rate**: Constructed via triangulation (e.g., USD → EUR using EUR → GBP and GBP → USD).
""")

st.code("""
# Constructor
usd = ql.USDCurrency()
eur = ql.EURCurrency()
rate = ql.ExchangeRate(eur, usd, 1.14) # 1 EUR = 1.14 USD

# Convert Money
m_eur = ql.Money(100, eur)
m_usd = rate.exchange(m_eur) # Returns Money object in USD
""")

# ===================================================
# 🛠️ 4. SIMULATOR
# ===================================================

st.markdown("---")
st.markdown('## <span id="simulator">🛠️ 4. Currency & FX Simulator</span>', unsafe_allow_html=True)

col_a, col_b = st.columns(2)

with col_a:
    src_name = st.selectbox("Source Currency", list(currency_map.keys()), index=1, key="src_cur")
    target_name = st.selectbox("Target Currency", list(currency_map.keys()), index=0, key="target_cur")

with col_b:
    fx_rate = st.number_input(f"Exchange Rate ({src_name.split(' ')[0]} to {target_name.split(' ')[0]})", value=1.1, format="%.4f", key="fx_rate_input")
    convert_amount = st.number_input("Amount to Convert", value=100.0, key="convert_amount")

src_cur = currency_map[src_name]
tgt_cur = currency_map[target_name]

if src_cur.code() == tgt_cur.code():
    st.warning("Please select two different currencies for conversion.")
else:
    # Construct Rate
    rate_obj = ql.ExchangeRate(src_cur, tgt_cur, fx_rate)
    
    # Construct Money
    m_src = convert_amount * src_cur
    
    # Perform Conversion
    m_tgt = rate_obj.exchange(m_src)
    
    st.markdown('<div class="glass-card" style="text-align: center;">', unsafe_allow_html=True)
    st.subheader(f"Conversion Result")
    st.title(f"{m_tgt.value():.2f} {tgt_cur.code()}")
    st.markdown(f"**Rate Used:** 1 {src_cur.code()} = {fx_rate} {tgt_cur.code()}")
    st.markdown('</div>', unsafe_allow_html=True)

    # Details
    st.markdown("#### 🔍 Object Details")
    st.write(f"Source: {rate_obj.source().name()}")
    st.write(f"Target: {rate_obj.target().name()}")
    st.write(f"Type: {'Direct' if rate_obj.type() == 0 else 'Derived'}")

# ===================================================
# 📝 5. SUMMARY
# ===================================================

st.markdown("---")
st.markdown('## <span id="summary">📝 5. Summary Cheat Sheet</span>', unsafe_allow_html=True)

st.info("""
💡 **Quant Insight**

Currencies are static data objects, while `Money` and `ExchangeRate` are dynamic operational objects.

- **Currency**: `name()`, `code()`, `symbol()`, `rounding()`
- **Money**: `Money(val, cur)`, `value()`, `currency()`
- **ExchangeRate**: `ExchangeRate(src, tgt, rate)`, `exchange(money)`

👉 Remember that QuantLib handles the math of currency conversions strictly to prevent adding "Apple" (USD) with "Oranges" (EUR) without an explicit rate.
""")

# ===================================================
#  NAVIGATION
# ===================================================

st.markdown("---")

# Custom CSS for Right Alignment of the Next button
st.markdown("""
<style>
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) button {
        margin-left: auto;
        display: block;
    }
</style>
""", unsafe_allow_html=True)

nav_col1, nav_col2 = st.columns([1, 1])

with nav_col1:
    if st.button("⬅️ Previous: Cashflows & Legs"):
        st.switch_page("pages/02_Cashflows_Legs.py")

with nav_col2:
    if st.button("➡️ Next: Dates & Conventions"):
        st.switch_page("pages/04_Dates_Conventions.py")
