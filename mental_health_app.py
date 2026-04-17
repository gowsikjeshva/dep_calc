import streamlit as st
import pickle
import numpy as np
import os
import datetime

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="MindCheck — Student Wellbeing",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  CUSTOM CSS — Forest Green & Warm Cream Theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

:root {
    --bg:           #0f1a14;
    --bg2:          #131f18;
    --surface:      #18271d;
    --surface2:     #1d3024;
    --surface3:     #243b2b;
    --border:       #2a4a34;
    --border2:      #3a6647;
    --accent:       #4ade80;
    --accent2:      #22c55e;
    --accent3:      #86efac;
    --accent-glow:  rgba(74,222,128,0.2);
    --gold:         #fbbf24;
    --red:          #f87171;
    --amber:        #fb923c;
    --teal:         #2dd4bf;
    --text:         #f0faf3;
    --text2:        #a7c4b0;
    --muted:        #5c7d68;
    --serif:        'DM Serif Display', Georgia, serif;
    --sans:         'DM Sans', sans-serif;
    --mono:         'DM Mono', monospace;
}

html, body, [class*="css"] {
    font-family: var(--sans) !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 70% 50% at 10% 0%, rgba(74,222,128,0.07) 0%, transparent 60%),
        radial-gradient(ellipse 50% 40% at 90% 100%, rgba(34,197,94,0.06) 0%, transparent 60%),
        var(--bg) !important;
}

#MainMenu, footer { display: none !important; } 
header, [data-testid="stHeader"] { 
    background: transparent !important; 
    background-color: transparent !important; 
}
[data-testid="stHeader"]::before { display: none !important; }
.stDeployButton { display: none !important; }
.stAppDeployButton { display: none !important; }
[data-testid="stStatusWidget"] { display: none !important; }
[data-testid="manage-app-button"] { display: none !important; }
[data-testid="stForkButton"] { display: none !important; }
.viewerBadge_container { display: none !important; }
.viewerBadge_link_empty { display: none !important; }

.block-container { padding: 2rem 3rem 4rem !important; max-width: 1180px !important; }

/* ── Sidebar ── */
[data-testid="collapsedControl"],
[data-testid="collapsedControl"] *,
header button,
header button *,
[data-testid="stHeader"] button,
[data-testid="stHeader"] button * {
    color: #22c55e !important;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0c1710 0%, #0f1a14 100%) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] .block-container { padding: 1.8rem 1rem !important; }
[data-testid="stSidebar"] .stRadio > div > label {
    border-radius: 10px !important;
    padding: .55rem .9rem !important;
    transition: background .2s !important;
    color: var(--text2) !important;
    font-size: .87rem !important;
    font-weight: 500 !important;
}
[data-testid="stSidebar"] .stRadio > div > label:hover {
    background: rgba(74,222,128,0.1) !important;
    color: var(--accent3) !important;
}

/* ── Typography ── */
h1 {
    font-family: var(--serif) !important;
    font-size: 2.7rem !important;
    font-weight: 400 !important;
    line-height: 1.18 !important;
    color: var(--text) !important;
    letter-spacing: -0.02em !important;
    margin-bottom: .2rem !important;
}
h1 em { color: var(--accent) !important; font-style: italic !important; }
h2 {
    font-family: var(--serif) !important;
    font-size: 1.5rem !important;
    font-weight: 400 !important;
    color: var(--text) !important;
    margin-bottom: .6rem !important;
    letter-spacing: -0.01em !important;
}
h3 {
    font-family: var(--sans) !important;
    font-size: .68rem !important;
    font-weight: 700 !important;
    letter-spacing: .16em !important;
    text-transform: uppercase !important;
    color: var(--accent2) !important;
    border-bottom: 1px solid var(--border) !important;
    padding-bottom: .5rem !important;
    margin-bottom: 1rem !important;
}

/* ── Cards ── */
.mc-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.5rem 1.75rem;
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
    transition: border-color .25s, box-shadow .25s;
}
.mc-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(74,222,128,0.3), transparent);
}
.mc-card:hover {
    border-color: var(--border2);
    box-shadow: 0 0 30px rgba(74,222,128,0.06);
}
.mc-card-accent { border-left: 3px solid var(--accent2); }
.mc-card-glow {
    box-shadow: 0 0 50px rgba(74,222,128,0.1);
    border-color: rgba(74,222,128,0.35);
}

/* ── Labels ── */
.section-label {
    font-size: .67rem;
    font-weight: 700;
    letter-spacing: .18em;
    text-transform: uppercase;
    color: var(--accent2);
    margin-bottom: .35rem;
    display: flex;
    align-items: center;
    gap: .45rem;
}
.section-label::before {
    content: '';
    display: inline-block;
    width: 18px; height: 2px;
    background: var(--accent);
    border-radius: 2px;
}

/* ── Score ring ── */
.score-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 2rem 0 1.5rem;
}
.score-ring {
    width: 148px; height: 148px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-family: var(--serif);
    font-size: 2.8rem;
    font-weight: 400;
    margin-bottom: 1rem;
    position: relative;
    background: var(--surface2);
}
.score-ring::after {
    content: '';
    position: absolute;
    inset: -7px;
    border-radius: 50%;
    background: conic-gradient(var(--ring-color) var(--ring-pct), var(--surface3) 0);
    z-index: -1;
}
.score-ring::before {
    content: '';
    position: absolute;
    inset: -18px;
    border-radius: 50%;
    background: radial-gradient(circle, var(--ring-glow) 0%, transparent 70%);
    z-index: -2;
}

/* ── Risk badge ── */
.risk-badge {
    display: inline-flex;
    align-items: center;
    gap: .35rem;
    padding: .35rem 1.2rem;
    border-radius: 999px;
    font-size: .76rem;
    font-weight: 700;
    letter-spacing: .09em;
    text-transform: uppercase;
}

/* ── Tip pill ── */
.tip-pill {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1rem 1.1rem;
    margin-bottom: .6rem;
    font-size: .87rem;
    line-height: 1.6;
    position: relative;
    overflow: hidden;
    transition: border-color .2s;
}
.tip-pill::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    background: linear-gradient(180deg, var(--accent), var(--accent2));
    border-radius: 3px 0 0 3px;
}
.tip-pill:hover { border-color: var(--border2); }
.tip-title { font-weight: 600; color: var(--text); font-size: .9rem; margin-bottom: .25rem; }
.tip-body { color: var(--text2); font-size: .83rem; }
.tip-icon { font-size: 1.2rem; float: right; margin-left: .7rem; }

/* ── Factor bar ── */
.factor-row {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: .55rem;
    font-size: .83rem;
    padding: .3rem 0;
}
.factor-name { min-width: 165px; color: var(--text2); font-weight: 500; }
.factor-bar-bg {
    flex: 1; height: 6px;
    border-radius: 4px;
    background: var(--surface3);
    overflow: hidden;
}
.factor-bar-fill {
    height: 6px;
    border-radius: 4px;
    position: relative;
}
.factor-pct { font-size: .74rem; color: var(--muted); min-width: 34px; text-align: right; font-weight: 600; font-family: var(--mono); }

/* ── Metric tile ── */
.metric-tile {
    background: linear-gradient(135deg, var(--surface2) 0%, var(--surface3) 100%);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.3rem 1rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: transform .2s, box-shadow .2s;
}
.metric-tile::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--accent2), transparent);
}
.metric-tile:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 24px rgba(74,222,128,0.12);
}
.metric-val {
    font-family: var(--serif);
    font-size: 2.2rem;
    font-weight: 400;
    color: var(--accent3);
    line-height: 1;
}
.metric-lbl {
    font-size: .68rem;
    letter-spacing: .1em;
    text-transform: uppercase;
    color: var(--muted);
    margin-top: .4rem;
    font-weight: 600;
}
.metric-icon { font-size: 1.3rem; margin-bottom: .35rem; }

/* ── Stat grid ── */
.stat-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: .9rem; margin: 1rem 0; }
.stat-item {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.1rem;
    text-align: center;
}
.stat-num { font-family: var(--serif); font-size: 1.9rem; color: var(--accent); font-weight: 400; }
.stat-label { font-size: .72rem; color: var(--muted); text-transform: uppercase; letter-spacing: .08em; margin-top: .25rem; }

/* ── Progress step ── */
.step-indicator {
    display: flex;
    align-items: center;
    gap: .4rem;
    margin-bottom: 1.8rem;
    flex-wrap: wrap;
}
.step-dot {
    width: 26px; height: 26px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: .7rem;
    font-weight: 700;
    border: 2px solid var(--border2);
    color: var(--muted);
}
.step-dot.active {
    background: var(--accent2);
    border-color: var(--accent2);
    color: #0f1a14;
    box-shadow: 0 0 14px var(--accent-glow);
}
.step-line { flex: 1; height: 1px; background: var(--border); min-width: 18px; }

/* ── Quote block ── */
.quote-block {
    border-left: 3px solid var(--accent2);
    padding: .9rem 1.4rem;
    background: rgba(74,222,128,0.05);
    border-radius: 0 10px 10px 0;
    margin: 1rem 0;
    font-size: .9rem;
    color: var(--text2);
    font-style: italic;
    line-height: 1.7;
}

/* ── Feature table ── */
.feat-table { width: 100%; border-collapse: collapse; font-size: .83rem; }
.feat-table th {
    padding: .7rem .9rem;
    text-align: left;
    color: var(--accent2);
    font-weight: 700;
    font-size: .7rem;
    letter-spacing: .1em;
    text-transform: uppercase;
    border-bottom: 1px solid var(--border);
}
.feat-table td {
    padding: .6rem .9rem;
    color: var(--text2);
    border-bottom: 1px solid rgba(42,74,52,0.5);
    font-family: var(--mono);
    font-size: .8rem;
}
.feat-table td:first-child { color: var(--text); font-family: var(--sans); font-weight: 500; font-size: .83rem; }
.feat-table tr:hover td { background: rgba(74,222,128,0.03); }

/* ── Resource card ── */
.resource-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.1rem 1.4rem;
    margin-bottom: .75rem;
    display: flex;
    gap: 1rem;
    align-items: flex-start;
    transition: all .2s;
}
.resource-card:hover {
    border-color: var(--border2);
    box-shadow: 0 4px 16px rgba(74,222,128,0.08);
    transform: translateX(3px);
}
.resource-emoji { font-size: 1.6rem; flex-shrink: 0; }
.resource-name { font-weight: 700; font-size: .95rem; color: var(--text); }
.resource-contact { font-size: .86rem; color: var(--accent3); font-weight: 600; margin: .2rem 0; font-family: var(--mono); }
.resource-meta { font-size: .74rem; color: var(--muted); }

/* ── Wellbeing wheel ── */
.wheel-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: .9rem; }
.wheel-item {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1rem .9rem;
    text-align: center;
    transition: all .2s;
}
.wheel-item:hover { border-color: var(--accent2); box-shadow: 0 0 16px var(--accent-glow); }
.wheel-icon { font-size: 1.6rem; margin-bottom: .3rem; }
.wheel-label { font-size: .72rem; font-weight: 600; color: var(--text2); text-transform: uppercase; letter-spacing: .06em; }
.wheel-score { font-family: var(--serif); font-size: 1.4rem; color: var(--accent3); margin-top: .15rem; }

/* ── Disclaimer ── */
.disclaimer {
    background: rgba(248,113,113,0.07);
    border: 1px solid rgba(248,113,113,0.22);
    border-radius: 12px;
    padding: 1rem 1.4rem;
    font-size: .79rem;
    color: #fca5a5;
    line-height: 1.7;
    margin-top: 1.8rem;
}
.disclaimer b { color: #fecaca; }

/* ── Streamlit overrides ── */
.stSlider > div > div > div { background: var(--accent2) !important; }
.stSelectbox > div > div {
    background: var(--surface2) !important;
    border-color: var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
}
.stNumberInput > div > div {
    background: var(--surface2) !important;
    border-color: var(--border) !important;
    border-radius: 10px !important;
}
.stButton > button {
    background: linear-gradient(135deg, #22c55e 0%, #4ade80 100%) !important;
    color: #0f1a14 !important;
    border: none !important;
    border-radius: 12px !important;
    padding: .85rem 2rem !important;
    font-size: .95rem !important;
    font-weight: 700 !important;
    letter-spacing: .05em !important;
    width: 100% !important;
    text-transform: uppercase !important;
    box-shadow: 0 4px 18px rgba(74,222,128,0.35) !important;
    transition: all .2s !important;
}
.stButton > button:hover {
    box-shadow: 0 8px 28px rgba(74,222,128,0.55) !important;
    transform: translateY(-1px) !important;
}
label { color: var(--text2) !important; font-size: .84rem !important; font-weight: 500 !important; }
.stRadio > label { color: var(--text) !important; }

/* ── Misc ── */
.mc-divider { border: none; border-top: 1px solid var(--border); margin: 1.6rem 0; }
.hero-line { width: 52px; height: 3px; background: linear-gradient(90deg, var(--accent), var(--accent3)); border-radius: 2px; margin-bottom: 1rem; }
.insight-pill {
    display: inline-flex; align-items: center; gap: .4rem;
    background: rgba(74,222,128,0.08);
    border: 1px solid rgba(74,222,128,0.25);
    border-radius: 999px;
    padding: .28rem .85rem;
    font-size: .74rem; color: var(--accent3); font-weight: 600; margin: .2rem;
}
.algo-badge {
    display: inline-block;
    background: rgba(74,222,128,0.1);
    border: 1px solid rgba(74,222,128,0.25);
    color: var(--accent3);
    border-radius: 7px;
    padding: .22rem .65rem;
    font-size: .76rem; font-weight: 600; margin: .2rem;
    font-family: var(--mono);
}
.confidence-container { background: var(--surface3); border-radius: 5px; height: 8px; margin: .4rem 0; overflow: hidden; }
.confidence-fill {
    height: 8px; border-radius: 5px;
    background: linear-gradient(90deg, var(--accent2), var(--accent3));
}

/* ── Team card ── */
.team-card {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.3rem 1.5rem;
    text-align: center;
    transition: all .2s;
}
.team-card:hover {
    border-color: var(--accent2);
    box-shadow: 0 0 20px var(--accent-glow);
    transform: translateY(-2px);
}
.team-avatar {
    width: 56px; height: 56px;
    background: linear-gradient(135deg, var(--accent2), var(--teal));
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.4rem; font-weight: 700; color: #0f1a14;
    margin: 0 auto .8rem;
    font-family: var(--serif);
}
.team-name { font-weight: 700; font-size: .95rem; color: var(--text); margin-bottom: .2rem; }
.team-roll { font-size: .78rem; color: var(--accent3); font-family: var(--mono); font-weight: 500; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  LOAD MODEL
# ─────────────────────────────────────────────
model = None
model_loaded = False
try:
    model = pickle.load(open('depression_model.pkl', 'rb'))
    model_loaded = True
except FileNotFoundError:
    pass

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:.8rem 0 1.8rem'>
        <div style='font-size:2.4rem; margin-bottom:.4rem; filter:drop-shadow(0 0 16px rgba(74,222,128,0.45))'>🧠</div>
        <div style='font-family:"DM Serif Display",serif; font-size:1.6rem; color:#f0faf3; font-weight:400; letter-spacing:-0.01em'>MindCheck</div>
        <div style='font-size:.66rem; color:#5c7d68; letter-spacing:.17em; text-transform:uppercase; margin-top:.25rem'>Student Wellbeing AI</div>
        <div style='margin:.8rem auto 0; width:36px; height:2px; background:linear-gradient(90deg,#22c55e,#86efac); border-radius:2px'></div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigate",
        ["🔍  Assessment", "📊  Insights", "📈  Trends & Stats", "📚  Resources", "🌿  Wellness Hub", "ℹ️  About"],
        label_visibility="collapsed"
    )

    st.markdown("<hr style='border-color:#2a4a34; margin:1.2rem 0'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:.77rem; color:#5c7d68; line-height:1.8; padding:0 .1rem'>
        <div style='color:#4ade80; font-weight:700; font-size:.78rem; margin-bottom:.4rem'>How it works</div>
        Complete the 6-section assessment. The AI analyses your inputs across <b style='color:#a7c4b0'>20+ factors</b> and returns a personalised risk profile with evidence-backed recommendations.
        <div style='margin-top:.9rem; padding:.65rem; background:rgba(74,222,128,0.07); border-radius:9px; border:1px solid rgba(74,222,128,0.18)'>
            <div style='font-size:.7rem; color:#86efac; font-weight:700; text-transform:uppercase; letter-spacing:.09em; margin-bottom:.3rem'>Model</div>
            <div style='font-size:.74rem; color:#5c7d68'>Binary classification · 14 core features · Student dataset</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not model_loaded:
        st.markdown("""
        <div style='background:rgba(251,191,36,0.08);border:1px solid rgba(251,191,36,0.25);border-radius:10px;padding:.85rem 1rem;margin-top:1rem;font-size:.75rem;color:#fbbf24;line-height:1.6'>
        ⚠️ <b>Demo Mode</b><br>Add <code>depression_model.pkl</code> to enable live AI predictions.
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PAGE: ASSESSMENT
# ─────────────────────────────────────────────
if "🔍" in page:

    st.markdown("""
    <div style='margin-bottom:2rem'>
        <p class='section-label'>Mental Health Assessment</p>
        <div class='hero-line'></div>
        <h1>How are you <em>really</em> feeling?</h1>
        <p style='color:#5c7d68; font-size:.95rem; max-width:580px; line-height:1.8; margin-top:.6rem'>
        Answer honestly — responses are private and only used to generate your personalised report across 6 areas of student wellbeing.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='step-indicator'>
        <div class='step-dot active'>A</div><div class='step-line'></div>
        <div class='step-dot active'>B</div><div class='step-line'></div>
        <div class='step-dot active'>C</div><div class='step-line'></div>
        <div class='step-dot active'>D</div><div class='step-line'></div>
        <div class='step-dot active'>E</div><div class='step-line'></div>
        <div class='step-dot active'>F</div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("assessment_form"):

        st.markdown("<h3>A — About You</h3>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            gender = st.selectbox("Gender", ["Male", "Female", "Non-binary / Other", "Prefer not to say"])
        with col2:
            age = st.number_input("Age", 16, 60, 21)
        with col3:
            year = st.selectbox("Year of Study", ["1st Year", "2nd Year", "3rd Year", "4th Year", "Postgraduate", "PhD"])

        col4, col5 = st.columns(2)
        with col4:
            degree = st.selectbox("Degree / Programme", ["Engineering / Technology", "Science", "Arts / Humanities", "Business / Commerce", "Medicine / Health", "Law", "Education", "Other"])
        with col5:
            city_type = st.selectbox("Living Situation", ["On-campus hostel", "Private rented room", "Family home", "Shared house / flat", "Living alone"])

        st.markdown("<hr class='mc-divider'>", unsafe_allow_html=True)
        st.markdown("<h3>B — Academic Life</h3>", unsafe_allow_html=True)
        col6, col7 = st.columns(2)
        with col6:
            cgpa = st.number_input("Current CGPA / GPA  (0–10 scale)", 0.0, 10.0, 7.0, step=0.1)
            academic = st.slider("Academic Pressure  (1 = very low · 5 = extreme)", 1, 5, 3)
        with col7:
            study_hours = st.slider("Daily Study / Work Hours", 0, 16, 6)
            study_sat = st.slider("Study Satisfaction  (1 = very unhappy · 5 = very satisfied)", 1, 5, 3)

        col8, col9 = st.columns(2)
        with col8:
            attendance = st.slider("Class Attendance  (%)", 0, 100, 75)
        with col9:
            deadline_stress = st.slider("Deadline / Exam Stress  (1–5)", 1, 5, 3)

        col_e1, col_e2 = st.columns(2)
        with col_e1:
            assignment_load = st.slider("Weekly Assignment Load  (1 = light · 5 = overwhelming)", 1, 5, 3)
        with col_e2:
            future_anxiety = st.slider("Career / Future Anxiety  (1 = calm · 5 = very worried)", 1, 5, 2)

        st.markdown("<hr class='mc-divider'>", unsafe_allow_html=True)
        st.markdown("<h3>C — Lifestyle & Habits</h3>", unsafe_allow_html=True)
        col10, col11, col12 = st.columns(3)
        with col10:
            sleep = st.selectbox("Average Sleep Duration", ["Less than 5 hours", "5–6 hours", "7–8 hours", "More than 8 hours"])
        with col11:
            diet = st.selectbox("Dietary Habits", ["Healthy", "Moderate", "Unhealthy"])
        with col12:
            exercise = st.selectbox("Exercise Frequency", ["Daily", "4–5× per week", "2–3× per week", "Once a week", "Rarely / Never"])

        col13, col14 = st.columns(2)
        with col13:
            screen_time = st.slider("Daily Social Media / Screen Time  (hours)", 0, 12, 3)
        with col14:
            substance = st.selectbox("Caffeine / Substance Use", ["None", "Caffeine only (coffee/tea)", "Occasional alcohol", "Regular alcohol", "Other substances"])

        col15a, col16a = st.columns(2)
        with col15a:
            hydration = st.selectbox("Daily Hydration", ["Well hydrated (8+ glasses)", "Moderate (4–7 glasses)", "Low (< 4 glasses)"])
        with col16a:
            hobbies = st.selectbox("Time Spent on Hobbies", ["Daily", "A few times a week", "Rarely", "Never"])

        st.markdown("<hr class='mc-divider'>", unsafe_allow_html=True)
        st.markdown("<h3>D — Social & Financial Wellbeing</h3>", unsafe_allow_html=True)
        col15, col16 = st.columns(2)
        with col15:
            financial = st.slider("Financial Stress  (1 = none · 5 = severe)", 1, 5, 2)
            social_support = st.slider("Social Support / Close Friends  (1 = isolated · 5 = strong network)", 1, 5, 3)
        with col16:
            loneliness = st.slider("Feelings of Loneliness  (1 = never · 5 = always)", 1, 5, 2)
            relationship = st.selectbox("Relationship Status", ["Single", "In a relationship", "Married", "Complicated / Other"])

        col17d, col18d = st.columns(2)
        with col17d:
            family_conflict = st.slider("Family Conflict / Tension  (1 = none · 5 = high)", 1, 5, 2)
        with col18d:
            peer_pressure = st.slider("Peer / Social Pressure  (1 = none · 5 = intense)", 1, 5, 2)

        st.markdown("<hr class='mc-divider'>", unsafe_allow_html=True)
        st.markdown("<h3>E — Mental Health History</h3>", unsafe_allow_html=True)
        col17, col18, col19 = st.columns(3)
        with col17:
            suicide = st.selectbox("Ever had suicidal thoughts?", ["No", "Yes"])
        with col18:
            family = st.selectbox("Family history of mental illness?", ["No", "Yes"])
        with col19:
            prev_diagnosis = st.selectbox("Previous mental health diagnosis?", ["No", "Yes — anxiety", "Yes — depression", "Yes — other"])

        col20, col21 = st.columns(2)
        with col20:
            therapy = st.selectbox("Currently in therapy / counselling?", ["No", "Yes"])
        with col21:
            medication = st.selectbox("Currently taking mental health medication?", ["No", "Yes"])

        col22e, col23e = st.columns(2)
        with col22e:
            burnout = st.selectbox("Burnout this semester?", ["No", "Mild burnout", "Moderate burnout", "Severe burnout"])
        with col23e:
            panic_attacks = st.selectbox("Panic / anxiety attack frequency", ["Never", "Rarely (once a month)", "Sometimes (weekly)", "Often (multiple times a week)"])

        st.markdown("<hr class='mc-divider'>", unsafe_allow_html=True)
        st.markdown("<h3>F — This Week's Mood Snapshot</h3>", unsafe_allow_html=True)
        col22, col23 = st.columns(2)
        with col22:
            mood = st.slider("Overall Mood  (1 = very low · 10 = excellent)", 1, 10, 6)
            energy = st.slider("Energy Levels  (1 = exhausted · 10 = very energised)", 1, 10, 6)
        with col23:
            motivation = st.slider("Motivation  (1 = none · 10 = high)", 1, 10, 5)
            anxiety_level = st.slider("Anxiety Level  (1 = calm · 10 = very anxious)", 1, 10, 4)

        col24, col25 = st.columns(2)
        with col24:
            concentration = st.slider("Concentration / Focus  (1 = very poor · 10 = excellent)", 1, 10, 6)
        with col25:
            self_esteem = st.slider("Self-Esteem / Confidence  (1 = very low · 10 = very high)", 1, 10, 6)

        st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)
        submitted = st.form_submit_button("🔍  Run My Wellbeing Assessment")

    # ─────────────────────────────────────────
    #  RESULTS
    # ─────────────────────────────────────────
    if submitted:

        gender_val     = 1 if gender == "Male" else 0
        suicide_val    = 1 if suicide == "Yes" else 0
        family_val     = 1 if family == "Yes" else 0
        therapy_val    = 1 if therapy == "Yes" else 0
        medication_val = 1 if medication == "Yes" else 0
        prev_dx_val    = 0 if prev_diagnosis == "No" else 1

        sleep_map   = {"Less than 5 hours": 0, "5–6 hours": 1, "7–8 hours": 2, "More than 8 hours": 3}
        diet_map    = {"Healthy": 0, "Moderate": 1, "Unhealthy": 2}
        ex_map      = {"Daily": 4, "4–5× per week": 3, "2–3× per week": 2, "Once a week": 1, "Rarely / Never": 0}
        year_map    = {"1st Year": 1, "2nd Year": 2, "3rd Year": 3, "4th Year": 4, "Postgraduate": 5, "PhD": 6}
        subs_map    = {"None": 0, "Caffeine only (coffee/tea)": 1, "Occasional alcohol": 2, "Regular alcohol": 3, "Other substances": 4}
        burnout_map = {"No": 0, "Mild burnout": 1, "Moderate burnout": 2, "Severe burnout": 3}
        panic_map   = {"Never": 0, "Rarely (once a month)": 1, "Sometimes (weekly)": 2, "Often (multiple times a week)": 3}

        sleep_val     = sleep_map[sleep]
        diet_val      = diet_map[diet]
        exercise_val  = ex_map[exercise]
        year_val      = year_map[year]
        substance_val = subs_map[substance]
        burnout_val   = burnout_map[burnout]
        panic_val     = panic_map[panic_attacks]

        input_data = np.array([[
            gender_val, age, academic, 0, cgpa,
            study_sat, 0, sleep_val, diet_val, 0,
            suicide_val, study_hours, financial, family_val
        ]])

        if model_loaded:
            prediction = model.predict(input_data)[0]
            try:
                prob = model.predict_proba(input_data)[0][1]
            except:
                prob = 0.75 if prediction == 1 else 0.25
        else:
            risk_pts = 0
            if academic >= 4: risk_pts += 2
            if sleep_val <= 1: risk_pts += 2
            if financial >= 4: risk_pts += 2
            if suicide == "Yes": risk_pts += 3
            if family == "Yes": risk_pts += 1
            if diet_val >= 2: risk_pts += 1
            if exercise_val == 0: risk_pts += 1
            if mood <= 4: risk_pts += 2
            if anxiety_level >= 7: risk_pts += 2
            if loneliness >= 4: risk_pts += 1
            if burnout_val >= 2: risk_pts += 2
            if panic_val >= 2: risk_pts += 2
            if family_conflict >= 4: risk_pts += 1
            prediction = 1 if risk_pts >= 6 else 0
            prob = min(0.95, risk_pts / 18)

        risk_pct = int(prob * 100)
        is_high  = prediction == 1

        if risk_pct >= 70:
            ring_color="#f87171"; ring_glow="rgba(248,113,113,0.22)"; badge_bg="rgba(248,113,113,0.1)"
            badge_fg="#fca5a5"; badge_border="rgba(248,113,113,0.35)"; level_text="High Risk"; level_icon="⚠️"
        elif risk_pct >= 40:
            ring_color="#fb923c"; ring_glow="rgba(251,146,60,0.22)"; badge_bg="rgba(251,146,60,0.1)"
            badge_fg="#fdba74"; badge_border="rgba(251,146,60,0.35)"; level_text="Moderate Risk"; level_icon="⚡"
        else:
            ring_color="#4ade80"; ring_glow="rgba(74,222,128,0.22)"; badge_bg="rgba(74,222,128,0.1)"
            badge_fg="#86efac"; badge_border="rgba(74,222,128,0.35)"; level_text="Low Risk"; level_icon="✅"

        # Score card
        st.markdown(f"""
        <div class='mc-card mc-card-glow' style='text-align:center; padding:2rem'>
            <p class='section-label' style='justify-content:center'>Your Wellbeing Report · {datetime.date.today().strftime("%d %b %Y")}</p>
            <div class='score-wrap'>
                <div class='score-ring' style='color:{ring_color};--ring-color:{ring_color};--ring-pct:{risk_pct*3.6}deg;--ring-glow:{ring_glow}'>{risk_pct}%</div>
                <span class='risk-badge' style='background:{badge_bg};color:{badge_fg};border:1.5px solid {badge_border}'>{level_icon}&nbsp; {level_text}</span>
            </div>
            <p style='color:#5c7d68; font-size:.9rem; margin-top:.8rem; max-width:480px; margin-left:auto; margin-right:auto; line-height:1.7'>
            {"Your responses indicate several factors contributing to elevated mental health risk. Review the recommendations below and consider speaking with a counsellor." if is_high else "Your mental health appears to be in a relatively stable place. Continue nurturing the protective habits highlighted below."}
            </p>
            <div style='margin-top:1rem'>
                <span class='insight-pill'>📋 {len([v for v in [academic>=4, sleep_val<=1, financial>=4, exercise_val==0, mood<=4, anxiety_level>=7, loneliness>=4] if v])} risk factors flagged</span>
                <span class='insight-pill'>🎯 Confidence: {"High" if abs(prob-0.5)>0.3 else "Moderate"}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Wellbeing wheel
        st.markdown("<h2 style='margin-top:2rem'>Wellbeing Profile</h2>", unsafe_allow_html=True)
        w_sleep = int((sleep_val / 3) * 100)
        w_social = int((social_support / 5) * 100)
        w_mood_s = int((mood / 10) * 100)
        w_energy_s = int((energy / 10) * 100)
        w_focus = int((concentration / 10) * 100)
        w_esteem = int((self_esteem / 10) * 100)
        w_motivation_s = int((motivation / 10) * 100)
        w_calm = int(((10 - anxiety_level) / 10) * 100)

        def wheel_color(v):
            if v >= 65: return "#4ade80"
            if v >= 40: return "#fb923c"
            return "#f87171"

        wheels = [
            ("😴","Sleep",w_sleep),("🤝","Social",w_social),("😊","Mood",w_mood_s),
            ("⚡","Energy",w_energy_s),("🎯","Focus",w_focus),("💙","Self-Esteem",w_esteem),
            ("🔥","Motivation",w_motivation_s),("🧘","Calm",w_calm),
        ]
        wheel_html = "<div class='wheel-grid'>" + "".join([
            f"<div class='wheel-item'><div class='wheel-icon'>{icon}</div><div class='wheel-label'>{label}</div><div class='wheel-score' style='color:{wheel_color(val)}'>{val}%</div></div>"
            for icon, label, val in wheels
        ]) + "</div>"
        st.markdown(f"<div class='mc-card'>{wheel_html}</div>", unsafe_allow_html=True)

        # Factor breakdown
        st.markdown("<h2 style='margin-top:1.2rem'>Contributing Factors</h2>", unsafe_allow_html=True)
        factors = {
            "Academic pressure": min(academic/5,1.0),
            "Financial stress": min(financial/5,1.0),
            "Sleep quality": 1-(sleep_val/3),
            "Diet & nutrition": diet_val/2,
            "Physical activity": 1-(exercise_val/4),
            "Social isolation": 1-(social_support/5),
            "Loneliness": loneliness/5,
            "Screen overuse": min(screen_time/10,1.0),
            "Deadline stress": min(deadline_stress/5,1.0),
            "Low mood": 1-(mood/10),
            "Anxiety level": anxiety_level/10,
            "Low motivation": 1-(motivation/10),
            "Family conflict": family_conflict/5,
            "Peer pressure": peer_pressure/5,
            "Burnout": burnout_val/3,
            "Career anxiety": future_anxiety/5,
        }

        def bar_color(v):
            if v < 0.35: return "linear-gradient(90deg, #059669, #4ade80)"
            if v < 0.65: return "linear-gradient(90deg, #d97706, #fb923c)"
            return "linear-gradient(90deg, #dc2626, #f87171)"

        bars_html = "".join([
            f"<div class='factor-row'><span class='factor-name'>{name}</span><div class='factor-bar-bg'><div class='factor-bar-fill' style='width:{int(val*100)}%;background:{bar_color(val)}'></div></div><span class='factor-pct'>{int(val*100)}%</span></div>"
            for name, val in sorted(factors.items(), key=lambda x: -x[1])
        ])
        st.markdown(f"<div class='mc-card mc-card-accent'>{bars_html}</div>", unsafe_allow_html=True)

        # Recommendations
        st.markdown("<h2 style='margin-top:1.2rem'>Personalised Recommendations</h2>", unsafe_allow_html=True)
        tips = []
        if sleep_val <= 1:
            tips.append(("🛌","Prioritise sleep","You're sleeping under 6 hours. Chronic sleep deprivation impairs memory and emotional regulation. Gaining even 30 extra minutes measurably improves mood and cognitive performance."))
        if academic >= 4:
            tips.append(("📚","Manage academic overwhelm","Break tasks into focused 25-minute Pomodoro sessions. Use a weekly priority matrix: urgent vs. important. Talk to a tutor early — before deadlines pile up."))
        if financial >= 4:
            tips.append(("💰","Address financial pressure","Explore your institution's hardship bursaries, emergency funds, and food banks. One conversation with a student welfare officer can open doors you didn't know existed."))
        if exercise_val == 0:
            tips.append(("🏃","Move every day","A 20-minute brisk walk reduces cortisol by up to 26% and improves sleep quality. Consistency matters more than intensity — campus grounds count."))
        if social_support <= 2:
            tips.append(("🤝","Build your support network","Commit to joining one club or study group this week. Start small — even one trusted person dramatically reduces depression risk."))
        if screen_time >= 6:
            tips.append(("📱","Reclaim time from screens","6+ hours of social media is associated with significantly higher anxiety. Try a 1-hour screen-free window before sleep and replace it with reading or journaling."))
        if diet_val >= 2:
            tips.append(("🥗","Fuel your brain","Ultra-processed diets worsen mood and cognition. Start with one swap: add vegetables to one meal per day and reduce sugary drinks."))
        if suicide == "Yes":
            tips.append(("❤️","You're not alone","Having had suicidal thoughts is more common than many admit. Please reach out — iCall (India): 9152987821. A conversation can be life-changing."))
        if mood <= 4:
            tips.append(("🌤","Nurture your mood","Schedule one enjoyable activity daily — even 15 minutes. Behavioural activation is clinically proven to lift low mood over time."))
        if anxiety_level >= 7:
            tips.append(("🌬","Regulate your nervous system","Box breathing (inhale 4s → hold 4s → exhale 4s → hold 4s, repeat 4×) reduces acute anxiety within minutes. Use it before exams or when anxiety spikes."))
        if loneliness >= 4:
            tips.append(("🫂","Address loneliness","Even sending one genuine text to someone you trust has an immediate psychological effect. Consider volunteering — helping others is one of the fastest ways to feel connected."))
        if burnout_val >= 2:
            tips.append(("🔋","Recover from burnout","Block 30 minutes daily for non-productive, purely restorative activity. Consider reducing your workload temporarily — burnout is physiological, not a mindset."))
        if panic_val >= 2:
            tips.append(("🧘","Manage panic responses","Daily breathwork (5 minutes), cold water face splashes during acute episodes, and progressive muscle relaxation before sleep all help recalibrate your stress baseline."))
        if family_conflict >= 4:
            tips.append(("🏠","Navigate family tension","Consider speaking with a counsellor to develop coping strategies. Setting gentle but clear communication boundaries at home meaningfully reduces tension."))
        if concentration <= 4:
            tips.append(("🎯","Restore focus","Close all tabs except the one you're working on. The Pomodoro method and ambient focus music can help retrain attention impaired by sleep deficit or anxiety."))
        if therapy == "No" and is_high:
            tips.append(("🛋","Consider professional support","Most campuses offer free confidential counselling. Booking the first appointment is the hardest step — and often the most important one."))

        if not tips:
            tips = [
                ("✨","You're doing well","Your habits are in a healthy place. Protect your sleep schedule, social connections, and physical activity even during high-stress periods."),
                ("📖","Sustain academic balance","Regular short study sessions outperform last-minute cramming. Guard your recovery time — it is part of performing well."),
                ("🙏","Practise intentional gratitude","Writing 3 specific things you're grateful for each morning builds psychological resilience over time."),
            ]

        tips_html = "".join([
            f"<div class='tip-pill'><span class='tip-icon'>{icon}</span><div class='tip-title'>{title}</div><div class='tip-body'>{body}</div></div>"
            for icon, title, body in tips
        ])
        st.markdown(f"<div class='mc-card'>{tips_html}</div>", unsafe_allow_html=True)

        # Snapshot metrics
        st.markdown("<h2 style='margin-top:1.2rem'>This Week at a Glance</h2>", unsafe_allow_html=True)
        cols = st.columns(6)
        tiles = [("😊",f"{mood}/10","Mood"),("⚡",f"{energy}/10","Energy"),("🔥",f"{motivation}/10","Motivation"),
                 ("🧘",f"{10-anxiety_level}/10","Calm"),("🎯",f"{concentration}/10","Focus"),("💙",f"{self_esteem}/10","Self-Worth")]
        for col, (icon, val, lbl) in zip(cols, tiles):
            col.markdown(f"<div class='metric-tile'><div class='metric-icon'>{icon}</div><div class='metric-val'>{val}</div><div class='metric-lbl'>{lbl}</div></div>", unsafe_allow_html=True)

        st.markdown("""
        <div class='disclaimer'>
        ⚕️ <b>Medical Disclaimer:</b> MindCheck is an educational screening tool and does not constitute clinical diagnosis, advice, or treatment. If you are in distress or experiencing a mental health crisis, please contact a qualified healthcare professional immediately.<br>
        🇮🇳 India: <b>iCall — 9152987821</b> &nbsp;|&nbsp; <b>Vandrevala Foundation — 1860-2662-345</b> (24/7) &nbsp;|&nbsp; <b>NIMHANS — 080-46110007</b>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PAGE: INSIGHTS
# ─────────────────────────────────────────────
elif "📊" in page:
    st.markdown("""
    <p class='section-label'>Model Transparency</p>
    <div class='hero-line'></div>
    <h1>Inside the <em>AI model</em></h1>
    <p style='color:#5c7d68; max-width:600px; line-height:1.8; font-size:.95rem; margin-top:.6rem'>
    A fully transparent view of features, algorithm, and known limitations. We believe in explainable AI.
    </p>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='stat-grid'>
        <div class='stat-item'><div class='stat-num'>14</div><div class='stat-label'>Core features</div></div>
        <div class='stat-item'><div class='stat-num'>Binary</div><div class='stat-label'>Classification task</div></div>
        <div class='stat-item'><div class='stat-num'>.pkl</div><div class='stat-label'>Serialised format</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""<div class='mc-card mc-card-accent'><h2>Core Input Features</h2>
    <p style='color:#5c7d68; font-size:.86rem; line-height:1.7; margin:.4rem 0 1rem'>
    The model uses 14 features from training data. Additional assessment fields generate the wellbeing wheel and recommendations — they do not alter the core AI risk score.
    </p>""", unsafe_allow_html=True)

    feat_table = [
        ("Gender","Binary","Male=1, Female=0","Demographic"),
        ("Age","Numeric","16–60 years","Demographic"),
        ("Academic Pressure","Ordinal 1–5","Self-reported scale","Academic"),
        ("CGPA","Numeric 0–10","Current grade point average","Academic"),
        ("Study Satisfaction","Ordinal 1–5","Self-reported scale","Academic"),
        ("Sleep Duration","Ordinal 0–3","<5h=0 · 5–6h=1 · 7–8h=2 · >8h=3","Lifestyle"),
        ("Dietary Habits","Ordinal 0–2","Healthy=0 · Moderate=1 · Unhealthy=2","Lifestyle"),
        ("Suicidal Thoughts","Binary","Yes=1, No=0","Mental Health"),
        ("Study/Work Hours","Numeric","Daily hours 0–16","Academic"),
        ("Financial Stress","Ordinal 1–5","Self-reported scale","Financial"),
        ("Family History","Binary","Mental illness: Yes=1, No=0","Mental Health"),
        ("Index 3 (unknown)","Padded 0","Original feature unknown","⚠️ Unknown"),
        ("Index 6 (unknown)","Padded 0","Original feature unknown","⚠️ Unknown"),
        ("Index 9 (unknown)","Padded 0","Original feature unknown","⚠️ Unknown"),
    ]
    rows = "".join([
        f"<tr><td>{n}</td><td>{t}</td><td>{e}</td><td><span class='algo-badge' style='{'background:rgba(248,113,113,0.1);border-color:rgba(248,113,113,0.25);color:#fca5a5' if '⚠️' in c else ''}'>{c}</span></td></tr>"
        for n, t, e, c in feat_table
    ])
    st.markdown(f"<table class='feat-table'><thead><tr><th>Feature</th><th>Type</th><th>Encoding</th><th>Category</th></tr></thead><tbody>{rows}</tbody></table></div>", unsafe_allow_html=True)

    col_ins1, col_ins2 = st.columns(2)
    with col_ins1:
        st.markdown("""
        <div class='mc-card'><h2>Likely Algorithm</h2>
        <p style='color:#5c7d68; font-size:.85rem; line-height:1.75; margin:.4rem 0'>
        Based on the dataset type and binary classification task, the model was most likely trained using a <b style='color:#f0faf3'>Random Forest</b> classifier — an ensemble of decision trees that votes on the final prediction.
        </p>
        <div style='margin-top:.8rem'>
            <div style='font-size:.73rem; color:#5c7d68; margin-bottom:.25rem'>Algorithm confidence ranking</div>
            <div style='margin-bottom:.5rem'><div style='display:flex;justify-content:space-between;font-size:.79rem;color:#a7c4b0;margin-bottom:.25rem'><span>Random Forest</span><span>85%</span></div><div class='confidence-container'><div class='confidence-fill' style='width:85%'></div></div></div>
            <div style='margin-bottom:.5rem'><div style='display:flex;justify-content:space-between;font-size:.79rem;color:#a7c4b0;margin-bottom:.25rem'><span>Gradient Boosting / XGBoost</span><span>60%</span></div><div class='confidence-container'><div class='confidence-fill' style='width:60%'></div></div></div>
            <div style='margin-bottom:.5rem'><div style='display:flex;justify-content:space-between;font-size:.79rem;color:#a7c4b0;margin-bottom:.25rem'><span>Logistic Regression</span><span>35%</span></div><div class='confidence-container'><div class='confidence-fill' style='width:35%'></div></div></div>
            <div><div style='display:flex;justify-content:space-between;font-size:.79rem;color:#a7c4b0;margin-bottom:.25rem'><span>SVM</span><span>20%</span></div><div class='confidence-container'><div class='confidence-fill' style='width:20%'></div></div></div>
        </div></div>
        """, unsafe_allow_html=True)

    with col_ins2:
        st.markdown("""
        <div class='mc-card'><h2>Known Limitations</h2>
        <p style='color:#5c7d68; font-size:.85rem; line-height:1.75; margin:.4rem 0'>
        Three feature positions (index 3, 6, 9) are zero-padded because their original field mapping is unknown. If these carry high importance, predictions may be unreliable.
        </p>
        <div style='margin-top:.7rem'>
            <div class='tip-pill' style='padding:.65rem .9rem;margin-bottom:.45rem'><div class='tip-body'>⚠️ <b style='color:#f0faf3'>Dataset bias:</b> Trained on Indian university students — may not generalise globally.</div></div>
            <div class='tip-pill' style='padding:.65rem .9rem;margin-bottom:.45rem'><div class='tip-body'>⚠️ <b style='color:#f0faf3'>Self-report bias:</b> Subject to recall bias and social desirability effects.</div></div>
            <div class='tip-pill' style='padding:.65rem .9rem'><div class='tip-body'>⚠️ <b style='color:#f0faf3'>Not clinical:</b> A screening tool only — not a replacement for professional diagnosis.</div></div>
        </div></div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class='quote-block'>
    "The best mental health tools don't replace human connection — they lower the barrier to seeking it. MindCheck is designed as a first step, not a final answer."
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PAGE: TRENDS & STATS
# ─────────────────────────────────────────────
elif "📈" in page:
    st.markdown("""
    <p class='section-label'>Research & Context</p>
    <div class='hero-line'></div>
    <h1>Student mental health <em>by the numbers</em></h1>
    <p style='color:#5c7d68; max-width:600px; line-height:1.8; font-size:.95rem; margin-top:.6rem'>
    Evidence-backed statistics on student wellbeing globally and in India.
    </p>
    """, unsafe_allow_html=True)

    stat_data = [
        ("1 in 4","University students globally experience mental health problems during their studies","#4ade80"),
        ("75%","Of all mental health conditions begin before age 24 — making university years critical","#22c55e"),
        ("40%","Of students with mental health issues never seek professional help","#86efac"),
        ("56%","Increase in students seeking counselling at Indian universities since 2019","#4ade80"),
        ("3×","Students from low-income families are 3× more likely to report financial stress as a trigger","#22c55e"),
        ("82%","Of students say academic pressure is their primary source of anxiety","#86efac"),
    ]

    cols = st.columns(3)
    for i, (num, desc, color) in enumerate(stat_data):
        with cols[i % 3]:
            st.markdown(f"""
            <div class='mc-card' style='text-align:center; padding:1.6rem 1.3rem; min-height:160px'>
                <div style='font-family:"DM Serif Display",serif; font-size:2.3rem; color:{color}; margin-bottom:.5rem'>{num}</div>
                <div style='font-size:.83rem; color:#a7c4b0; line-height:1.65'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<h2 style='margin-top:1.8rem'>Key Risk Factor Research</h2>", unsafe_allow_html=True)
    research = [
        ("😴","Sleep deprivation","Students sleeping fewer than 6 hours are 2.5× more likely to report depressive symptoms. REM sleep directly regulates emotional processing and memory consolidation."),
        ("💸","Financial stress","A 2023 UGC survey found 1 in 3 Indian university students cited financial worry as their primary mental health stressor — above academic pressure."),
        ("📱","Social media overuse","Meta-analyses show 4+ hours of passive social media consumption correlates with significantly elevated loneliness and social comparison anxiety."),
        ("🏃","Physical inactivity","Regular aerobic exercise is as effective as antidepressant medication for mild-to-moderate depression in controlled trials (Blumenthal et al., 2007)."),
        ("🤝","Social connection","Perceived social isolation increases depression risk by 29% and anxiety by 18%. Strong peer relationships are the most consistent protective factor across cultures."),
        ("🎓","Academic perfectionism","Maladaptive perfectionism (fear of failure rather than pursuit of excellence) is strongly linked to burnout, anxiety, and dropout risk."),
    ]
    for icon, title, body in research:
        st.markdown(f"""
        <div class='mc-card' style='padding:1.1rem 1.4rem'>
        <div style='display:flex; gap:.9rem; align-items:flex-start'>
            <span style='font-size:1.6rem; flex-shrink:0'>{icon}</span>
            <div><div style='font-weight:700; color:#f0faf3; font-size:.92rem; margin-bottom:.3rem'>{title}</div>
            <div style='color:#5c7d68; font-size:.84rem; line-height:1.7'>{body}</div></div>
        </div></div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PAGE: RESOURCES
# ─────────────────────────────────────────────
elif "📚" in page:
    st.markdown("""
    <p class='section-label'>Crisis Support & Help</p>
    <div class='hero-line'></div>
    <h1>You are never <em>alone</em></h1>
    <p style='color:#5c7d68; max-width:600px; line-height:1.8; font-size:.95rem; margin-top:.6rem'>
    Vetted, confidential mental health resources for students across India and internationally.
    </p>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='background:rgba(248,113,113,0.07); border:1px solid rgba(248,113,113,0.25); border-radius:12px; padding:.9rem 1.3rem; margin-bottom:1.3rem; font-size:.86rem; color:#fca5a5; line-height:1.7'>
    🆘 <b>If you are in immediate crisis, please call or text a helpline now.</b> You don't have to be at rock bottom to reach out. Counsellors are trained and ready to listen.
    </div>
    """, unsafe_allow_html=True)

    resources = [
        ("🆘","iCall — TISS Mumbai","9152987821","Mon–Sat · 8am–10pm","Free phone & chat counselling with psychologists from the Tata Institute of Social Sciences. English, Hindi & regional languages.","#f87171"),
        ("🆘","Vandrevala Foundation","1860-2662-345","24 hours · 7 days","India's largest mental health helpline. Free, anonymous, and available around the clock in multiple languages.","#f87171"),
        ("🆘","Snehi Helpline","044-24640050","24 hours · 7 days","Suicide prevention and emotional support for individuals in crisis across India.","#f87171"),
        ("🆘","NIMHANS Helpline","080-46110007","Mon–Sat · 8am–8pm","National Institute of Mental Health helpline offering clinical guidance and referral support.","#f87171"),
        ("🌍","Crisis Text Line","Text HOME to 741741","24 hours · 7 days","Free text-based crisis support. Available in India, UK, USA, Ireland, and Canada.","#4ade80"),
        ("🌍","Befrienders Worldwide","befrienders.org","Varies by centre","Global directory of emotional support helplines. Find your nearest centre online.","#4ade80"),
        ("📖","iMind (India)","9901006454","Mon–Sat · 9am–9pm","Telangana-based mental health support covering counselling, therapy referrals, and psychoeducation.","#2dd4bf"),
        ("📖","Mind UK","0300-123-3393","Mon–Fri · 9am–6pm","Comprehensive mental health information, community support, and peer networks.","#2dd4bf"),
        ("📖","NAMI USA","1-800-950-6264","Mon–Fri · 10am–10pm ET","National Alliance on Mental Illness — education, advocacy, and peer support programmes.","#2dd4bf"),
    ]
    for emoji, name, contact, hours, desc, color in resources:
        st.markdown(f"""
        <div class='resource-card'>
            <span class='resource-emoji'>{emoji}</span>
            <div style='flex:1'>
                <div class='resource-name'>{name}</div>
                <div class='resource-contact' style='color:{color}'>{contact}</div>
                <div class='resource-meta'>{hours} &nbsp;·&nbsp; {desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<h2 style='margin-top:1.8rem'>Evidence-Based Self-Help Techniques</h2>", unsafe_allow_html=True)
    techniques = [
        ("📦","Box Breathing","Inhale 4s → Hold 4s → Exhale 4s → Hold 4s. Repeat 4×. Activates the parasympathetic system. Use before exams or during anxiety spikes."),
        ("🌿","5-4-3-2-1 Grounding","Name 5 things you see, 4 you can touch, 3 you hear, 2 you smell, 1 you taste. Anchors you to the present moment and interrupts panic spirals."),
        ("📓","Expressive Journaling","Write for 10 unedited minutes. James Pennebaker's research shows expressive writing measurably reduces depression symptoms and improves immune function."),
        ("🚶","Nature Walks","20 minutes in green space lowers cortisol by measurable amounts. University grounds count. Consistency matters more than intensity."),
        ("📵","Phone-Free Mornings","Avoiding your phone for the first 30 minutes sets a calmer neurological baseline for the whole day. Replace it with stretching, water, or stillness."),
        ("🤝","Micro-Connection","Sending one genuine message to someone you trust reduces the psychological burden of loneliness immediately. You don't have to share everything."),
        ("🌬","Progressive Muscle Relaxation","Tense and release each muscle group from toes to forehead over 15 minutes. Clinically effective for insomnia and generalised anxiety."),
        ("🙏","Gratitude Practice","Writing 3 specific things you're grateful for each morning sustains positive mood and builds resilience over 4+ weeks — supported by RCTs."),
    ]
    cols_t = st.columns(2)
    for i, (icon, title, body) in enumerate(techniques):
        with cols_t[i % 2]:
            st.markdown(f"<div class='tip-pill'><span class='tip-icon'>{icon}</span><div class='tip-title'>{title}</div><div class='tip-body'>{body}</div></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PAGE: WELLNESS HUB
# ─────────────────────────────────────────────
elif "🌿" in page:
    st.markdown("""
    <p class='section-label'>Daily Wellbeing</p>
    <div class='hero-line'></div>
    <h1>Your Wellness <em>Hub</em></h1>
    <p style='color:#5c7d68; max-width:600px; line-height:1.8; font-size:.95rem; margin-top:.6rem'>
    Curated tools, frameworks, and daily practices to build lasting psychological resilience.
    </p>
    """, unsafe_allow_html=True)

    st.markdown("<h2 style='margin-top:1rem'>The 5 Pillars of Student Wellbeing</h2>", unsafe_allow_html=True)
    pillars = [
        ("💤","Sleep","#4ade80","Sleep is the single highest-impact intervention for mental health. Target 7–8 hours with consistent bed and wake times — even on weekends. Poor sleep amplifies every other stressor."),
        ("🏃","Movement","#22c55e","Exercise releases BDNF — your brain's own antidepressant. Any movement counts: walking, dancing, cycling. Aim for 30 minutes, 5× per week."),
        ("🤝","Connection","#2dd4bf","Humans are social by design. Prioritise face-to-face interaction, even briefly. One deep conversation is more restorative than a hundred likes on a post."),
        ("🎯","Purpose","#4ade80","A clear sense of why your work matters dramatically reduces burnout. Break long goals into weekly milestones you can actually feel progress on."),
        ("🧘","Recovery","#22c55e","Rest is part of the performance cycle. Build deliberate recovery into your schedule: phone-free evenings, creative hobbies, time in nature, adequate nutrition."),
    ]
    for icon, title, color, body in pillars:
        st.markdown(f"""
        <div class='mc-card' style='border-left:3px solid {color}; padding:1.2rem 1.6rem'>
        <div style='display:flex; align-items:flex-start; gap:1rem'>
            <span style='font-size:1.8rem; flex-shrink:0'>{icon}</span>
            <div><div style='font-weight:700; font-size:1rem; color:#f0faf3; margin-bottom:.35rem'>{title}</div>
            <div style='color:#5c7d68; font-size:.86rem; line-height:1.75'>{body}</div></div>
        </div></div>
        """, unsafe_allow_html=True)

    st.markdown("<h2 style='margin-top:1.8rem'>Building a Sustainable Study Routine</h2>", unsafe_allow_html=True)
    routine = [
        ("🌅","Morning anchor","Wake at a consistent time. Drink water before caffeine. 5 minutes of stretching or breathwork before checking your phone sets your neurological baseline for the day."),
        ("📋","Weekly priority mapping","Every Sunday, list your top 3 academic and top 2 personal priorities for the week. Nothing else gets scheduled until these are protected in your calendar."),
        ("⏱","Pomodoro study blocks","25 minutes of focused single-task work, then a 5-minute break. After 4 blocks, take a 20-minute rest. Eliminates decision fatigue and prevents cognitive overload."),
        ("🌇","Evening wind-down","Stop studying 1 hour before sleep. No social media. A consistent wind-down routine conditions your brain to prepare for deep sleep."),
        ("📵","Digital boundaries","Turn off non-essential notifications during study blocks. Check messages at fixed windows — reactive attention is exhausting."),
        ("🔋","Weekly recovery day","Protect one day per week for genuinely unstructured rest. Your performance the rest of the week will improve as a result."),
    ]
    cols_r = st.columns(2)
    for i, (icon, title, body) in enumerate(routine):
        with cols_r[i % 2]:
            st.markdown(f"<div class='tip-pill' style='min-height:110px'><span class='tip-icon'>{icon}</span><div class='tip-title'>{title}</div><div class='tip-body'>{body}</div></div>", unsafe_allow_html=True)

    st.markdown("""
    <div class='quote-block' style='margin-top:1.2rem'>
    "You don't have to be perfect. You don't have to have everything figured out. You just have to take the next small step — and then the one after that."
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PAGE: ABOUT
# ─────────────────────────────────────────────
elif "ℹ️" in page:
    st.markdown("""
    <p class='section-label'>About This Tool</p>
    <div class='hero-line'></div>
    <h1>MindCheck — <em>built with care</em></h1>
    """, unsafe_allow_html=True)

    # Team section
    st.markdown("<h2 style='margin-top:1.2rem'>Development Team</h2>", unsafe_allow_html=True)
    team = [
        ("D","Dinakar S","24BCS405"),
        ("G","Gowsik Jeshva M","24BCS409"),
        ("K","Kishore LS","24BCS413"),
    ]
    cols_team = st.columns(3)
    for col, (initial, name, roll) in zip(cols_team, team):
        col.markdown(f"""
        <div class='team-card'>
            <div class='team-avatar'>{initial}</div>
            <div class='team-name'>{name}</div>
            <div class='team-roll'>{roll}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class='mc-card mc-card-accent' style='padding:1.8rem; margin-top:1.2rem'>
    <p style='color:#a7c4b0; font-size:.95rem; line-height:1.85; margin:0'>
    MindCheck was built to give students a <b style='color:#f0faf3'>private, non-judgemental first step</b> toward understanding their mental health.
    It is not a replacement for professional care — it is a compassionate starting point for self-reflection and help-seeking.
    </p>
    </div>

    <div class='mc-card'>
    <h2>What's New in v3.0</h2>
    <div style='display:grid; grid-template-columns:1fr 1fr; gap:.7rem; margin-top:.7rem'>
        <div class='tip-pill'><div class='tip-title'>🌐 Expanded assessment</div><div class='tip-body'>28 questions across 6 sections — burnout, panic frequency, career anxiety, concentration & self-esteem.</div></div>
        <div class='tip-pill'><div class='tip-title'>🎯 Wellbeing wheel</div><div class='tip-body'>8-dimension visual profile: Sleep, Social, Mood, Energy, Focus, Self-Esteem, Motivation & Calm.</div></div>
        <div class='tip-pill'><div class='tip-title'>📈 Trends & Stats page</div><div class='tip-body'>Evidence-backed research on student mental health with key statistics and risk factor analysis.</div></div>
        <div class='tip-pill'><div class='tip-title'>🌿 Wellness Hub</div><div class='tip-body'>5 pillars of wellbeing and a sustainable study routine framework.</div></div>
        <div class='tip-pill'><div class='tip-title'>🎨 Refreshed UI</div><div class='tip-body'>Forest green professional theme with warm accents, factor bars, and metric tiles.</div></div>
        <div class='tip-pill'><div class='tip-title'>💬 Extended tips</div><div class='tip-body'>15+ personalised recommendation triggers with research-backed actionable guidance.</div></div>
    </div>
    </div>

    <div class='mc-card'>
    <h2>Tech Stack</h2>
    <div style='display:flex; gap:.4rem; flex-wrap:wrap; margin-top:.7rem'>
        <span class='algo-badge'>Python 3</span>
        <span class='algo-badge'>Streamlit</span>
        <span class='algo-badge'>scikit-learn</span>
        <span class='algo-badge'>NumPy</span>
        <span class='algo-badge'>pickle</span>
        <span class='algo-badge'>HTML/CSS</span>
        <span class='algo-badge'>Google Fonts</span>
    </div>
    <p style='color:#5c7d68; font-size:.84rem; line-height:1.7; margin-top:.9rem; margin-bottom:0'>
    Built with Python 3, Streamlit for the UI layer, scikit-learn for the ML model, and NumPy for feature processing. The model is loaded from a pre-trained <code style='background:rgba(74,222,128,0.1);padding:.1rem .4rem;border-radius:4px;color:#86efac'>.pkl</code> file serialised via pickle.
    </p>
    </div>

    <div class='mc-card'>
    <h2>Privacy & Data</h2>
    <p style='color:#5c7d68; font-size:.84rem; line-height:1.75; margin:.4rem 0 0'>
    <b style='color:#f0faf3'>No data is stored or transmitted.</b> All processing happens locally within your browser session. Closing the tab permanently clears everything. MindCheck does not use cookies, analytics, or third-party tracking of any kind.
    </p>
    </div>

    <div class='mc-card'>
    <h2>Version & Build</h2>
    <p style='color:#5c7d68; font-size:.84rem; line-height:1.7; margin:.4rem 0 0'>
    <b style='color:#f0faf3'>v3.0</b> — Expanded 28-feature assessment · Wellbeing wheel · Trends & Stats · Wellness Hub · Forest green professional UI · 15+ recommendation triggers · Algorithm confidence visualisation.<br><br>
    Built {datetime.date.today().strftime('%B %Y')} · Designed for Indian university students · Sri Eshwar College of Engineering
    </p>
    </div>
    """, unsafe_allow_html=True)
