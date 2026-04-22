import streamlit as st
import QuantLib as ql
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import quad

st.set_page_config(page_title="QuantLib - Math Tools", layout="wide")

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

st.title("🧮 Math Tools in QuantLib")

# ===================================================
# 📚 TABLE OF CONTENTS
# ===================================================

st.markdown("## 📚 Table of Contents")

st.markdown("""
<div style="line-height:2; font-size:16px;">
🔹 <a href="#solvers" target="_self">1. 1D Solvers (Root Finding)</a><br>
🔹 <a href="#integration" target="_self">2. Integration (Gaussian Quadrature)</a><br>
🔹 <a href="#interpolation" target="_self">3. Interpolation Methods (1D & 2D)</a><br>
🔹 <a href="#optimization" target="_self">4. Optimization & Random Numbers</a><br>
🔹 <a href="#rng" target="_self">5. Random Number Generators</a><br>
🔹 <a href="#paths" target="_self">6. Path Generators</a><br>
🔹 <a href="#statistics" target="_self">7. Statistics</a><br>
</div>
""", unsafe_allow_html=True)

# ===================================================
# 🎯 1. SOLVERS
# ===================================================

st.markdown("---")
st.markdown('## <span id="solvers">🎯 1. 1D Solvers</span>', unsafe_allow_html=True)

st.markdown("""
### 🧠 Root Finding
QuantLib provides several types of 1D solvers to find $x$ such that $f(x) = 0$.

👉 **Available Solvers:**
- `ql.Brent`, `ql.Bisection`, `ql.Secant`, `ql.Ridder`, `ql.FalsePosition`
- `ql.Newton` (requires derivative)
""")

# 🎮 INTERACTIVE: SOLVER TESTER
st.markdown("#### 🎮 Interactive Solver: Find Root of $x^2 - A = 0$")

s_col1, s_col2 = st.columns([1, 2])

with s_col1:
    s_a = st.number_input("Target A (Find square root of A)", value=16.0, step=1.0)
    s_guess = st.number_input("Initial Guess", value=1.0)
    s_method = st.selectbox("Solver Method", ["Brent", "Bisection", "Secant", "Ridder"])
    
    def f(x):
        return x**2 - s_a

    solver_map = {
        "Brent": ql.Brent(),
        "Bisection": ql.Bisection(),
        "Secant": ql.Secant(),
        "Ridder": ql.Ridder()
    }
    
    if st.button("🚀 Solve"):
        solver = solver_map[s_method]
        try:
            root = solver.solve(f, 1e-6, s_guess, 0.01)
            st.success(f"**Root Found:** {root:.6f}")
        except Exception as e:
            st.error(f"Solver Error: {e}")

with s_col2:
    st.markdown("#### 💻 Code Example")
    st.code(f"""
def f(x):
    return x**2 - {s_a}

solver = ql.{s_method}()
root = solver.solve(f, 1e-6, {s_guess}, 0.1)
print(f"Root: {{root}}")
""")

# ===================================================
# 📐 2. INTEGRATION
# ===================================================

st.markdown("---")
st.markdown('## <span id="integration">📐 2. Integration</span>', unsafe_allow_html=True)

st.markdown("""
### 🧠 Gaussian Quadrature
QuantLib uses Gaussian Quadrature for efficient numerical integration.

👉 **Note:** By default, `GaussLegendre` operates on [-1, 1]. For custom boundaries [a, b], we scale input parameters.
""")

st.code("""
# ql versus scipy
f = lambda x: x**2
quad_ql = ql.GaussLegendreIntegration(128)
result = quad_ql(f) # Definite integral on [-1, 1]
""")

# ===================================================
# 📈 3. INTERPOLATION
# ===================================================

st.markdown("---")
st.markdown('## <span id="interpolation">📈 3. Interpolation</span>', unsafe_allow_html=True)

st.markdown("""
### 🧠 1D & 2D Methods
Commonly used for building yield curves or volatility surfaces.
""")

# 🎮 INTERACTIVE: INTERPOLATION COMPARISON
st.markdown("#### 🎮 Compare 1D Methods")

X = [1., 2., 3., 4., 5.]
Y = [0.5, 0.8, 0.7, 0.9, 0.85]

i_sel = st.multiselect("Select Methods to Compare", 
                      ["Linear", "CubicNaturalSpline", "ForwardFlat"], 
                      default=["Linear", "CubicNaturalSpline"])

xx = np.linspace(1, 6, 100)
fig, ax = plt.subplots(figsize=(10, 4))
ax.scatter(X, Y, color='cyan', label='Original Data', zorder=5)

if "Linear" in i_sel:
    interp = ql.LinearInterpolation(X, Y)
    yy = [interp(x, True) for x in xx]
    ax.plot(xx, yy, label='Linear')

if "CubicNaturalSpline" in i_sel:
    interp = ql.CubicNaturalSpline(X, Y)
    yy = [interp(x, True) for x in xx]
    ax.plot(xx, yy, label='Cubic Spline')

if "ForwardFlat" in i_sel:
    interp = ql.ForwardFlatInterpolation(X, Y)
    yy = [interp(x, True) for x in xx]
    ax.plot(xx, yy, label='Forward Flat')

ax.legend()
ax.set_facecolor('#1e1e1e')
fig.patch.set_facecolor('#0f0c29')
ax.tick_params(colors='white')
st.pyplot(fig)

# ===================================================
# 🛠️ 4. OPTIMIZATION
# ===================================================

st.markdown("---")
st.markdown('## <span id="optimization">🛠️ 4. Optimization</span>', unsafe_allow_html=True)

st.markdown("""
QuantLib provides an optimization framework for model calibration (e.g., Levenberg-Marquardt, Simplex, Conjugate Gradient).
""")

# ===================================================
# 🎲 5. RANDOM NUMBERS
# ===================================================

st.markdown("---")
st.markdown('## <span id="rng">🎲 5. Random Number Generators</span>', unsafe_allow_html=True)

st.markdown("""
### 🧠 Pseudo & Quasi Random
QuantLib supports standard generators and low-bias sequences (Sobol, Halton) for Monte Carlo simulations.
""")

rng_col1, rng_col2 = st.columns(2)

with rng_col1:
    st.markdown("#### Pseudo-Random (Uniform)")
    st.write("- `ql.MersenneTwisterUniformRng` (Standard)")
    st.write("- `ql.LecuyerUniformRng`")
    
    st.markdown("#### Gaussian (Normal)")
    st.write("- `ql.BoxMullerMersenneTwisterGaussianRng` (Classic)")
    st.write("- `ql.InvCumulativeMersenneTwisterGaussianRng` (Accurate)")

with rng_col2:
    st.markdown("#### Quasi-Random (Low Bias)")
    st.write("- `ql.SobolRsg` (Best for high dimensions)")
    st.write("- `ql.HaltonRsg` (Consistent)")

# 🎮 INTERACTIVE: RNG TESTER
st.markdown("#### 🎮 Interactive RNG Generator")
seed = st.number_input("RNG Seed", value=12345)
if st.button("🎲 Generate Samples"):
    unifMt = ql.MersenneTwisterUniformRng(int(seed))
    bmGauss = ql.BoxMullerMersenneTwisterGaussianRng(unifMt)
    samples = [bmGauss.next().value() for _ in range(10)]
    st.write("Samples from Normal Distribution:", samples)

# ===================================================
# 🛤️ 6. PATH GENERATORS
# ===================================================

st.markdown("---")
st.markdown('## <span id="paths">🛤️ 6. Path Generators</span>', unsafe_allow_html=True)

st.markdown("""
Combines a stochastic process and an RNG to produce price paths.
""")

st.code("""
# Heston Path Generation Example
process = ql.HestonProcess(riskFreeTS, dividendTS, spot, v0, kappa, theta, sigma, rho)
times = ql.TimeGrid(length, timestep)
rng = ql.GaussianRandomSequenceGenerator(...)
pathGenerator = ql.GaussianMultiPathGenerator(process, list(times), rng)
""")

# ===================================================
# 📊 7. STATISTICS
# ===================================================

st.markdown("---")
st.markdown('## <span id="statistics">📊 7. Statistics</span>', unsafe_allow_html=True)

st.markdown("""
QuantLib includes statistics accumulators for Monte Carlo paths.
- `ql.Statistics`: Accumulates mean, variance, skewness, and kurtosis.
- `ql.IncrementalStatistics`: Updates parameters incrementally to save memory.
""")

st.code("""
stats = ql.Statistics()
for path in paths:
    stats.add(path.price_at_maturity)
print(f"Mean Outcome: {stats.mean()}")
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
    if st.button("⬅️ Previous: Instruments"):
        st.switch_page("pages/06_Instruments.py")

with nav_col4:
    if st.button("➡️ Next: Pricing Engines"):
        st.switch_page("pages/08_Pricing_Engines.py")
