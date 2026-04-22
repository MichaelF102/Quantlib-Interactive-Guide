import streamlit as st

st.set_page_config(
    page_title="QuantLib Interactive Guide",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
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
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.5);
    }
</style>
""", unsafe_allow_html=True)


# Custom CSS for a premium look
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #1e1e2f 0%, #121212 100%);
        color: #ffffff;
    }
    .stTitle {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        background: -webkit-linear-gradient(#00c6ff, #0072ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .card {
        padding: 20px;
        border-radius: 15px;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("⚖️ QuantLib Interactive Guide")
st.subheader("Master Quantitative Finance with Python and QuantLib")

st.markdown("""
Welcome to the **QuantLib Interactive Guide**. This application is designed to help you navigate the complex world of quantitative finance using the QuantLib library.

### 🚀 Explore the Modules
Choose a topic below to jump directly to the interactive guide:

<style>
/* Custom styling for page links to look like cards */
[data-testid="stPageLink"] {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    padding: 5px;
    transition: all 0.3s ease;
}
[data-testid="stPageLink"]:hover {
    background: rgba(255, 255, 255, 0.15);
    border-color: #00d4ff;
    transform: translateY(-2px);
}
</style>

""" , unsafe_allow_html=True)

toc_data = [
    ("pages/01_Basics.py", "01 Basics", "🏗️"),
    ("pages/02_Cashflows_Legs.py", "02 Cashflows & Legs", "💰"),
    ("pages/03_Currencies.py", "03 Currencies", "💱"),
    ("pages/04_Dates_Conventions.py", "04 Dates & Conventions", "📅"),
    ("pages/05_Indexes.py", "05 Indexes", "📈"),
    ("pages/06_Instruments.py", "06 Instruments", "📂"),
    ("pages/07_Math_Tools.py", "07 Math Tools", "🧮"),
    ("pages/08_Pricing_Engines.py", "08 Pricing Engines", "⚙️"),
    ("pages/09_Pricing_Models.py", "09 Pricing Models", "📐"),
    ("pages/10_Stochastic_Processes.py", "10 Stochastic Processes", "🎲"),
    ("pages/11_Term_Structures.py", "11 Term Structures", "📉"),
    ("pages/12_Helpers.py", "12 Calibration Helpers", "🛠️"),
]

# Create a 3x4 grid for the 12 pages
for i in range(0, len(toc_data), 3):
    cols = st.columns(3)
    for j in range(3):
        if i + j < len(toc_data):
            path, label, icon = toc_data[i + j]
            with cols[j]:
                st.page_link(path, label=label, icon=icon, use_container_width=True)

st.markdown("---")



st.markdown("## 🧠 What is QuantLib?")

st.markdown("""
**QuantLib** is an open-source library used by quantitative analysts, traders, and financial engineers to:

- 📊 Price financial instruments (options, bonds, swaps)
- 📉 Build yield curves and volatility surfaces
- ⚙️ Model market dynamics (interest rates, equities, credit)
- 🧮 Perform risk analysis and scenario simulation

It acts as a **financial computation engine** powering real-world trading systems.
""")

st.markdown("---")
st.markdown("## 🏗️ How QuantLib Works")

st.code("""
Market Data → Term Structures → Models → Instruments → Pricing Engines → Results
""")

st.markdown("""
Each component plays a specific role:

- **Market Data** → Inputs (rates, vol, prices)
- **Term Structures** → Curves (yield, volatility)
- **Models** → Market assumptions (Black-Scholes, Hull-White)
- **Instruments** → Financial products
- **Pricing Engines** → Compute valuation

👉 This modular design makes QuantLib extremely powerful and flexible.
""")

st.markdown("---")

st.markdown("## 💼 Real-World Use Cases")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
        <h4>📈 Derivatives Pricing</h4>
        <p>Options, swaps, structured products using advanced models.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <h4>📊 Risk Management</h4>
        <p>Greeks, sensitivities, VaR, stress testing.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
        <h4>🏦 Fixed Income</h4>
        <p>Yield curves, bond pricing, interest rate modeling.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("## 🧠 Core Concepts You Must Know")

st.markdown("""
- Evaluation Date  
- Day Count Conventions  
- Yield Curves  
- Discounting  
- Compounding  
- Cashflows & Legs  
- Pricing Engines  

👉 Master these → QuantLib becomes easy.
""")

st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="card">
        <h3>📂 Structured Learning</h3>
        <p>Follow the numbered pages in the sidebar for a step-by-step introduction to QuantLib's architecture.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <h3>🧪 Interactive Examples</h3>
        <p>Each section contains live code examples where you can tweak parameters and see the results in real-time.</p>
    </div>
    """, unsafe_allow_html=True)

st.sidebar.success("Select a topic above to begin.")
st.sidebar.markdown("Made By Michael Fernandes")

st.markdown("""
## 👨‍💻 About the Creator

This project is built by **Michael Fernandes** — a passionate developer with strong interests in:

- 📊 Data Science  
- ⚙️ Automation  
- 💹 Quantitative Finance  

I enjoy building **interactive tools and systems** that simplify complex concepts and make learning more intuitive.

🔗 **Explore more of my work:**
- GitHub: https://github.com/MichaelF102  
- LinkedIn: https://www.linkedin.com/in/michael-fernandes-7a3b6227a/
""")
