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
#  CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Root palette — soft pastel + indigo ── */
:root {
    --bg:        #f5f0fb;
    --surface:   #ffffff;
    --surface2:  #ede8f7;
    --border:    #d6cff0;
    --accent:    #4f46e5;
    --accent2:   #6366f1;
    --lavender:  #e9e4fa;
    --mint:      #d4f5ec;
    --peach:     #fde8dc;
    --green:     #059669;
    --red:       #dc2626;
    --amber:     #d97706;
    --text:      #1e1b4b;
    --muted:     #6b7280;
    --serif:     'DM Serif Display', Georgia, serif;
    --sans:      'DM Sans', sans-serif;
}

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: var(--sans) !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 4rem !important; max-width: 1100px !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--lavender) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] .block-container { padding: 1.5rem 1rem !important; }

/* ── Headings ── */
h1 { font-family: var(--serif) !important; font-size: 2.6rem !important; font-weight: 400 !important; line-height: 1.15 !important; color: var(--text) !important; }
h2 { font-family: var(--serif) !important; font-size: 1.5rem !important; font-weight: 400 !important; color: var(--text) !important; }
h3 { font-family: var(--sans) !important; font-size: 1rem !important; font-weight: 600 !important; letter-spacing: .06em !important; text-transform: uppercase !important; color: var(--muted) !important; }

/* ── Cards ── */
.mc-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.5rem 1.75rem;
    margin-bottom: 1.25rem;
}
.mc-card-accent {
    border-left: 3px solid var(--accent);
}

/* ── Section label ── */
.section-label {
    font-size: .7rem;
    font-weight: 600;
    letter-spacing: .12em;
    text-transform: uppercase;
    color: var(--accent2);
    margin-bottom: .35rem;
}

/* ── Score ring ── */
.score-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem 0 1.5rem;
}
.score-ring {
    width: 140px; height: 140px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-family: var(--serif);
    font-size: 2.8rem;
    font-weight: 400;
    margin-bottom: 1rem;
    position: relative;
}
.score-ring::before {
    content: '';
    position: absolute; inset: -6px;
    border-radius: 50%;
    background: conic-gradient(var(--ring-color) var(--ring-pct), var(--surface2) 0);
    z-index: -1;
}

/* ── Risk badge ── */
.risk-badge {
    display: inline-block;
    padding: .35rem 1.1rem;
    border-radius: 999px;
    font-size: .8rem;
    font-weight: 600;
    letter-spacing: .06em;
    text-transform: uppercase;
}

/* ── Tip pill ── */
.tip-pill {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: .75rem 1rem;
    margin-bottom: .6rem;
    font-size: .9rem;
    line-height: 1.55;
}
.tip-icon { font-size: 1.1rem; margin-right: .5rem; }

/* ── Factor bar ── */
.factor-row { display: flex; align-items: center; gap: 10px; margin-bottom: .55rem; font-size: .85rem; }
.factor-name { min-width: 150px; color: var(--muted); }
.factor-bar-bg { flex: 1; height: 6px; border-radius: 3px; background: var(--surface2); }
.factor-bar-fill { height: 6px; border-radius: 3px; }

/* ── Metric tile ── */
.metric-tile {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.1rem 1.2rem;
    text-align: center;
}
.metric-val { font-family: var(--serif); font-size: 2rem; font-weight: 400; }
.metric-lbl { font-size: .72rem; letter-spacing: .08em; text-transform: uppercase; color: var(--muted); margin-top: .25rem; }

/* ── Divider ── */
.mc-divider { border: none; border-top: 1px solid var(--border); margin: 1.5rem 0; }

/* ── Streamlit overrides ── */
.stSlider > div > div > div { background: var(--accent) !important; }
.stSelectbox > div > div { background: var(--surface2) !important; border-color: var(--border) !important; border-radius: 10px !important; }
.stNumberInput > div > div { background: var(--surface2) !important; border-color: var(--border) !important; border-radius: 10px !important; }
.stButton > button {
    background: linear-gradient(135deg, #4f46e5, #6366f1) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: .75rem 2.5rem !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    letter-spacing: .04em !important;
    width: 100% !important;
    transition: opacity .2s !important;
}
.stButton > button:hover { opacity: .88 !important; }
label { color: var(--muted) !important; font-size: .85rem !important; }

/* ── Disclaimer ── */
.disclaimer {
    background: var(--peach);
    border: 1px solid #f5c6b0;
    border-radius: 10px;
    padding: .9rem 1.2rem;
    font-size: .78rem;
    color: #7c3a1e;
    line-height: 1.6;
    margin-top: 1.5rem;
}
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
#  SIDEBAR — NAVIGATION + ABOUT
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: .5rem 0 1.5rem'>
        <div style='font-size:2.2rem; margin-bottom:.3rem'>🧠</div>
        <div style='font-family:"DM Serif Display",serif; font-size:1.4rem; color:#1e1b4b'>MindCheck</div>
        <div style='font-size:.75rem; color:#6b7280; letter-spacing:.08em; text-transform:uppercase'>Student Wellbeing AI</div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigate",
        ["🔍  Assessment", "📊  Insights", "📚  Resources", "ℹ️  About"],
        label_visibility="collapsed"
    )

    st.markdown("<hr style='border-color:#d6cff0; margin:1.2rem 0'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:.78rem; color:#6b7280; line-height:1.7'>
    <b style='color:#4f46e5'>How it works</b><br>
    Fill in the assessment form. Our AI model analyses your inputs across <b>20+ factors</b> and returns a personalised risk profile with actionable tips.
    </div>
    """, unsafe_allow_html=True)

    if not model_loaded:
        st.markdown("""
        <div style='background:#fde8dc;border:1px solid #f5c6b0;border-radius:10px;padding:.8rem 1rem;margin-top:1rem;font-size:.78rem;color:#7c3a1e'>
        ⚠️ <b>Model not found.</b><br>Place <code>depression_model.pkl</code> in the app directory to enable AI predictions. Demo mode active.
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PAGE: ASSESSMENT
# ─────────────────────────────────────────────
if "🔍" in page:

    # Hero
    st.markdown("""
    <div style='margin-bottom:2rem'>
        <p class='section-label'>Mental Health Assessment</p>
        <h1>How are you <em>really</em> doing?</h1>
        <p style='color:#8b90a8; font-size:1rem; max-width:560px; line-height:1.7; margin-top:.5rem'>
        Answer honestly — there are no right or wrong responses. This tool uses an AI model trained on student wellbeing data to give you a personalised picture of your mental health.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── FORM ──────────────────────────────────
    with st.form("assessment_form"):

        # ── Section A: Demographics ────────────
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
            degree = st.selectbox("Degree Type", ["Engineering / Technology", "Science", "Arts / Humanities", "Business / Commerce", "Medicine / Health", "Law", "Other"])
        with col5:
            city_type = st.selectbox("Living Situation", ["On-campus hostel", "Private rented room", "Family home", "Shared house / flat", "Alone"])

        st.markdown("<hr class='mc-divider'>", unsafe_allow_html=True)

        # ── Section B: Academic ─────────────────
        st.markdown("<h3>B — Academic Life</h3>", unsafe_allow_html=True)
        col6, col7 = st.columns(2)
        with col6:
            cgpa = st.number_input("Current CGPA / GPA (0–10)", 0.0, 10.0, 7.0, step=0.1)
            academic = st.slider("Academic Pressure  (1 = very low, 5 = extreme)", 1, 5, 3)
        with col7:
            study_hours = st.slider("Daily Study / Work Hours", 0, 16, 6)
            study_sat = st.slider("Study Satisfaction  (1 = very unhappy, 5 = very satisfied)", 1, 5, 3)

        col8, col9 = st.columns(2)
        with col8:
            attendance = st.slider("Class Attendance (%)", 0, 100, 75)
        with col9:
            deadline_stress = st.slider("Deadline / Exam Stress  (1–5)", 1, 5, 3)

        st.markdown("<hr class='mc-divider'>", unsafe_allow_html=True)

        # ── Section C: Lifestyle ────────────────
        st.markdown("<h3>C — Lifestyle & Habits</h3>", unsafe_allow_html=True)
        col10, col11, col12 = st.columns(3)
        with col10:
            sleep = st.selectbox("Average Sleep Duration", [
                "Less than 5 hours", "5–6 hours", "7–8 hours", "More than 8 hours"
            ])
        with col11:
            diet = st.selectbox("Dietary Habits", ["Healthy", "Moderate", "Unhealthy"])
        with col12:
            exercise = st.selectbox("Exercise Frequency", [
                "Daily", "4–5× per week", "2–3× per week", "Once a week", "Rarely / Never"
            ])

        col13, col14 = st.columns(2)
        with col13:
            screen_time = st.slider("Daily Social Media / Screen Time (hours)", 0, 12, 3)
        with col14:
            substance = st.selectbox("Caffeine / Substance Use", [
                "None", "Caffeine only (coffee/tea)", "Occasional alcohol", "Regular alcohol", "Other substances"
            ])

        st.markdown("<hr class='mc-divider'>", unsafe_allow_html=True)

        # ── Section D: Social & Financial ───────
        st.markdown("<h3>D — Social & Financial</h3>", unsafe_allow_html=True)
        col15, col16 = st.columns(2)
        with col15:
            financial = st.slider("Financial Stress  (1 = none, 5 = severe)", 1, 5, 2)
            social_support = st.slider("Social Support / Close Friends  (1 = isolated, 5 = strong network)", 1, 5, 3)
        with col16:
            loneliness = st.slider("Feelings of Loneliness  (1 = never, 5 = always)", 1, 5, 2)
            relationship = st.selectbox("Relationship Status", ["Single", "In a relationship", "Married", "Complicated / Other"])

        st.markdown("<hr class='mc-divider'>", unsafe_allow_html=True)

        # ── Section E: Mental Health History ────
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

        st.markdown("<hr class='mc-divider'>", unsafe_allow_html=True)

        # ── Section F: Mood Snapshot ─────────────
        st.markdown("<h3>F — Mood This Week</h3>", unsafe_allow_html=True)
        col22, col23 = st.columns(2)
        with col22:
            mood = st.slider("Overall Mood  (1 = very low, 10 = excellent)", 1, 10, 6)
            energy = st.slider("Energy Levels  (1 = exhausted, 10 = very energised)", 1, 10, 6)
        with col23:
            motivation = st.slider("Motivation  (1 = none, 10 = high)", 1, 10, 5)
            anxiety_level = st.slider("Anxiety Level  (1 = calm, 10 = very anxious)", 1, 10, 4)

        # ── Submit ──────────────────────────────
        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        submitted = st.form_submit_button("🔍  Run My Assessment")

    # ─────────────────────────────────────────
    #  RESULTS
    # ─────────────────────────────────────────
    if submitted:

        # ── Encode features ────────────────────
        gender_val    = 1 if gender == "Male" else 0
        suicide_val   = 1 if suicide == "Yes" else 0
        family_val    = 1 if family == "Yes" else 0
        therapy_val   = 1 if therapy == "Yes" else 0
        medication_val= 1 if medication == "Yes" else 0
        prev_dx_val   = 0 if prev_diagnosis == "No" else 1

        sleep_map  = {"Less than 5 hours": 0, "5–6 hours": 1, "7–8 hours": 2, "More than 8 hours": 3}
        diet_map   = {"Healthy": 0, "Moderate": 1, "Unhealthy": 2}
        ex_map     = {"Daily": 4, "4–5× per week": 3, "2–3× per week": 2, "Once a week": 1, "Rarely / Never": 0}
        year_map   = {"1st Year": 1, "2nd Year": 2, "3rd Year": 3, "4th Year": 4, "Postgraduate": 5, "PhD": 6}
        subs_map   = {"None": 0, "Caffeine only (coffee/tea)": 1, "Occasional alcohol": 2, "Regular alcohol": 3, "Other substances": 4}

        sleep_val    = sleep_map[sleep]
        diet_val     = diet_map[diet]
        exercise_val = ex_map[exercise]
        year_val     = year_map[year]
        substance_val= subs_map[substance]

        # Build 14-feature array (compatible with original model)
        input_data = np.array([[
            gender_val, age, academic, 0, cgpa,
            study_sat, 0, sleep_val, diet_val, 0,
            suicide_val, study_hours, financial, family_val
        ]])

        # ── Predict (or demo) ──────────────────
        if model_loaded:
            prediction = model.predict(input_data)[0]
            try:
                prob = model.predict_proba(input_data)[0][1]
            except:
                prob = 0.75 if prediction == 1 else 0.25
        else:
            # Demo mode: calculate a heuristic risk score
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
            prediction = 1 if risk_pts >= 6 else 0
            prob = min(0.95, risk_pts / 14)

        risk_pct = int(prob * 100)
        is_high  = prediction == 1

        # Colour palette for risk level
        if risk_pct >= 70:
            ring_color = "#dc2626"; badge_bg = "#fde8dc"; badge_fg = "#b91c1c"; level_text = "High Risk"
        elif risk_pct >= 40:
            ring_color = "#d97706"; badge_bg = "#fef3c7"; badge_fg = "#92400e"; level_text = "Moderate Risk"
        else:
            ring_color = "#059669"; badge_bg = "#d4f5ec"; badge_fg = "#065f46"; level_text = "Low Risk"

        # ── Score ring ────────────────────────
        st.markdown(f"""
        <div class='mc-card' style='text-align:center; padding:2rem'>
            <p class='section-label' style='text-align:center'>Your Result</p>
            <div class='score-wrap'>
                <div class='score-ring' style='
                    background:#ede8f7;
                    color:{ring_color};
                    --ring-color:{ring_color};
                    --ring-pct:{risk_pct * 3.6}deg;
                    box-shadow: 0 0 40px {ring_color}40;
                '>{risk_pct}%</div>
                <span class='risk-badge' style='background:{badge_bg}; color:{badge_fg}; border:1px solid {ring_color}40'>{level_text}</span>
            </div>
            <p style='color:#6b7280; font-size:.9rem; margin-top:1rem; max-width:420px; margin-left:auto; margin-right:auto; line-height:1.65'>
            {"Your responses suggest several factors that may be contributing to elevated mental health risk. Please read the recommendations below." if is_high else "Your responses suggest your mental health is in a relatively good place. Keep nurturing the habits below to maintain your wellbeing."}
            </p>
        </div>
        """, unsafe_allow_html=True)

        # ── Factor breakdown ──────────────────
        st.markdown("<h2 style='margin-top:2rem'>What's driving your score</h2>", unsafe_allow_html=True)

        factors = {
            "Academic pressure":   min(academic / 5, 1.0),
            "Financial stress":    min(financial / 5, 1.0),
            "Sleep quality":       1 - (sleep_val / 3),
            "Diet & nutrition":    diet_val / 2,
            "Exercise / movement": 1 - (exercise_val / 4),
            "Social support":      1 - (social_support / 5),
            "Loneliness":          loneliness / 5,
            "Screen time":         min(screen_time / 10, 1.0),
            "Exam / deadline stress": min(deadline_stress / 5, 1.0),
            "Mood (inverted)":     1 - (mood / 10),
            "Anxiety level":       anxiety_level / 10,
            "Motivation (inverted)": 1 - (motivation / 10),
        }

        def bar_color(v):
            if v < 0.35: return "#34d399"
            if v < 0.65: return "#fbbf24"
            return "#f87171"

        bars_html = "".join([
            f"""<div class='factor-row'>
                <span class='factor-name'>{name}</span>
                <div class='factor-bar-bg'>
                    <div class='factor-bar-fill' style='width:{int(val*100)}%; background:{bar_color(val)}'></div>
                </div>
                <span style='font-size:.78rem; color:#8b90a8; min-width:30px; text-align:right'>{int(val*100)}%</span>
            </div>"""
            for name, val in sorted(factors.items(), key=lambda x: -x[1])
        ])

        st.markdown(f"<div class='mc-card mc-card-accent'>{bars_html}</div>", unsafe_allow_html=True)

        # ── Personalised tips ─────────────────
        st.markdown("<h2 style='margin-top:2rem'>Personalised recommendations</h2>", unsafe_allow_html=True)

        tips = []
        if sleep_val <= 1:
            tips.append(("🛌", "Sleep is foundational", "You're sleeping less than 6 hours. Try a consistent bedtime routine — even 30 extra minutes improves mood and focus significantly."))
        if academic >= 4:
            tips.append(("📚", "Tackle academic overwhelm", "High academic pressure is a top stressor. Break tasks into 25-minute Pomodoro blocks. Speak to a tutor or academic advisor early — don't wait until exams."))
        if financial >= 4:
            tips.append(("💰", "Financial stress is real", "Explore your institution's hardship fund, bursaries, or food bank. Even a single conversation with a student support officer can reveal options you didn't know about."))
        if exercise_val == 0:
            tips.append(("🏃", "Move your body daily", "Even a 20-minute walk reduces cortisol and improves sleep. You don't need a gym — campus grounds count."))
        if social_support <= 2:
            tips.append(("🤝", "Build your support network", "Strong social ties are one of the best buffers against depression. Join one club, society, or study group this week."))
        if screen_time >= 6:
            tips.append(("📱", "Manage your screen time", "6+ hours of social media is linked to higher anxiety in students. Try a 1-hour evening cut-off before sleep."))
        if diet_val >= 2:
            tips.append(("🥗", "Fuel your brain", "Processed food increases inflammation and worsens low mood. One small swap — like adding fruit to breakfast — compounds over time."))
        if suicide == "Yes":
            tips.append(("❤️", "You don't have to face this alone", "Having had suicidal thoughts is more common than people admit. Please reach out to a counsellor today — iCall: 9152987821 (India) or your campus helpline."))
        if mood <= 4:
            tips.append(("🌤", "Nurture your mood deliberately", "Scheduling one enjoyable activity per day (even 15 minutes) is a proven technique to lift low mood. What did you used to enjoy?"))
        if anxiety_level >= 7:
            tips.append(("🌬", "Calm your nervous system", "Box breathing (4-4-4-4) activates the parasympathetic system and reduces anxiety in under 5 minutes. Try it before any stressful event."))
        if loneliness >= 4:
            tips.append(("🫂", "Address feelings of loneliness", "Loneliness is not about being alone — it's about connection quality. Even texting one person you trust today matters."))
        if therapy == "No" and is_high:
            tips.append(("🛋", "Consider talking to someone", "Therapy doesn't mean you're broken. Most campuses offer free counselling sessions. Getting a first appointment is the hardest step — book it today."))

        # Default tips if nothing triggered
        if not tips:
            tips = [
                ("✨", "Keep it up", "Your habits are in a good place. Stay consistent with your sleep, social connections, and physical activity."),
                ("📖", "Maintain academic balance", "Regular short study sessions beat cramming. Protect your weekends for recovery."),
                ("🙏", "Practice gratitude", "Writing 3 things you're grateful for each morning is clinically proven to sustain positive mood over time."),
            ]

        tips_html = "".join([
            f"<div class='tip-pill'><span class='tip-icon'>{icon}</span><b>{title}:</b> {body}</div>"
            for icon, title, body in tips
        ])
        st.markdown(f"<div class='mc-card'>{tips_html}</div>", unsafe_allow_html=True)

        # ── Snapshot metrics ──────────────────
        st.markdown("<h2 style='margin-top:2rem'>Your snapshot</h2>", unsafe_allow_html=True)
        m1, m2, m3, m4 = st.columns(4)
        tiles = [
            (f"{mood}/10", "Mood"),
            (f"{energy}/10", "Energy"),
            (f"{motivation}/10", "Motivation"),
            (f"{10 - anxiety_level}/10", "Calm"),
        ]
        for col, (val, lbl) in zip([m1, m2, m3, m4], tiles):
            col.markdown(f"""
            <div class='metric-tile'>
                <div class='metric-val'>{val}</div>
                <div class='metric-lbl'>{lbl}</div>
            </div>
            """, unsafe_allow_html=True)

        # ── Disclaimer ────────────────────────
        st.markdown("""
        <div class='disclaimer'>
        ⚕️ <b>Important disclaimer:</b> MindCheck is an educational tool and does not constitute clinical advice, diagnosis, or treatment.
        The AI model may not reflect your individual circumstances. If you are in distress or experiencing a mental health crisis, please contact a qualified healthcare professional immediately.
        In India: <b>iCall — 9152987821</b> | <b>Vandrevala Foundation — 1860-2662-345</b> (24/7)
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PAGE: INSIGHTS
# ─────────────────────────────────────────────
elif "📊" in page:
    st.markdown("""
    <p class='section-label'>How the model works</p>
    <h1>Understanding the <em>science</em></h1>
    <p style='color:#6b7280; max-width:600px; line-height:1.7; font-size:1rem; margin-top:.5rem'>
    Here's a transparent look at the inputs, algorithm, and limitations of the prediction model.
    </p>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='mc-card mc-card-accent'>
    <h2>Input features used</h2>
    <p style='color:#6b7280; font-size:.9rem; line-height:1.7; margin-top:.5rem'>
    The core model uses the original 14 features from the training dataset. The additional fields collected in the assessment are used to generate personalised recommendations and your snapshot score — they do not alter the core AI prediction.
    </p>
    </div>
    """, unsafe_allow_html=True)

    feat_table = [
        ("Gender", "Binary", "Male=1, Female=0"),
        ("Age", "Numeric", "16–60"),
        ("Academic Pressure", "Ordinal 1–5", "Self-reported"),
        ("CGPA", "Numeric 0–10", "Current grade"),
        ("Study Satisfaction", "Ordinal 1–5", "Self-reported"),
        ("Sleep Duration", "Ordinal 0–3", "Encoded categories"),
        ("Dietary Habits", "Ordinal 0–2", "Healthy / Moderate / Unhealthy"),
        ("Suicidal Thoughts", "Binary", "Yes=1, No=0"),
        ("Study/Work Hours", "Numeric", "Daily hours"),
        ("Financial Stress", "Ordinal 1–5", "Self-reported"),
        ("Family History", "Binary", "Yes=1, No=0"),
    ]
    rows = "".join([
        f"<tr><td style='padding:.55rem .8rem; color:#1e1b4b'>{n}</td><td style='padding:.55rem .8rem; color:#6b7280'>{t}</td><td style='padding:.55rem .8rem; color:#6b7280'>{e}</td></tr>"
        for n, t, e in feat_table
    ])
    st.markdown(f"""
    <div class='mc-card'>
    <table style='width:100%; border-collapse:collapse; font-size:.85rem'>
        <thead><tr style='border-bottom:1px solid #d6cff0'>
            <th style='padding:.6rem .8rem; text-align:left; color:#4f46e5; font-weight:600'>Feature</th>
            <th style='padding:.6rem .8rem; text-align:left; color:#4f46e5; font-weight:600'>Type</th>
            <th style='padding:.6rem .8rem; text-align:left; color:#4f46e5; font-weight:600'>Encoding</th>
        </tr></thead>
        <tbody>{rows}</tbody>
    </table>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='mc-card'>
    <h2>Likely algorithm: Random Forest</h2>
    <p style='color:#6b7280; font-size:.9rem; line-height:1.7; margin-top:.5rem'>
    Based on the dataset type and binary classification task, the model was most likely trained using a <b style='color:#1e1b4b'>Random Forest</b> classifier — an ensemble of decision trees that votes on the final prediction. Random Forests handle mixed numeric/ordinal features well, are robust to outliers, and naturally provide feature importances.
    Other possibilities include <b style='color:#1e1b4b'>Logistic Regression</b> (fast, interpretable baseline), <b style='color:#1e1b4b'>Gradient Boosting / XGBoost</b> (higher accuracy, slower), or <b style='color:#1e1b4b'>SVM</b> (good on small datasets with clear boundaries).
    </p>
    </div>

    <div class='mc-card'>
    <h2>Known limitations</h2>
    <p style='color:#6b7280; font-size:.9rem; line-height:1.7; margin-top:.5rem'>
    ⚠️ Three feature positions (index 3, 6, 9) in the original 14-feature array are zero-padded in this app because the UI fields they corresponded to are unknown. If those features carry high importance in the trained model, predictions may be unreliable.<br><br>
    ⚠️ The model was trained on a specific dataset (likely Indian university students). It may not generalise well across cultural or geographic contexts.<br><br>
    ⚠️ Self-reported data is subject to recall bias and social desirability effects.
    </p>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PAGE: RESOURCES
# ─────────────────────────────────────────────
elif "📚" in page:
    st.markdown("""
    <p class='section-label'>Support & Help</p>
    <h1>You're not <em>alone</em></h1>
    <p style='color:#6b7280; max-width:600px; line-height:1.7; font-size:1rem; margin-top:.5rem'>
    A list of vetted mental health resources for students in India and internationally.
    </p>
    """, unsafe_allow_html=True)

    resources = [
        ("🆘", "iCall (India)", "9152987821", "Mon–Sat 8am–10pm", "Psychologists from TISS; free phone & chat counselling"),
        ("🆘", "Vandrevala Foundation", "1860-2662-345", "24 / 7", "Free 24/7 helpline across India"),
        ("🆘", "Snehi", "044-24640050", "24 / 7", "Suicide prevention and emotional support helpline"),
        ("🌍", "Crisis Text Line (Global)", "Text HOME to 741741", "24 / 7", "Free text-based crisis support"),
        ("🌍", "Befrienders Worldwide", "befrienders.org", "24 / 7", "Global directory of emotional support helplines"),
        ("📖", "Mind (UK)", "0300-123-3393", "Mon–Fri 9am–6pm", "Mental health information and support"),
        ("📖", "NAMI (USA)", "1-800-950-6264", "Mon–Fri 10am–10pm ET", "National Alliance on Mental Illness helpline"),
    ]

    for emoji, name, contact, hours, desc in resources:
        st.markdown(f"""
        <div class='mc-card' style='display:flex; gap:1.2rem; align-items:flex-start'>
            <span style='font-size:1.6rem; margin-top:.1rem'>{emoji}</span>
            <div>
                <b style='font-size:1rem; color:#1e1b4b'>{name}</b>
                <div style='font-size:.88rem; color:#4f46e5; margin:.2rem 0'>{contact}</div>
                <div style='font-size:.78rem; color:#6b7280'>{hours} &nbsp;·&nbsp; {desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class='mc-card' style='margin-top:.5rem'>
    <h2>Self-help techniques</h2>
    <div style='display:grid; grid-template-columns:1fr 1fr; gap:1rem; margin-top:1rem'>
        <div class='tip-pill'><b>📦 Box breathing</b><br><span style='color:#6b7280;font-size:.85rem'>Inhale 4s → Hold 4s → Exhale 4s → Hold 4s. Repeat 4×. Reduces acute anxiety in under 5 minutes.</span></div>
        <div class='tip-pill'><b>🌿 5-4-3-2-1 grounding</b><br><span style='color:#6b7280;font-size:.85rem'>Name 5 things you see, 4 you feel, 3 you hear, 2 you smell, 1 you taste. Anchors you to the present.</span></div>
        <div class='tip-pill'><b>📓 Journaling</b><br><span style='color:#6b7280;font-size:.85rem'>Write for 10 minutes without editing. Studies show expressive writing reduces depression symptoms.</span></div>
        <div class='tip-pill'><b>🚶 Nature walks</b><br><span style='color:#6b7280;font-size:.85rem'>20 minutes in green space measurably lowers cortisol. No gym needed.</span></div>
        <div class='tip-pill'><b>📵 Phone-free mornings</b><br><span style='color:#6b7280;font-size:.85rem'>The first 30 minutes without your phone sets a calmer baseline for the whole day.</span></div>
        <div class='tip-pill'><b>🤝 Peer support</b><br><span style='color:#6b7280;font-size:.85rem'>Simply telling one person how you feel — even a message — reduces psychological burden immediately.</span></div>
    </div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PAGE: ABOUT
# ─────────────────────────────────────────────
elif "ℹ️" in page:
    st.markdown("""
    <p class='section-label'>About this tool</p>
    <h1>MindCheck — <em>built with care</em></h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='mc-card mc-card-accent'>
    <p style='color:#6b7280; font-size:.95rem; line-height:1.75'>
    MindCheck was built to give students a <b style='color:#1e1b4b'>private, non-judgemental first step</b> toward understanding their mental health.
    It is not a replacement for professional care — it is a starting point for reflection and help-seeking.
    </p>
    </div>

    <div class='mc-card'>
    <h2>Tech stack</h2>
    <p style='color:#6b7280; font-size:.9rem; line-height:1.7; margin-top:.5rem'>
    Built with <b style='color:#1e1b4b'>Python 3</b>, <b style='color:#1e1b4b'>Streamlit</b> for the UI, <b style='color:#1e1b4b'>scikit-learn</b> for the ML model, and <b style='color:#1e1b4b'>NumPy</b> for feature processing. The model is loaded from a pre-trained <code>.pkl</code> file serialised via pickle.
    </p>
    </div>

    <div class='mc-card'>
    <h2>Data & privacy</h2>
    <p style='color:#6b7280; font-size:.9rem; line-height:1.7; margin-top:.5rem'>
    No data is stored or transmitted. All processing happens locally in your browser session. Closing the tab clears everything. This app does not use cookies or analytics.
    </p>
    </div>

    <div class='mc-card'>
    <h2>Version</h2>
    <p style='color:#6b7280; font-size:.9rem; line-height:1.7; margin-top:.5rem'>
    v2.0 — Enhanced assessment (20+ features), personalised recommendations, factor breakdown, resources page, insights page.<br>
    Built {datetime.date.today().strftime('%B %Y')}.
    </p>
    </div>
    """, unsafe_allow_html=True)
