import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from modules.data_generator import generate_athlete_data

class RiskPredictor:
    def __init__(self):
        self.df = generate_athlete_data(200)
        self.model = RandomForestClassifier(n_estimators=50, random_state=42, max_depth=5)
        self.features = [
            "training_hours_weekly", 
            "perceived_exertion_1to10", 
            "sleep_hours", 
            "past_injuries", 
            "jump_load_count"
        ]
        self._train_model()
        
    def _train_model(self):
        X = self.df[self.features]
        y = self.df["is_high_risk"]
        self.model.fit(X, y)
        
    def predict_athlete_risk(self, data: dict) -> dict:
        input_df = pd.DataFrame([data])
        
        # Predict probability of class 1 (High Risk)
        risk_prob = self.model.predict_proba(input_df)[0][1]
        risk_score = int(risk_prob * 100)
        
        flag = "High Risk" if risk_score > 60 else "Elevated" if risk_score > 35 else "Optimal"
        
        # Determine top risk factors based on generic heuristics relative to thresholds
        risk_factors = []
        if data["sleep_hours"] < 6.5:
            risk_factors.append("Inadequate Sleep")
        if data["perceived_exertion_1to10"] > 7:
            risk_factors.append("High Perceived Exertion")
        if data["jump_load_count"] > 200:
            risk_factors.append("Excessive Jump Load")
        if data["past_injuries"] > 0:
            risk_factors.append("Injury History")
            
        if not risk_factors:
            risk_factors.append("Metrics within safe thresholds")
            
        return {
            "risk_score_percent": risk_score,
            "flag": flag,
            "top_risk_factors": risk_factors
        }
