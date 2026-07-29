import streamlit as st
import pandas as pd
import random
from modules.data_generator import generate_athlete_data
from modules.leaderboard import RealTimeLeaderboard
from modules.risk_predictor import RiskPredictor
from modules.rag_engine import CoachingRAG

# ==========================================
# Application State Initialization
# ==========================================
st.set_page_config(page_title="CourtIQ | AI Coaching", layout="wide", page_icon="🏀")

@st.cache_resource
def load_models():
    return RiskPredictor(), CoachingRAG()

if 'leaderboard' not in st.session_state:
    st.session_state.leaderboard = RealTimeLeaderboard()
    # Initialize roster
    df = generate_athlete_data(50)
    st.session_state.roster_df = df
    for _, row in df.iterrows():
        status = "High Risk" if row['is_high_risk'] == 1 else "Optimal"
        st.session_state.leaderboard.add_or_update_athlete(
            athlete_id=row['athlete_id'],
            name=row['name'],
            team=row['team'],
            score=row['performance_score'],
            risk_flag=status
        )

risk_predictor, rag_engine = load_models()

# ==========================================
# UI Layout
# ==========================================
st.title("CourtIQ Performance Dashboard")
tab1, tab2, tab3 = st.tabs(["🏆 Live Leaderboard", "⚠️ Risk Inspector", "🧠 AI Coach (RAG)"])

# ------------------------------------------
# Tab 1: Leaderboard
# ------------------------------------------
with tab1:
    st.header("Real-Time Athlete Leaderboard")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        team_filter = st.selectbox("Filter by Team", ["All", "Red Hawks", "Blue Titans", "Iron Wolves", "Silver Eagles"])
    
    with col2:
        # Simulate real-time score updates
        if st.button("🔄 Simulate Live Match Update"):
            random_id = random.choice(st.session_state.roster_df['athlete_id'].tolist())
            current_data = st.session_state.leaderboard.athletes_db[random_id]
            new_score = round(current_data['score'] + random.uniform(1.0, 5.0), 1)
            
            st.session_state.leaderboard.add_or_update_athlete(
                athlete_id=random_id,
                name=current_data['name'],
                team=current_data['team'],
                score=new_score,
                risk_flag=current_data['risk_flag']
            )
            st.success(f"Updated {current_data['name']} score to {new_score}")

    top_athletes = st.session_state.leaderboard.get_top_n(n=20, team_filter=team_filter)
    
    if top_athletes:
        df_display = pd.DataFrame(top_athletes)
        # Apply color coding to the risk status
        def color_status(val):
            color = '#ff4b4b' if val == 'High Risk' else '#21c354'
            return f'color: {color}; font-weight: bold'
        
        st.dataframe(
            df_display.style.map(color_status, subset=['Status']),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No athletes found for this team.")

# ------------------------------------------
# Tab 2: Risk Inspector
# ------------------------------------------
with tab2:
    st.header("Predictive Injury Risk Modeling")
    
    selected_name = st.selectbox(
        "Select Athlete", 
        st.session_state.roster_df['name'].tolist()
    )
    
    athlete_data = st.session_state.roster_df[st.session_state.roster_df['name'] == selected_name].iloc[0]
    
    st.markdown(f"### Adjust Workload for **{selected_name}**")
    
    colA, colB = st.columns(2)
    with colA:
        training_hrs = st.slider("Weekly Training Hours", 0.0, 40.0, float(athlete_data['training_hours_weekly']))
        exertion = st.slider("Perceived Exertion (1-10)", 1, 10, int(athlete_data['perceived_exertion_1to10']))
        sleep = st.slider("Average Sleep (Hours)", 3.0, 12.0, float(athlete_data['sleep_hours']))
    
    with colB:
        jump_load = st.slider("Jump Load Count (Weekly)", 0, 500, int(athlete_data['jump_load_count']))
        past_injuries = st.number_input("Past Injuries", 0, 10, int(athlete_data['past_injuries']))
        
        if st.button("Run Predictive Analysis", type="primary"):
            input_features = {
                "training_hours_weekly": training_hrs,
                "perceived_exertion_1to10": exertion,
                "sleep_hours": sleep,
                "past_injuries": past_injuries,
                "jump_load_count": jump_load
            }
            
            result = risk_predictor.predict_athlete_risk(input_features)
            
            st.divider()
            st.subheader("Prediction Results")
            
            metric_col1, metric_col2 = st.columns(2)
            metric_col1.metric("Injury Risk Score", f"{result['risk_score_percent']}%")
            
            status_color = "red" if result['flag'] == "High Risk" else "orange" if result['flag'] == "Elevated" else "green"
            metric_col2.markdown(f"### Status: :{status_color}[{result['flag']}]")
            
            st.markdown("**Primary Risk Drivers:**")
            for factor in result['top_risk_factors']:
                st.markdown(f"- {factor}")

# ------------------------------------------
# Tab 3: RAG Assistant
# ------------------------------------------
with tab3:
    st.header("Knowledge Base & Protocol Assistant")
    st.markdown("Ask natural language questions about recovery, conditioning, and sports science protocols.")
    
    user_query = st.text_input("Ask the Coach AI:", placeholder="e.g., What are the signs of CNS overtraining?")
    
    if st.button("Search Knowledge Base"):
        if user_query.strip():
            with st.spinner("Searching sports science corpus..."):
                response = rag_engine.query_coaching_rag(user_query)
                
                st.info("Answer:")
                st.write(response["answer"])
                
                with st.expander("View Source Context"):
                    for idx, source in enumerate(response["sources"]):
                        st.caption(f"**Chunk {idx + 1}:** {source}")
        else:
            st.warning("Please enter a question.")
