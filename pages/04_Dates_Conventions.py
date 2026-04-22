import streamlit as st
import QuantLib as ql
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="QuantLib - Dates & Conventions", layout="wide")

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

st.title("📅 Dates, Calendars & Conventions")

# ===================================================
# 📚 TABLE OF CONTENTS
# ===================================================

st.markdown("## 📚 Table of Contents")

st.markdown("""
<div style="line-height:2; font-size:16px;">
🔹 <a href="#conventions" target="_self">1. Conventions (Compounding, Frequencies, Business Days)</a><br>
🔹 <a href="#date" target="_self">2. Date Class</a><br>
🔹 <a href="#period" target="_self">3. Period Class</a><br>
🔹 <a href="#calendar" target="_self">4. Calendar Class</a><br>
🔹 <a href="#daycounter" target="_self">5. DayCounter Class</a><br>
🔹 <a href="#schedule" target="_self">6. Schedule Class</a><br>
🔹 <a href="#makeschedule" target="_self">7. MakeSchedule Utility</a><br>
🔹 <a href="#timegrid" target="_self">8. TimeGrid Class</a><br>
</div>
""", unsafe_allow_html=True)

# ===================================================
# ⚙️ 1. CONVENTIONS
# ===================================================

st.markdown("---")
st.markdown('## <span id="conventions">⚙️ 1. Conventions</span>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📈 Compounding")
    st.markdown("""
    - `ql.Simple`: $1 + r \times t$
    - `ql.Compounded`: $(1+r)^t$
    - `ql.Continuous`: $e^{r \times t}$
    - `ql.SimpleThenCompounded`
    - `ql.CompoundedThenSimple`
    """)

    st.markdown("### 🔄 Business Day Conventions")
    st.markdown("""
    - `ql.Following`: Next business day.
    - `ql.ModifiedFollowing`: Next business day, unless in next month (then previous).
    - `ql.Preceding`: Previous business day.
    - `ql.ModifiedPreceding`: Previous business day, unless in previous month (then next).
    - `ql.Unadjusted`: No change.
    """)

with col2:
    st.markdown("### ⏳ Frequencies")
    st.markdown("""
    - `ql.NoFrequency`: 0
    - `ql.Once`: 1
    - `ql.Annual`: 1
    - `ql.Semiannual`: 2
    - `ql.Quarterly`: 4
    - `ql.Bimonthly`: 6
    - `ql.Monthly`: 12
    - `ql.Daily`: 365
    """)

# ===================================================
# 📅 2. DATE
# ===================================================

st.markdown("---")
st.markdown('## <span id="date">📅 2. Date Class</span>', unsafe_allow_html=True)

st.markdown("""
### 🧠 QuantLib Dates
QuantLib handles dates using a serial number system similar to Excel (where 1 is 1899-12-31).
""")

col_d1, col_d2 = st.columns(2)

with col_d1:
    st.markdown("#### 🎮 Date Inspector")
    input_date = st.date_input("Select Date", datetime(2024, 6, 15))
    ql_date = ql.Date(input_date.day, input_date.month, input_date.year)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.write(f"**ISO Format:** `{ql_date.ISO()}`")
    st.write(f"**Weekday:** {ql_date.weekday()} (1=Sun, 7=Sat)")
    st.write(f"**Day of Year:** {ql_date.dayOfYear()}")
    st.write(f"**Serial Number:** {ql_date.serialNumber()}")
    st.write(f"**Is Leap Year?** {ql.Date.isLeap(ql_date.year())}")
    st.write(f"**Is End of Month?** {ql.Date.isEndOfMonth(ql_date)}")
    st.markdown('</div>', unsafe_allow_html=True)

with col_d2:
    st.markdown("#### 💻 Constructors & Static Functions")
    st.code("""
# Constructors
d = ql.Date(15, 6, 2024)
d = ql.Date('15-06-2024', '%d-%m-%Y')
d = ql.Date(45458) # Serial number

# Static Functions
today = ql.Date.todaysDate()
last_day = ql.Date.endOfMonth(d)
next_fri = ql.Date.nextWeekday(d, ql.Friday)
    """)

# ===================================================
# ⏳ 3. PERIOD
# ===================================================

st.markdown("---")
st.markdown('## <span id="period">⏳ 3. Period Class</span>', unsafe_allow_html=True)

st.markdown("""
Represents a time interval like "3 Months" or "10 Years".
""")

col_p1, col_p2 = st.columns(2)

with col_p1:
    p_n = st.number_input("Number", value=3, step=1, key="p_n")
    p_u = st.selectbox("Units", ["Days", "Weeks", "Months", "Years"], index=2)
    
    unit_map = {"Days": ql.Days, "Weeks": ql.Weeks, "Months": ql.Months, "Years": ql.Years}
    period = ql.Period(int(p_n), unit_map[p_u])
    
    st.success(f"Generated Period: **{period}**")

with col_p2:
    st.code("""
# Usage
p1 = ql.Period(3, ql.Months)
p2 = ql.Period('6M')
p3 = ql.Period(ql.Annual)

# Date Math
future_date = ql.Date(1,1,2024) + p1
    """)

# ===================================================
# 🗓️ 4. CALENDAR
# ===================================================

st.markdown("---")
st.markdown('## <span id="calendar">🗓️ 4. Calendar Class</span>', unsafe_allow_html=True)

st.markdown("""
Calendars define business days and holidays for specific countries or exchanges.
""")

cal_map = {
    "TARGET (Eurozone)": ql.TARGET(),
    "United States (Settlement)": ql.UnitedStates(ql.UnitedStates.Settlement),
    "United States (NYSE)": ql.UnitedStates(ql.UnitedStates.NYSE),
    "United Kingdom (Settlement)": ql.UnitedKingdom(),
    "China (SSE)": ql.China(ql.China.SSE),
    "India (NSE)": ql.India(),
    "Japan": ql.Japan()
}

selected_cal_name = st.selectbox("Select Calendar", list(cal_map.keys()))
cal = cal_map[selected_cal_name]

col_c1, col_c2 = st.columns(2)

with col_c1:
    test_date = st.date_input("Check if Business Day", datetime(2024, 1, 1), key="cal_date")
    t_ql = ql.Date(test_date.day, test_date.month, test_date.year)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    is_bd = cal.isBusinessDay(t_ql)
    if is_bd:
        st.success(f"✅ {t_ql} is a Business Day in {selected_cal_name}")
    else:
        st.error(f"🏖️ {t_ql} is a Holiday/Weekend in {selected_cal_name}")
    
    st.write(f"**Is Weekend?** {cal.isWeekend(t_ql.weekday())}")
    st.write(f"**End of Month BD:** {cal.endOfMonth(t_ql)}")
    st.markdown('</div>', unsafe_allow_html=True)

with col_c2:
    st.markdown("#### 💻 Useful Functions")
    st.code("""
cal = ql.UnitedStates(ql.UnitedStates.NYSE)
cal.isBusinessDay(d)
cal.addHoliday(ql.Date(20, 6, 2024))
cal.adjust(d, ql.Following)
new_d = cal.advance(d, ql.Period('2M'), ql.ModifiedFollowing)
    """)

# ===================================================
# 📏 5. DAYCOUNTER
# ===================================================

st.markdown("---")
st.markdown('## <span id="daycounter">📏 5. DayCounter Class</span>', unsafe_allow_html=True)

st.markdown("""
Day counters calculate the fraction of a year between two dates, critical for interest accrual.
""")

dc_map = {
    "Actual/360": ql.Actual360(),
    "Actual/365 Fixed": ql.Actual365Fixed(),
    "Actual/Actual (ISDA)": ql.ActualActual(ql.ActualActual.ISDA),
    "Thirty/360 (Bond Basis)": ql.Thirty360(ql.Thirty360.BondBasis),
    "Business/252": ql.Business252()
}

selected_dc_name = st.selectbox("Select Day Counter", list(dc_map.keys()))
dc = dc_map[selected_dc_name]

dc_d1 = st.date_input("Start Date", datetime(2024, 1, 1), key="dc_d1")
dc_d2 = st.date_input("End Date", datetime(2024, 12, 31), key="dc_d2")

q_d1 = ql.Date(dc_d1.day, dc_d1.month, dc_d1.year)
q_d2 = ql.Date(dc_d2.day, dc_d2.month, dc_d2.year)

yf = dc.yearFraction(q_d1, q_d2)
st.info(f"**Year Fraction ({selected_dc_name}):** {yf:.6f}")

# ===================================================
# 🗓️ 6. SCHEDULE
# ===================================================

st.markdown("---")
st.markdown('## <span id="schedule">🗓️ 6. Schedule Class</span>', unsafe_allow_html=True)

st.markdown("""
Generates a sequence of dates (e.g., for coupon payments).
""")

with st.expander("Show Schedule Parameters"):
    st.code("""
ql.Schedule(
    effectiveDate, terminationDate, tenor, calendar, 
    convention, terminationDateConvention, 
    rule, endOfMonth
)
    """)

# ===================================================
# 🛠️ 7. MAKESCHEDULE
# ===================================================

st.markdown("---")
st.markdown('## <span id="makeschedule">🛠️ 7. MakeSchedule Utility</span>', unsafe_allow_html=True)

col_s1, col_s2 = st.columns([1, 2])

with col_s1:
    s_start = st.date_input("Effective Date", datetime(2024, 1, 1), key="s_start")
    s_end = st.date_input("Termination Date", datetime(2026, 1, 1), key="s_end")
    s_tenor = st.selectbox("Tenor", ["3M", "6M", "1Y"], index=1)
    
    rule_map = {
        "Backward": ql.DateGeneration.Backward,
        "Forward": ql.DateGeneration.Forward,
        "ThirdWednesday": ql.DateGeneration.ThirdWednesday,
        "Zero": ql.DateGeneration.Zero
    }
    s_rule = st.selectbox("Rule", list(rule_map.keys()))

    q_s_start = ql.Date(s_start.day, s_start.month, s_start.year)
    q_s_end = ql.Date(s_end.day, s_end.month, s_end.year)
    
    schedule = ql.MakeSchedule(q_s_start, q_s_end, ql.Period(s_tenor), rule=rule_map[s_rule])

with col_s2:
    st.markdown("#### 📋 Generated Dates")
    dates = [d.ISO() for d in schedule]
    st.dataframe(pd.DataFrame({"Payment Date": dates}), use_container_width=True)

# ===================================================
# 🕸️ 8. TIMEGRID
# ===================================================

st.markdown("---")
st.markdown('## <span id="timegrid">🕸️ 8. TimeGrid Class</span>', unsafe_allow_html=True)

st.markdown("""
Used for numerical methods (like Monte Carlo or Finite Differences) to define time steps.
""")

tg_end = st.slider("Horizon (Years)", 1.0, 10.0, 5.0)
tg_steps = st.slider("Steps", 1, 100, 10)

tg = ql.TimeGrid(tg_end, tg_steps)
st.write("Grid Points:", [round(t, 4) for t in tg])

# ===================================================
# 📝 SUMMARY
# ===================================================

st.markdown("---")
st.info("""
💡 **Quant Insight**

Dates and Calendars are the foundation of all QuantLib instruments. 
- Use **Calendars** to handle local holidays.
- Use **DayCounters** for accruals.
- Use **Schedules** to link them into periodic payments.

👉 Miscalculating a single business day can lead to significant valuation errors in large portfolios!
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

nav_col1, nav_col2 = st.columns([1, 1])

with nav_col1:
    if st.button("⬅️ Previous: Currencies"):
        st.switch_page("pages/03_Currencies.py")

with nav_col2:
    if st.button("➡️ Next: Indexes"):
        st.switch_page("pages/05_Indexes.py")
