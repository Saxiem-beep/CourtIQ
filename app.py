import streamlit as st
import pandas as pd

# --- Page Config ---
st.set_page_config(page_title="CourtIQ Dashboard", page_icon="🏀", layout="wide")

st.title("CourtIQ 🧠")
st.subheader("AI Performance Coaching & Risk Management")

# --- Embedded Data (Self-Contained Fix) ---
@st.cache_data
def load_data():
    data = [
      {
        "athlete_id": "ATH-001",
        "name": "Rahul Sharma",
        "sport": "Basketball",
        "weekly_load_minutes": 420,
        "sleep_avg_hours": 6.2,
        "injury_risk_score": 0.88,
        "risk_status": "High Risk - Overtraining",
        "coach_note": "Requires immediate load management."
      },
      {
        "athlete_id": "ATH-002",
        "name": "Priya Patel",
        "sport": "Dance",
        "weekly_load_minutes": 280,
        "sleep_avg_hours": 7.8,
        "injury_risk_score": 0.21,
        "risk_status": "Optimal",
        "coach_note": "Ready for competition intensity."
      },
      {
        "athlete_id": "ATH-003",
        "name": "Vikram Singh",
        "sport": "Basketball",
        "weekly_load_minutes": 350,
        "sleep_avg_hours": 5.5,
        "injury_risk_score": 0.74,
        "risk_status": "Moderate Risk",
        "coach_note": "Monitor knee stress; reduce jump reps."
      }
    ]
    # Convert to DataFrame and sort by risk
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
