import streamlit as st
import pickle
import numpy as np

# Page configuration
st.set_page_config(page_title="Student Mental Health Tracker", page_icon="🧠")

# Load trained model
try:
    model = pickle.load(open('depression_model.pkl', 'rb'))
except FileNotFoundError:
    st.error("Model file 'depression_model.pkl' not found. Please check your directory.")

st.title("🎓 Student Depression Prediction System")
st.write("Assess potential mental health risk factors using our AI model.")

# --- INPUT SECTION ---
col1, col2 = st.columns(2)

with col1:
    gender = st.selectbox("Gender", ["Male", "Female"])
    age = st.number_input("Age", 18, 40, value=20)
    academic = st.slider("Academic Pressure (1-5)", 1, 5, 3)
    cgpa = st.number_input("Current CGPA", 0.0, 10.0, 7.5)
    hours = st.slider("Daily Study/Work Hours", 0, 12, 6)

with col2:
    sleep = st.selectbox(
        "Average Sleep Duration",
        ["Less than 5 hours", "5-6 hours", "7-8 hours", "More than 8 hours"]
    )
    diet = st.selectbox(
        "Dietary Habits",
        ["Healthy", "Moderate", "Unhealthy"]
    )
    study_sat = st.slider("Study Satisfaction (1-5)", 1, 5, 3)
    financial = st.slider("Financial Stress (1-5)", 1, 5, 3)

st.subheader("Personal History")
c3, c4 = st.columns(2)
with c3:
    suicide = st.selectbox("Ever had Suicidal Thoughts?", ["No", "Yes"])
with c4:
    family = st.selectbox("Family History of Mental Illness?", ["No", "Yes"])

# --- DATA PREPROCESSING ---
gender_val = 1 if gender == "Male" else 0
suicide_val = 1 if suicide == "Yes" else 0
family_val = 1 if family == "Yes" else 0
financial_val = financial  # Fixed the missing variable here

sleep_map = {
    "Less than 5 hours": 0,
    "5-6 hours": 1,
    "7-8 hours": 2,
    "More than 8 hours": 3
}
diet_map = {
    "Healthy": 0,
    "Moderate": 1,
    "Unhealthy": 2
}

sleep_val = sleep_map[sleep]
diet_val = diet_map[diet]

# Constructing the input array (Ensuring all 14 features match your model training)
input_data = np.array([[
    gender_val, age, academic, 0, cgpa,
    study_sat, 0, sleep_val, diet_val, 0,
    suicide_val, hours, financial_val, family_val
]])

# --- PREDICTION & FEEDBACK ---
st.markdown("---")

if st.button("Predict Depression Risk"):
    prediction = model.predict(input_data)
    
    if prediction[0] == 1:
        st.error("### ⚠️ Result: High Depression Risk")
        
        # Tip for High Risk
        st.warning("**Immediate Wellness Tips:**")
        st.info("""
        * **Seek Support:** Reach out to a campus counselor or mental health professional.
        * **Connection:** Talk to a friend or family member about how you're feeling.
        * **Mindfulness:** Practice grounding exercises (like naming 5 things you see) to manage anxiety.
        * **Emergency:** If you feel unsafe, please contact a 24/7 crisis helpline immediately.
        """)
    else:
        st.success("### ✅ Result: Low Depression Risk")
        st.balloons()
        
        # Maintenance Tips
        st.markdown("#### ✨ How to Maintain Your Mental Wellbeing")
        st.write("""
        * **Routine:** Stick to a consistent sleep schedule of at least 7 hours.
        * **Balance:** Take frequent short breaks (5-10 mins) during long study sessions.
        * **Nutrition:** Keep choosing healthy meals; gut health is closely linked to mood.
        * **Activity:** Aim for 30 minutes of light physical activity most days of the week.
        """)

# --- FOOTER ---
st.markdown("---")
st.caption("""
**Disclaimer:** This tool is for educational purposes only and is not a clinical diagnosis. 
If you are struggling, please consult a qualified healthcare professional.
""")