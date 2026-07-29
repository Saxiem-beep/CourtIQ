%%writefile app.py
import streamlit as st
import pandas as pd
import json

# --- Page Config ---
st.set_page_config(page_title="CourtIQ Dashboard", page_icon="🏀", layout="wide")

st.title("CourtIQ 🧠")
st.subheader("AI Performance Coaching & Risk Management")

# --- Load Data ---
@st.cache_data
def load_data():
    with open("data/mock_athlete_data.json", "r") as file:
        data = json.load(file)
    df = pd.DataFrame(data).sort_values(by="injury_risk_score", ascending=False)
    return df

df = load_data()

# --- Dashboard Layout ---
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 🚨 High-Priority Alerts (Sorted by Risk Score)")
    st.dataframe(
        df[['name', 'sport', 'risk_status', 'injury_risk_score']], 
        use_container_width=True,
        hide_index=True
    )

with col2:
    st.markdown("### 💬 Ask the RAG Coach")
    st.info("Ask a question based on indexed coaching manuals.")
    
    user_query = st.text_input("Ask about an athlete or drill:")
    if st.button("Generate Insight"):
        if user_query:
            st.success(f"**CourtIQ AI:** Based on the biomechanics data and training history, I recommend reducing {df.iloc[0]['name']}'s plyometric load by 20% this week to lower the {df.iloc[0]['injury_risk_score']} risk score.")
        else:
            st.warning("Please enter a question.")
